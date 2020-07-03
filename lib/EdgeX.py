from robot.api import logger
import subprocess
import os
import time
import platform
import sys
from dotenv import load_dotenv
import http.client
import copy

services = {
    "core-data": {"composeName": "core-data", "port": 48080, "url": "/api/v1/ping"},
    "core-metadata": {"composeName": "core-metadata", "port": 48081, "url": "/api/v1/ping"},
    "core-command": {"composeName": "core-command", "port": 48082, "url": "/api/v1/ping"},
    "support-logging": {"composeName": "support-logging", "port": 48061, "url": "/api/v1/ping"},
    "support-notifications": {"composeName": "support-notifications", "port": 48060, "url": "/api/v1/ping"},
    "support-scheduler": {"composeName": "support-scheduler", "port": 48085, "url": "/api/v1/ping"},
    "export-client": {"composeName": "export-client", "port": 48071, "url": "/api/v1/ping"},
    "export-distro": {"composeName": "export-distro", "port": 48070, "url": "/api/v1/ping"},
    "device-virtual": {"composeName": "device-virtual", "port": 49990, "url": "/api/v1/ping"},
    "xpert-manager": {"composeName": "xpert-manager", "port": 8080, "url": ""},
}

withoutExportServices = {
    "core-data": {"composeName": "core-data", "port": 48080, "url": "/api/v1/ping"},
    "core-metadata": {"composeName": "core-metadata", "port": 48081, "url": "/api/v1/ping"},
    "core-command": {"composeName": "core-command", "port": 48082, "url": "/api/v1/ping"},
    "support-logging": {"composeName": "support-logging", "port": 48061, "url": "/api/v1/ping"},
    "support-notifications": {"composeName": "support-notifications", "port": 48060, "url": "/api/v1/ping"},
    "support-scheduler": {"composeName": "support-scheduler", "port": 48085, "url": "/api/v1/ping"},
    "app-service-mqtt-export": {"composeName": "app-service", "port": 48097, "url": "/api/v1/ping"},
    "device-virtual": {"composeName": "device-virtual", "port": 49990, "url": "/api/v1/ping"},
    "xpert-manager": {"composeName": "xpert-manager", "port": 8080, "url": ""},
}


class EdgeX(object):

    def __init__(self):
        load_dotenv(dotenv_path="common.env", verbose=True)

    def pull_the_edgex_docker_images(self):
        cmd = docker_compose_cmd()
        cmd.append('pull')
        run_command(cmd)

    def edgex_is_deployed(self):
        # Deploy services
        cmd = docker_compose_cmd()
        cmd.extend(['up', '-d'])
        run_command(cmd)

        time.sleep(20)
        # Check services are started
        check_dependencies_services_startup(services)

    def edgex_is_deployed_with_compose_file(self, file_name):
        # Deploy services
        cmd = docker_compose_cmd()
        cmd.extend(['-f', file_name, 'up', '-d'])
        run_command(cmd)

        time.sleep(20)

        # Check services are started
        if 'export' in file_name:
            dependencies = copy.deepcopy(services)
        else:
            dependencies = copy.deepcopy(withoutExportServices)
        check_dependencies_services_startup(dependencies)

    def shutdown_edgex(self):
        cmd = docker_compose_cmd()
        cmd.append('down')
        run_command(cmd)

        cmd = ['docker', 'volume', 'prune', '-f']
        run_command(cmd)

    def shutdown_edgex_with_compose_file(self, file_name):
        cmd = docker_compose_cmd()
        cmd.extend(['-f', file_name, 'down'])
        run_command(cmd)

        cmd = ['docker', 'volume', 'prune', '-f']
        run_command(cmd)

    def stop_edgex(self):
        cmd = docker_compose_cmd()
        cmd.append('stop')
        run_command(cmd)

    def dependecy_services_are_deployed(self, *args):
        dependencies = dict()
        for arg in args:
            dependencies[arg] = services[arg]

        # Deploy services (default: redis, consul )
        cmd = docker_compose_cmd()
        cmd.extend(['up', '-d', "redis"])
        run_command(cmd)

        cmd = docker_compose_cmd()
        cmd.extend(['up', '-d', "consul"])
        run_command(cmd)

        for k in dependencies:
            cmd = docker_compose_cmd()
            cmd.extend(['up', '-d', dependencies[k]["composeName"]])
            run_command(cmd)

        # Check services are started
        check_dependencies_services_startup(dependencies)

    def deploy_service(self, service):
        # Deploy service
        cmd = docker_compose_cmd()
        cmd.extend(['up', '-d', services[service]["composeName"]])
        run_command(cmd)

        # Check services are started
        logger.info("Check service " + service + " is startup...", also_console=True)
        check_service_startup(services[service])


def run_command(cmd):
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    for line in p.stdout:
        logger.info(line, also_console=True)

    p.wait()
    logger.info("exit " + str(p.returncode))
    if p.returncode != 0:
        msg = "Fail to execute cmd: " + " ".join(str(x) for x in cmd)
        logger.error(msg)
        raise Exception(msg)
    else:
        msg = "Success to execute cmd: " + " ".join(str(x) for x in cmd)
        logger.info(msg)


def docker_compose_cmd():
    cwd = str(os.getcwd())
    userhome = str(os.getenv("userhome"))
    return ["docker", "run", "--rm", "--env-file", "common.env",
            "-v", userhome + "/.docker/config.json:/root/.docker/config.json", 
            "-v", cwd + ":" + cwd, "-w", cwd,
            "-v", "/var/run/docker.sock:/var/run/docker.sock",
            get_docker_compose_image()]

# Not use in this branch
def get_env_file():
    if platform.machine() == "aarch32":
        return "arm.env"
    elif platform.machine() == "aarch64":
        return "arm64.env"
    elif platform.machine() == "x86_64":
        return "x86_64.env"
    else:
        msg = "Unknow platform machine: " + platform.machine()
        logger.error(msg)
        raise Exception(msg)

def get_docker_compose_image():
    try:
        # return str(os.environ["compose"])
        #arch = str(os.getenv("arch"))
        return str("iotechsys/dev-testing-compose:1.25.0")
    except KeyError:
        logger.error("Please set the environment variable: compose")
        sys.exit(1)


def check_dependencies_services_startup(dependencies):
    for s in dependencies:
        logger.info("Check service " + s + " is startup...", also_console=True)
        check_service_startup(dependencies[s])


def check_service_startup(d):
    retrytimes = int(os.environ["retryFetchStartupTimes"])
    waittime = int(os.environ["waitTime"])
    for i in range(retrytimes):
        logger.info("Ping localhost " + str(d["port"]) + d["url"] + " ... ", also_console=True)
        conn = http.client.HTTPConnection(host="localhost", port=d["port"])
        conn.request(method="GET", url=d["url"])
        try:
            r1 = conn.getresponse()
        except:
            time.sleep(waittime)
            continue
        logger.info(r1.status, also_console=True)
        if int(r1.status) == 200:
            logger.info("Service is startup.", also_console=True)
            return True
        else:
            time.sleep(waittime)
            continue
    return False
