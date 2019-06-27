import ResourceUsage
import PingResponse
import ServiceStartupTime
from robot.api import logger


class PerformanceSummary(object):

    def show_reports(self):
        logger.info("Resource usage:")
        ResourceUsage.show_the_summary_table_in_html()

        logger.info("Startup time:")
        ServiceStartupTime.show_the_comparison_table_in_html(ServiceStartupTime.result1, ServiceStartupTime.result2)
        logger.info("Startup time(exclude ruleengine):")
        ServiceStartupTime.show_the_comparison_table_in_html(ServiceStartupTime.result3, ServiceStartupTime.result4)

        logger.info("Ping API latency:")
        PingResponse.show_the_summary_table_in_html()
