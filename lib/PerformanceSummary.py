import ResourceUsage
import PingResponse
import AllServicesStartupAtOnce
import AllServicesStartupOneByOne
import StartupTimeHandler
from robot.api import logger


class PerformanceSummary(object):

    def show_reports(self):
        logger.info("Resource usage:")
        ResourceUsage.show_the_summary_table_in_html()

        logger.info("Startup time:")
        StartupTimeHandler.show_the_comparison_table_in_html(AllServicesStartupAtOnce.all_up_time,
                                                             AllServicesStartupAtOnce.all_up_time_without_recreate)
        logger.info("Startup time(exclude ruleengine):")
        StartupTimeHandler.show_the_comparison_table_in_html(AllServicesStartupAtOnce.all_up_time_exclude_ruleengine,
                                                             AllServicesStartupAtOnce.all_up_time_exclude_ruleengine_without_recreate)

        logger.info("Startup time(deploy one by one):")
        StartupTimeHandler.show_the_comparison_table_in_html(AllServicesStartupOneByOne.up_time,
                                                             AllServicesStartupOneByOne.up_time_without_recreate)

        logger.info("Ping API latency:")
        PingResponse.show_the_summary_table_in_html()
