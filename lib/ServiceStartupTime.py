from robot.api import logger
import traceback
import time
from datetime import datetime
import pytz

import docker
import re

client = docker.from_env()

msgRegex = r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}.\d+Z app=\S* \S*=\S* msg=\"Service started in: \d*.\d*m?s"
startupDatetimeRegex = r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}.\d{0,6}"
binaryStartupTimeRegex = r"\d*.\d*m?s"

ruleengineRegexMsg = r"\[\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}.\d+\] boot - \d  INFO \[main\] --- Application: Started Application in \d+.\d+ seconds"
ruleengineRegexTime = r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}.\d{0,3}"
ruleengineRegexBinaryStartupTime = r"\d*.\d* seconds"

services = {
    "edgex-core-consul": {"msgRegex": msgRegex, "startupDatetimeRegex": startupDatetimeRegex,
                          "binaryStartupTimeRegex": binaryStartupTimeRegex},
    "edgex-mongo": {"msgRegex": msgRegex, "startupDatetimeRegex": startupDatetimeRegex,
                    "binaryStartupTimeRegex": binaryStartupTimeRegex},
    "edgex-core-data": {"msgRegex": msgRegex, "startupDatetimeRegex": startupDatetimeRegex,
                        "binaryStartupTimeRegex": binaryStartupTimeRegex},
    "edgex-core-metadata": {"msgRegex": msgRegex, "startupDatetimeRegex": startupDatetimeRegex,
                            "binaryStartupTimeRegex": binaryStartupTimeRegex},
    "edgex-core-command": {"msgRegex": msgRegex, "startupDatetimeRegex": startupDatetimeRegex,
                           "binaryStartupTimeRegex": binaryStartupTimeRegex},
    "edgex-support-logging": {"msgRegex": msgRegex, "startupDatetimeRegex": startupDatetimeRegex,
                              "binaryStartupTimeRegex": binaryStartupTimeRegex},
    "edgex-support-notifications": {"msgRegex": msgRegex, "startupDatetimeRegex": startupDatetimeRegex,
                                    "binaryStartupTimeRegex": binaryStartupTimeRegex},
    "edgex-support-scheduler": {"msgRegex": msgRegex, "startupDatetimeRegex": startupDatetimeRegex,
                                "binaryStartupTimeRegex": binaryStartupTimeRegex},
    "edgex-export-client": {"msgRegex": msgRegex, "startupDatetimeRegex": startupDatetimeRegex,
                            "binaryStartupTimeRegex": binaryStartupTimeRegex},
    "edgex-export-distro": {"msgRegex": msgRegex, "startupDatetimeRegex": startupDatetimeRegex,
                            "binaryStartupTimeRegex": binaryStartupTimeRegex},
    "edgex-support-rulesengine": {"msgRegex": ruleengineRegexMsg, "startupDatetimeRegex": ruleengineRegexTime,
                                  "binaryStartupTimeRegex": ruleengineRegexBinaryStartupTime},
    "edgex-device-virtual": {"msgRegex": msgRegex, "startupDatetimeRegex": startupDatetimeRegex,
                             "binaryStartupTimeRegex": binaryStartupTimeRegex},
}

services_exclude_ruleengine = {
    "edgex-core-consul": {"msgRegex": msgRegex, "startupDatetimeRegex": startupDatetimeRegex,
                          "binaryStartupTimeRegex": binaryStartupTimeRegex},
    "edgex-mongo": {"msgRegex": msgRegex, "startupDatetimeRegex": startupDatetimeRegex,
                    "binaryStartupTimeRegex": binaryStartupTimeRegex},
    "edgex-core-data": {"msgRegex": msgRegex, "startupDatetimeRegex": startupDatetimeRegex,
                        "binaryStartupTimeRegex": binaryStartupTimeRegex},
    "edgex-core-metadata": {"msgRegex": msgRegex, "startupDatetimeRegex": startupDatetimeRegex,
                            "binaryStartupTimeRegex": binaryStartupTimeRegex},
    "edgex-core-command": {"msgRegex": msgRegex, "startupDatetimeRegex": startupDatetimeRegex,
                           "binaryStartupTimeRegex": binaryStartupTimeRegex},
    "edgex-support-logging": {"msgRegex": msgRegex, "startupDatetimeRegex": startupDatetimeRegex,
                              "binaryStartupTimeRegex": binaryStartupTimeRegex},
    "edgex-support-notifications": {"msgRegex": msgRegex, "startupDatetimeRegex": startupDatetimeRegex,
                                    "binaryStartupTimeRegex": binaryStartupTimeRegex},
    "edgex-support-scheduler": {"msgRegex": msgRegex, "startupDatetimeRegex": startupDatetimeRegex,
                                "binaryStartupTimeRegex": binaryStartupTimeRegex},
    "edgex-export-client": {"msgRegex": msgRegex, "startupDatetimeRegex": startupDatetimeRegex,
                            "binaryStartupTimeRegex": binaryStartupTimeRegex},
    "edgex-export-distro": {"msgRegex": msgRegex, "startupDatetimeRegex": startupDatetimeRegex,
                            "binaryStartupTimeRegex": binaryStartupTimeRegex},
    "edgex-device-virtual": {"msgRegex": msgRegex, "startupDatetimeRegex": startupDatetimeRegex,
                             "binaryStartupTimeRegex": binaryStartupTimeRegex},
}


class ServiceStartupTime(object):
    result1 = {}
    result2 = {}

    def start_time_is_recorded(self):
        self.start_time = time.time()
        logger.info("\n --- Start time %s seconds ---" % self.start_time, also_console=True)

    def fetch_services_start_up_time_and_total_time(self):
        # wait for service start
        time.sleep(25)
        global result1
        result1 = get_services_start_up_time_and_total_time(self.start_time, services)

    def fetch_services_start_up_time_and_total_time_without_creating_containers(self):
        # wait for service start
        time.sleep(25)
        global result2
        result2 = get_services_start_up_time_and_total_time(self.start_time, services)

        # Exclude ruleengine

    def fetch_services_start_up_time_and_total_time_exclude_ruleengine(self):
        # wait for service start
        time.sleep(10)
        global result1
        result1 = get_services_start_up_time_and_total_time(self.start_time, services_exclude_ruleengine)

    # Exclude ruleengine
    def fetch_services_start_up_time_and_total_time_without_creating_containers_exclude_ruleengine(self):
        # wait for service start
        time.sleep(10)
        global result2
        result2 = get_services_start_up_time_and_total_time(self.start_time, services_exclude_ruleengine)

    def show_the_summary_table(self):
        show_the_summary_table_in_html(result1)

    def show_the_summary_table2(self):
        show_the_summary_table_in_html(result2)

    def show_the_comparison_table(self):
        html = """ 
        <table style="border: 1px solid black;white-space: initial;"> 
            <tr style="border: 1px solid black;">
                <th style="border: 1px solid black;">
                    Micro service			 	 
                </th>
                <th style="border: 1px solid black;">
                    Startup time(Binary)
                </th>
                <th style="border: 1px solid black;">
                    Startup time(Container+Binary)
                </th>
                <th style="border: 1px solid black;">
                    Startup time(Binary) <br/> without recreate container 
                </th>
                <th style="border: 1px solid black;">
                    Startup time(Container+Binary)<br/> without recreate container
                </th>
            </tr>
        """

        for k in result1:
            html = html + """ 
            <tr style="border: 1px solid black;">
                <td style="border: 1px solid black;">
                    {}			 	 
                </td>
                <td style="border: 1px solid black;">
                    {}
                </td>
                <td style="border: 1px solid black;">
                    {} seconds
                </td>
                <td style="border: 1px solid black;">
                    {}
                </td>
                <td style="border: 1px solid black;">
                    {} seconds
                </td>
            </tr>
        """.format(
                k, result1[k]["binaryStartupTime"], str(result1[k]["startupTime"]), result2[k]["binaryStartupTime"],
                str(result2[k]["startupTime"]),
            )

        html = html + "</table>"
        logger.info(html, html=True)

    def fetch_statup_time_from_service(self, service):
        time.sleep(5)
        startedTime = fetch_started_time_by_service(service)

        startupTime = 0
        if (startedTime == 0):
            logger.console('StartupTime: ' + str(startupTime))
        else:
            startupTime = startedTime - self.start_time
            logger.console('StartupTime: ' + str(startupTime))


def findTotalStartupTime(result):
    largestTime = 0
    for k in result:
        if largestTime < result[k]["startupTime"]:
            largestTime = result[k]["startupTime"]

    return str(largestTime)


def get_services_start_up_time_and_total_time(start_time, containers):
    result = {}
    for k in containers:
        res = fetch_started_time_by_service(k)

        result[k] = {}
        result[k]["binaryStartupTime"] = res["binaryStartupTime"]

        if not res["startupDateTime"]:
            result[k]["startupTime"] = 0
        else:
            startupDateTime = res["startupDateTime"]
            datePattern = "%Y-%m-%dT%H:%M:%S.%f"
            if "T" not in startupDateTime:
                datePattern = "%Y-%m-%d %H:%M:%S.%f"
            dt = datetime.strptime(startupDateTime, datePattern).replace(tzinfo=pytz.UTC)

            result[k]["startupTime"] = dt.timestamp() - start_time

    totalStartupTime = findTotalStartupTime(result)
    result["Total startup time"] = {}
    result["Total startup time"]["binaryStartupTime"] = ""
    result["Total startup time"]["startupTime"] = totalStartupTime

    return result


def fetch_started_time_by_service(service):
    response = {"startupDateTime": "", "binaryStartupTime": ""}
    containerName = service
    logger.info("Fetch the service: " + containerName, also_console=True)
    try:
        container = client.containers.get(containerName)
        msg = container.logs(until=int(time.time()))
        # level=INFO ts=2019-06-18T07:17:18.5245679Z app=edgex-core-data source=main.go:70 msg="Service started in: 120.62ms"
        x = re.findall(services[containerName]["msgRegex"], str(msg))
        if (len(x) == 0):
            return response
        startedMsg = x[len(x) - 1]

        logger.info("[Service started msg] " + startedMsg, also_console=True)
        # 2019-06-18T07:17:18.524567
        x = re.findall(services[containerName]["startupDatetimeRegex"], startedMsg)
        if (len(x) == 0):
            return response
        startupDateTime = x[len(x) - 1]
        response["startupDateTime"] = startupDateTime

        x = re.findall(services[containerName]["binaryStartupTimeRegex"], startedMsg)
        binaryStartupTime = x[len(x) - 1]
        response["binaryStartupTime"] = binaryStartupTime

        return response
    except docker.errors.NotFound as error:
        logger.console(error)
    except:
        logger.console(containerName + " fail to fetch started time by_service")
        traceback.print_exc()


def show_the_summary_table_in_html(result):
    html = """ 
    <table style="border: 1px solid black;white-space: initial;"> 
        <tr style="border: 1px solid black;">
            <th style="border: 1px solid black;">
                Micro service			 	 
            </th>
            <th style="border: 1px solid black;">
                Startup time(Binary)
            </th>
            <th style="border: 1px solid black;">
                Startup time(Container+Binary)
            </th>
        </tr>
    """

    for k in result:
        html = html + """ 
        <tr style="border: 1px solid black;">
            <td style="border: 1px solid black;">
                {}			 	 
            </td>
            <td style="border: 1px solid black;">
                {}
            </td>
            <td style="border: 1px solid black;">
                {} seconds
            </td>
        </tr>
    """.format(
            k, result[k]["binaryStartupTime"], str(result[k]["startupTime"]),
        )

    html = html + "</table>"
    logger.info(html, html=True)
