from robot.api import logger
import subprocess
import os
import platform
import sys
from dotenv import load_dotenv


# docker run --rm --env-file x86_64.env -v $PWD:$PWD -w $PWD -v /var/run/docker.sock:/var/run/docker.sock docker/compose:1.24.0 up -d


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

    def edgex_is_deployed_exclude_ruleengine(self):
        cmd = docker_compose_cmd()
        cmd.extend(['-f', 'docker-compose-exclude-ruleengine.yml', 'up', '-d'])
        run_command(cmd)

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
