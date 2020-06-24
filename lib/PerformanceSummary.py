import ResourceUsage
import PingResponse
import AllServicesStartupAtOnce
import AllServicesStartupOneByOne
import StartupTimeHandler
import EventExportedTime


class PerformanceSummary(object):

    def show_reports(self):
        ResourceUsage.show_the_summary_table_in_html()

        StartupTimeHandler.show_the_comparison_table_in_html("Startup time:", AllServicesStartupAtOnce.all_up_time,
                                                             AllServicesStartupAtOnce.all_up_time_without_recreate)

        StartupTimeHandler.show_the_comparison_table_in_html("Startup time(deploy one by one):",
                                                             AllServicesStartupOneByOne.up_time,
                                                             AllServicesStartupOneByOne.up_time_without_recreate)

        PingResponse.show_the_summary_table_in_html()

        EventExportedTime.show_the_summary_table_in_html("EXPORT_CLIENT")
        EventExportedTime.show_the_summary_table_in_html("APP-SERVICE-MQTT-EXPORT")
