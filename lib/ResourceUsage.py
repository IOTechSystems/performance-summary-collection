import traceback
import time
from robot.api import logger
import docker

# client = docker.APIClient(base_url="unix://var/run/docker.sock")
client = docker.from_env()

services = {
    "edgex-core-consul": {"binary": ""},
    "edgex-mongo": {"binary": ""},
    "edgex-core-data": {"binary": "/core-data"},
    "edgex-core-metadata": {"binary": "/core-metadata"},
    "edgex-core-command": {"binary": "/core-command"},
    "edgex-support-logging": {"binary": "/support-logging"},
    "edgex-support-notifications": {"binary": "/support-notifications"},
    "edgex-support-scheduler": {"binary": "/support-scheduler"},
    "edgex-export-client": {"binary": "/export-client"},
    "edgex-export-distro": {"binary": "/export-distro"},
    "edgex-support-rulesengine": {"binary": "/edgex/edgex-support-rulesengine/support-rulesengine.jar"},
    "edgex-device-virtual": {"binary": "/device-virtual"}
}


class ResourceUsage(object):

    def __init__(self):
        self._result = ""

    def fetch_footprint_cpu_memory(self):
        # fetch_by_service("edgex-core-data")
        for k in services:
            fetch_by_service(k)

    def show_the_summary_table(self):
        html = """ 
        <table style="border: 1px solid black;white-space: initial;"> 
            <tr style="border: 1px solid black;">
                <th style="border: 1px solid black;">
                    Micro service			 	 
                </th>
                <th style="border: 1px solid black;">
                    Image Footprint
                </th>
                <th style="border: 1px solid black;">
                    Executable
                </th>
                <th style="border: 1px solid black;">
                    Memory used on start up
                </th>
                <th style="border: 1px solid black;">
                    CPU Usage on start up
                </th>
            </tr>
        """

        for k in services:
            html = html + """ 
            <tr style="border: 1px solid black;">
                <td style="border: 1px solid black;">
                    {}			 	 
                </td>
                <td style="border: 1px solid black;">
                    {} MB
                </td>
                <td style="border: 1px solid black;">
                    {} MB
                </td>
                <td style="border: 1px solid black;">
                    {} MB
                </td>
                <td style="border: 1px solid black;">
                    {} %
                </td>
            </tr>
        """.format(
                k, services[k]["imageFootprint"], services[k]["binaryFootprint"], services[k]["memoryUsage"],
                services[k]["cpuUsage"]
            )

        html = html + "</table>"
        logger.info(html, html=True)


def fetch_by_service(service):
    containerName = service
    try:
        container = client.containers.get(containerName)
        imageName = container.attrs["Config"]["Image"]
        image = client.images.get(imageName)
        imageSize = image.attrs["Size"]

        execResult = container.stats(stream=False)
        cpuUsage = calculate_cpu_percent(execResult)
        memoryUsage = calculate_memory_usage(execResult)

        if not services[containerName]["binary"]:
            binarySize = 0
        else:
            _, stat = container.get_archive(services[containerName]["binary"])
            binarySize = stat["size"]

        services[containerName]["imageFootprint"] = format(int(imageSize) / 1000000, '.2f')
        services[containerName]["binaryFootprint"] = format(int(binarySize) / 1000000, '.2f')
        services[containerName]["cpuUsage"] = format(cpuUsage, '.2f')
        services[containerName]["memoryUsage"] = format(int(memoryUsage) / 1000000, '.2f')
        logger.info(containerName + " " + str(services[containerName]))
        # logger.console("\n  "+containerName)
        # logger.console("\n  "+services[containerName]["binary"])
        # logger.console("--- Image size %d Bytes ---" % imageSize)
        # logger.console("--- Binary size %s Bytes ---" % binarySize)
        # logger.console("--- CPU usage %d Bytes ---" % cpuUsage)
        # logger.console("--- Memory usage %d Bytes ---" % memoryUsage)
    except docker.errors.NotFound:
        services[containerName]["imageFootprint"] = 0
        services[containerName]["binaryFootprint"] = 0
        services[containerName]["cpuUsage"] = 0
        services[containerName]["memoryUsage"] = 0
        logger.console(containerName + " container not found")
    except:
        traceback.print_exc()


# https://github.com/docker/cli/blob/master/cli/command/container/stats_helpers.go
# https://github.com/TomasTomecek/sen/blob/master/sen/util.py#L160
def calculate_cpu_percent(d):
    cpu_count = len(d["cpu_stats"]["cpu_usage"]["percpu_usage"])
    cpu_percent = 0.0
    cpu_delta = float(d["cpu_stats"]["cpu_usage"]["total_usage"]) - \
                float(d["precpu_stats"]["cpu_usage"]["total_usage"])
    system_delta = float(d["cpu_stats"]["system_cpu_usage"]) - \
                   float(d["precpu_stats"]["system_cpu_usage"])
    if system_delta > 0.0:
        cpu_percent = cpu_delta / system_delta * 100.0 * cpu_count
    return cpu_percent


def calculate_memory_usage(d):
    return d["memory_stats"]["usage"] - d["memory_stats"]["stats"]["cache"]
