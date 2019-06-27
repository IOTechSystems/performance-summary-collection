from robot.api import logger
import subprocess
import os
import time
import platform
import sys
from dotenv import load_dotenv
import http.client

services = {
    "edgex-core-data": {"port": 48080, "url": "/api/v1/ping"},
    "edgex-core-metadata": {"port": 48081, "url": "/api/v1/ping"},
    "edgex-core-command": {"port": 48082, "url": "/api/v1/ping"},
    "edgex-support-logging": {"port": 48061, "url": "/api/v1/ping"},
    "edgex-support-notifications": {"port": 48060, "url": "/api/v1/ping"},
    "edgex-support-scheduler": {"port": 48085, "url": "/api/v1/ping"},
    "edgex-export-client": {"port": 48071, "url": "/api/v1/ping"},
    "edgex-export-distro": {"port": 48070, "url": "/api/v1/ping"},
    "edgex-support-rulesengine": {"port": 48075, "url": "/api/v1/ping"},
    "edgex-device-virtual": {"port": 49990, "url": "/api/v1/ping"},
}

services_exclude_ruleengine = {
    "edgex-core-data": {"port": 48080, "url": "/api/v1/ping"},
    "edgex-core-metadata": {"port": 48081, "url": "/api/v1/ping"},
    "edgex-core-command": {"port": 48082, "url": "/api/v1/ping"},
    "edgex-support-logging": {"port": 48061, "url": "/api/v1/ping"},
    "edgex-support-notifications": {"port": 48060, "url": "/api/v1/ping"},
    "edgex-support-scheduler": {"port": 48085, "url": "/api/v1/ping"},
    "edgex-export-client": {"port": 48071, "url": "/api/v1/ping"},
    "edgex-export-distro": {"port": 48070, "url": "/api/v1/ping"},
    "edgex-device-virtual": {"port": 49990, "url": "/api/v1/ping"},
}

class EdgeX(object):

    def __init__(self):
        load_dotenv(dotenv_path=get_env_file(), verbose=True)

    
    def pull_the_edgex_docker_images(self):
        cmd = docker_compose_cmd()
        cmd.append('pull')
        run_command(cmd)

    def edgex_is_deployed(self):
        cmd = docker_compose_cmd()
        cmd.extend(['up','-d'])
        run_command(cmd)

        check_services_starup()

    def edgex_is_deployed_exclude_ruleengine(self):
        cmd = docker_compose_cmd()
        cmd.extend(['-f', 'docker-compose-exclude-ruleengine.yml', 'up', '-d'])
        run_command(cmd)

        check_services_starup_exclude_ruleengine()

    def shutdown_edgex(self):
        cmd = docker_compose_cmd()
        cmd.append('down')
        run_command(cmd)

        cmd = ['docker', 'volume', 'prune', '-f']
        run_command(cmd)

    def stop_edgex(self):
        cmd = docker_compose_cmd()
        cmd.append('stop')
        run_command(cmd )

    def dependecy_services_are_deployed(self, *args):
        for arg in args:
            cmd = docker_compose_cmd()
            cmd.extend(['up', '-d', arg])
            run_command(cmd )

    def deploy_service(self, service):
        cmd = docker_compose_cmd()
        cmd.extend(['up', '-d', service])
        run_command(cmd)


def run_command(cmd):
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
        for line in p.stdout:
            logger.info(line,also_console=True)

        p.wait()
        logger.info("exit " + str(p.returncode)) 
        if (p.returncode != 0):
            msg = "Failt to execute cmd: "+ " ".join(str(x) for x in cmd)
            logger.error(msg) 
            raise Exception(msg)
        else:
            msg = "Success to execute cmd: "+ " ".join(str(x) for x in cmd)
            logger.info(msg) 


def docker_compose_cmd():
    cwd = str(os.getcwd())
    return ["docker", "run", "--rm",
            "--env-file", get_env_file(), "-e", "PWD=" + cwd,
            "-v", cwd + ":" + cwd, "-w", cwd, "-v",
            "/var/run/docker.sock:/var/run/docker.sock", docker_compose_image()]


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


def docker_compose_image():
    try:
        return str(os.environ["compose"])
    except KeyError:
        logger.error("Please set the environment variable: compose")
        sys.exit(1)


def check_services_starup():
    for s in services:
        logger.info("Check service " + s + " is startup...", also_console=True)
        ping(services[s])


def check_services_starup_exclude_ruleengine():
    for s in services_exclude_ruleengine:
        logger.info("Check service " + s + " is startup...", also_console=True)
        if not ping(services_exclude_ruleengine[s]):
            logger.info("Service " + s + " is unable to ping.", also_console=True)


def ping(d):
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
