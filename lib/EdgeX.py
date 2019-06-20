from robot.api import logger
import subprocess

class EdgeX(object):
    
    def pull_the_edgex_docker_images(self):
        cmd = ['docker-compose', 'pull']
        run_command(cmd)

    def edgex_is_deployed(self):
        cmd = ['docker-compose', 'up', '-d']
        run_command(cmd)

    def edgex_is_deployed_exclude_ruleengine(self):
        cmd = ['docker-compose', '-f', 'docker-compose-exclude-ruleengine.yml', 'up', '-d']
        run_command(cmd)

    def shutdown_edgex(self):
        cmd = ['docker-compose', 'down']
        run_command(cmd)
        cmd = ['docker', 'volume', 'prune', '-f']
        run_command(cmd)

    def stop_edgex(self):
        cmd = ['docker-compose', 'stop']
        run_command(cmd )

    def dependecy_services_are_deployed(self, *args):
        for arg in args:
            cmd = ['docker-compose', 'up', '-d', arg]
            run_command(cmd)

    def deploy_service(self, service):
        cmd = ['docker-compose', 'up', '-d', service]
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