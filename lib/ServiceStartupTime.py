from robot.api import logger
import traceback
import time
from datetime import datetime
import pytz
import os
import sys
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
        time.sleep(int(os.environ["waitTime"]))
        global result1
        result1 = get_services_start_up_time_and_total_time(self.start_time, services)

    def fetch_services_start_up_time_and_total_time_without_creating_containers(self):
        # wait for service start
        time.sleep(int(os.environ["waitTime"]))
        global result2
        result2 = get_services_start_up_time_and_total_time(self.start_time, services)

        # Exclude ruleengine

    def fetch_services_start_up_time_and_total_time_exclude_ruleengine(self):
        # wait for service start
        time.sleep(int(os.environ["waitTime"]))
        global result1
        result1 = get_services_start_up_time_and_total_time(self.start_time, services_exclude_ruleengine)

    # Exclude ruleengine
    def fetch_services_start_up_time_and_total_time_without_creating_containers_exclude_ruleengine(self):
        # wait for service start
        time.sleep(int(os.environ["waitTime"]))
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
        if startedTime == 0:
            logger.console('StartupTime: ' + str(startupTime))
        else:
            startupTime = startedTime - self.start_time
            logger.console('StartupTime: ' + str(startupTime))


def find_total_startup_time(result):
    largestTime = 0
    for k in result:
        if largestTime < result[k]["startupTime"]:
            largestTime = result[k]["startupTime"]

    return str(largestTime)


def get_services_start_up_time_and_total_time(start_time, containers):
    result = {}
    for k in containers:
        if k == "edgex-core-consul" or k == "edgex-mongo":
            logger.info("skip consul and mongo")
            result[k] = {}
            result[k]["binaryStartupTime"] = 0
            result[k]["startupTime"] = 0
            continue

        get_service_start_up_time_and_total_time(start_time, k, result)

    total_startup_time = find_total_startup_time(result)
    result["Total startup time"] = {}
    result["Total startup time"]["binaryStartupTime"] = ""
    result["Total startup time"]["startupTime"] = total_startup_time

    return result


def get_service_start_up_time_and_total_time(start_time, containerName, result):
    res = {}
    retrytimes = int(os.environ["retryFetchStartupTimes"])
    for i in range(retrytimes):
        try:
            res = fetch_started_time_by_service(containerName)
            break
        except docker.errors.NotFound as error:
            logger.error(error)
            res = {"startupDateTime": "", "binaryStartupTime": ""}
            break
        except Exception as e:
            logger.warn(e.args)
            if i == (retrytimes - 1):
                logger.warn("fail to fetch startup time from " + containerName)
                res = {"startupDateTime": "", "binaryStartupTime": ""}
                break
            # wait for retry
            logger.warn("Retry to fetch startup time from " + containerName)
            time.sleep(int(os.environ["waitTime"]))

    result[containerName] = {}
    result[containerName]["binaryStartupTime"] = res["binaryStartupTime"]

    if not res["startupDateTime"]:
        result[containerName]["startupTime"] = 0
    else:
        startupDateTime = res["startupDateTime"]
        datePattern = "%Y-%m-%dT%H:%M:%S.%f"
        if "T" not in startupDateTime:
            datePattern = "%Y-%m-%d %H:%M:%S.%f"
        dt = datetime.strptime(startupDateTime, datePattern).replace(tzinfo=pytz.UTC)

        result[containerName]["startupTime"] = dt.timestamp() - start_time


def fetch_started_time_by_service(service):
    response = {"startupDateTime": "", "binaryStartupTime": ""}
    containerName = service
    logger.info("Fetch the service: " + containerName, also_console=True)

    container = client.containers.get(containerName)
    msg = container.logs(until=int(time.time()))
    # level=INFO ts=2019-06-18T07:17:18.5245679Z app=edgex-core-data source=main.go:70 msg="Service started in: 120.62ms"
    x = re.findall(services[containerName]["msgRegex"], str(msg))
    if len(x) == 0:
        raise Exception("startup msg not found")
    startedMsg = x[len(x) - 1]

    logger.info("[Service started msg] " + startedMsg, also_console=True)
    # 2019-06-18T07:17:18.524567
    x = re.findall(services[containerName]["startupDatetimeRegex"], startedMsg)
    if len(x) == 0:
        raise Exception("startup msg not found")
    startupDateTime = x[len(x) - 1]
    response["startupDateTime"] = startupDateTime

    x = re.findall(services[containerName]["binaryStartupTimeRegex"], startedMsg)
    binaryStartupTime = x[len(x) - 1]
    response["binaryStartupTime"] = binaryStartupTime

    return response


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
