from robot.api import logger
import subprocess

class EdgeX(object):
    
    def edgex_is_deployed(self):
        cmd = ['docker-compose', 'up', '-d']
        p = subprocess.Popen(cmd, stderr=subprocess.PIPE)
        for line in p.stderr:
            logger.info(line,also_console=True)
        p.wait()
        logger.info(p.returncode) 
        if (p.returncode != 0):
            logger.error("Failt to deploy EdgeX") 
            raise Exception("Failt to deploy EdgeX")

    def edgex_is_deployed_exclude_ruleengine(self):
        cmd = ['docker-compose', '-f', 'docker-compose-exclude-ruleengine.yml', 'up', '-d']
        p = subprocess.Popen(cmd, stderr=subprocess.PIPE)
        for line in p.stderr:
            logger.info(line,also_console=True)
        p.wait()
        logger.info(p.returncode) 
        if (p.returncode != 0):
            logger.error("Failt to deploy EdgeX exclude ruleengine") 
            raise Exception("Failt to deploy EdgeX exclude ruleengine")

    def shutdown_edgex(self):
        cmd = ['docker-compose', 'down']
        p = subprocess.Popen(cmd, stderr=subprocess.PIPE)
        for line in p.stderr:
            logger.info(line,also_console=True)
        p.wait()
        logger.info(p.returncode) 
        if (p.returncode != 0):
            logger.error("Failt to shoutdown EdgeX") 
            raise Exception("Failt to shoutdown EdgeX")

    def stop_edgex(self):
        cmd = ['docker-compose', 'stop']
        p = subprocess.Popen(cmd, stderr=subprocess.PIPE)
        for line in p.stderr:
            logger.info(line,also_console=True)
        p.wait()
        logger.info(p.returncode) 
        if (p.returncode != 0):
            logger.error("Failt to stop EdgeX") 
            raise Exception("Failt to stop EdgeX")
