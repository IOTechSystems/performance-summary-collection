from robot.api import logger
import time
import copy
import StartupTimeHandler

# all_up_time : record startup time for deploy EdgeX at once
all_up_time = dict()
all_up_time_without_recreate = dict()
all_up_time_exclude_ruleengine = dict()
all_up_time_exclude_ruleengine_without_recreate = dict()


class AllServicesStartupAtOnce(object):

    def start_time_is_recorded(self):
        self.start_time = time.time()
        logger.info("\n --- Start time %s seconds ---" % self.start_time, also_console=True)

    def fetch_services_start_up_time_and_total_time(self):
        global all_up_time

        all_up_time = get_services_start_up_time_and_total_time(self.start_time, StartupTimeHandler.services)

    def fetch_services_start_up_time_and_total_time_without_creating_containers(self):
        global all_up_time_without_recreate

        all_up_time_without_recreate = get_services_start_up_time_and_total_time(self.start_time,
                                                                                 StartupTimeHandler.services)

    # Exclude ruleengine
    def fetch_services_start_up_time_and_total_time_exclude_ruleengine(self):
        global all_up_time_exclude_ruleengine

        services_exclude_ruleengine = copy.deepcopy(StartupTimeHandler.services)
        services_exclude_ruleengine.pop("support-rulesengine", None)  # exclude ruleengine

        all_up_time_exclude_ruleengine = get_services_start_up_time_and_total_time(self.start_time,
                                                                                   services_exclude_ruleengine)

    # Exclude ruleengine
    def fetch_services_start_up_time_and_total_time_without_creating_containers_exclude_ruleengine(self):
        global all_up_time_exclude_ruleengine_without_recreate

        services_exclude_ruleengine = copy.deepcopy(StartupTimeHandler.services)
        services_exclude_ruleengine.pop("support-rulesengine", None)  # exclude ruleengine

        all_up_time_exclude_ruleengine_without_recreate = get_services_start_up_time_and_total_time(self.start_time,
                                                                                                    services_exclude_ruleengine)

    def show_the_comparison_table(self):
        StartupTimeHandler.show_the_comparison_table_in_html("Startup time:", all_up_time, all_up_time_without_recreate)

    def show_the_comparison_table_for_exclude_ruleengine_case(self):
        StartupTimeHandler.show_the_comparison_table_in_html("Startup time(exclude ruleengine):",
                                                             all_up_time_exclude_ruleengine,
                                                             all_up_time_exclude_ruleengine_without_recreate)


def find_total_startup_time(result):
    largest_time = 0
    for k in result:
        if largest_time < result[k]["startupTime"]:
            largest_time = result[k]["startupTime"]

    return str(largest_time)


def get_services_start_up_time_and_total_time(start_time, containers):
    result = dict()
    for k in containers:
        StartupTimeHandler.fetch_service_start_up_time_by_container_name(containers[k], start_time, result)

    total_startup_time = find_total_startup_time(result)
    result["Total startup time"] = {}
    result["Total startup time"]["binaryStartupTime"] = ""
    result["Total startup time"]["startupTime"] = total_startup_time

    return result
