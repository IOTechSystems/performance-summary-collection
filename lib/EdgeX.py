from robot.api import logger
import subprocess
import os
import platform

# docker run --rm -v $PWD:$PWD -w $PWD -v /var/run/docker.sock:/var/run/docker.sock docker/compose:1.24.0 up -d

class EdgeX(object):
    
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
        logger.info(p.returncode) 
        if (p.returncode != 0):
            msg = "Failt to execute cmd: "+ " ".join(str(x) for x in cmd)
            logger.error(msg) 
            raise Exception(msg)
        else:
            msg = "Success to execute cmd: "+ " ".join(str(x) for x in cmd)
            logger.info(msg) 

def docker_compose_cmd():
    cwd = str(os.getcwd())
    return ["docker", "run", "--rm", "-v", cwd+":"+cwd, "-w",cwd, "-v", "/var/run/docker.sock:/var/run/docker.sock", docker_compose_file()]

def docker_compose_file():
    if "aarch64" not in platform.platform(): 
        return "docker/compose:1.24.0"
    else:
        return "iotech-services.jfrog.io/compose_arm64:1.25.0-rc1"