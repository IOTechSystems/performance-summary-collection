import time
from robot.api import logger
import docker

# client = docker.APIClient(base_url='unix://var/run/docker.sock')
client = docker.from_env()


class ServiceStartupTime(object):

    def __init__(self):
        self._result = ''
        self.start_time = time.time()

    def fetch_footprint_cpu_memory(self):
        logger.console("--- %s seconds ---" % (time.time() - self.start_time))
