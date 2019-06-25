import traceback
from robot.api import logger
import docker
import platform
from datetime import datetime
import sys

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
        cpuUsage = calculateCPUPercent(execResult)
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
    except docker.errors.NotFound as error:
        services[containerName]["imageFootprint"] = 0
        services[containerName]["binaryFootprint"] = 0
        services[containerName]["cpuUsage"] = 0
        services[containerName]["memoryUsage"] = 0
        logger.error(containerName + " container not found")
        logger.error(error)
    except:
        services[containerName]["imageFootprint"] = 0
        services[containerName]["binaryFootprint"] = 0
        services[containerName]["cpuUsage"] = 0
        services[containerName]["memoryUsage"] = 0
        logger.error(containerName + " fail to fetch resource usage")
        logger.error(traceback.format_exc())


def calculate_memory_usage(d):
    memory_usage = 0
    try:
        memory_usage = d["memory_stats"]["usage"] - d["memory_stats"]["stats"]["cache"]
    except:
        logger.error("fail to calculate memory usage")
        logger.error(traceback.format_exc())
        return memory_usage

    return memory_usage


# https://github.com/docker/cli/blob/master/cli/command/container/stats_helpers.go#L100
def calculateCPUPercent(d):
    percent = 0
    if (platform.system() == "Windows"):
        percent = calculateCPUPercentWindows(d)
    else:
        percent = calculateCPUPercentUnix(d)
    return percent

def calculateCPUPercentWindows(v):
    # Max number of 100ns intervals between the previous time read and now
    readTime = datetime.strptime(v["read"], "%Y-%m-%dT%H:%M:%S.%f").timestamp()
    prereadTime = datetime.strptime(v["preread"], "%Y-%m-%dT%H:%M:%S.%f").timestamp()
    possIntervals = (readTime-prereadTime)/1000                      # Start with number of ns intervals
    possIntervals /= 100                                              # Convert to number of 100ns intervals
    possIntervals *= int(v["num_procs"])                          # Multiple by the number of processors

    # Intervals used
    intervalsUsed = v["cpu_stats"]["cpu_usage"]["total_usage"] - v["precpu_stats"]["cpu_usage"]["total_usage"]

    # Percentage avoiding divide-by-zero
    if (possIntervals > 0):
        return float(intervalsUsed) / float(possIntervals) * 100.0
    
    return 0.00

def calculateCPUPercentUnix(v):
    # logger.console(v)
    previousCPU = v["precpu_stats"]["cpu_usage"]["total_usage"]
    previousSystem = v["precpu_stats"]["system_cpu_usage"]

    cpuPercent = 0.0
    # calculate the change for the cpu usage of the container in between readings
    cpuDelta = float(v["cpu_stats"]["cpu_usage"]["total_usage"]) - float(previousCPU)
    # calculate the change for the entire system between readings
    systemDelta = float(v["cpu_stats"]["system_cpu_usage"]) - float(previousSystem)
    onlineCPUs  = float(v["cpu_stats"]["online_cpus"])


    if (onlineCPUs == 0.0) :
        onlineCPUs = float(len(v["cpu_stats"]["cpu_usage"]["percpu_usage"]))

    if ((systemDelta > 0.0) and (cpuDelta > 0.0)): 
        cpuPercent = (cpuDelta / systemDelta) * onlineCPUs * 100.0

    return cpuPercent

