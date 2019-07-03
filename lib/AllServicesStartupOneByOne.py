from robot.api import logger
import time
import StartupTimeHandler

# up_time : record startup time for deploy EdgeX one by one
up_time = dict()
up_time_without_recreate = dict()


class AllServicesStartupOneByOne(object):

    def start_time_is_recorded(self):
        self.start_time = time.time()
        logger.info("\n --- Start time %s seconds ---" % self.start_time, also_console=True)

    def fetch_startup_time_from_service(self, service):
        StartupTimeHandler.fetch_service_start_up_time_by_container_name(StartupTimeHandler.services[service],
                                                                         self.start_time, up_time)

    def fetch_startup_time_from_service_without_recreate(self, service):
        StartupTimeHandler.fetch_service_start_up_time_by_container_name(StartupTimeHandler.services[service],
                                                                         self.start_time, up_time_without_recreate)

    def show_the_comparison_table(self):
        StartupTimeHandler.show_the_comparison_table_in_html("Startup time(deploy one by one):", up_time,
                                                             up_time_without_recreate)
