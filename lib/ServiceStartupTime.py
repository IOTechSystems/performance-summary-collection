from robot.api import logger
import traceback
import time
from datetime import datetime
import pytz

import docker
import re

client = docker.from_env()


regexMsg= r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}.\d+Z app=\S* \S*=\S* msg=\"Service started in: \d*.\d*m?s"
regexTime= r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}.\d{0,6}"

ruleengineRegexMsg = r"\[\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}.\d+\] boot - \d  INFO \[main\] --- Application: Started Application in \d+.\d+ seconds"
ruleengineRegexTime = r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}.\d{0,3}"

services = {
    "edgex-core-consul":{"regexMsg":regexMsg,"regexTime":regexTime},
    "edgex-mongo": {"regexMsg":regexMsg,"regexTime":regexTime},
    "edgex-core-data": {"regexMsg":regexMsg,"regexTime":regexTime},
    "edgex-core-metadata": {"regexMsg":regexMsg,"regexTime":regexTime},
    "edgex-core-command": {"regexMsg":regexMsg,"regexTime":regexTime},
    "edgex-support-logging": {"regexMsg":regexMsg,"regexTime":regexTime},
    "edgex-support-notifications": {"regexMsg":regexMsg,"regexTime":regexTime},
    "edgex-support-scheduler": {"regexMsg":regexMsg,"regexTime":regexTime},
    "edgex-export-client": {"regexMsg":regexMsg,"regexTime":regexTime},
    "edgex-export-distro": {"regexMsg":regexMsg,"regexTime":regexTime},
    "edgex-support-rulesengine": {"regexMsg":ruleengineRegexMsg,"regexTime":ruleengineRegexTime},
    "edgex-device-virtual": {"regexMsg":regexMsg,"regexTime":regexTime},
}

services_exclude_ruleengine = {
    "edgex-core-consul":{"regexMsg":regexMsg,"regexTime":regexTime},
    "edgex-mongo": {"regexMsg":regexMsg,"regexTime":regexTime},
    "edgex-core-data": {"regexMsg":regexMsg,"regexTime":regexTime},
    "edgex-core-metadata": {"regexMsg":regexMsg,"regexTime":regexTime},
    "edgex-core-command": {"regexMsg":regexMsg,"regexTime":regexTime},
    "edgex-support-logging": {"regexMsg":regexMsg,"regexTime":regexTime},
    "edgex-support-notifications": {"regexMsg":regexMsg,"regexTime":regexTime},
    "edgex-support-scheduler": {"regexMsg":regexMsg,"regexTime":regexTime},
    "edgex-export-client": {"regexMsg":regexMsg,"regexTime":regexTime},
    "edgex-export-distro": {"regexMsg":regexMsg,"regexTime":regexTime},
    "edgex-device-virtual": {"regexMsg":regexMsg,"regexTime":regexTime},
}



class ServiceStartupTime(object):
    result1 = {}
    result2 = {}

    def start_time_is_recorded(self):
        self.start_time = time.time()
        logger.info("\n --- Start time %s seconds ---" % self.start_time)

    def fetch_services_start_up_time_and_total_time(self):
        # wait for service start
        time.sleep( 25 )
        global result1
        result1 = get_services_start_up_time_and_total_time(self.start_time, services)

    def fetch_services_start_up_time_and_total_time_without_creating_containers(self):
        # wait for service start
        time.sleep( 25 )
        global result2
        result2 = get_services_start_up_time_and_total_time(self.start_time, services)    

    # Exclude ruleengine
    def fetch_services_start_up_time_and_total_time_exclude_ruleengine(self):
        # wait for service start
        time.sleep( 5 )
        global result1
        result1 = get_services_start_up_time_and_total_time(self.start_time, services_exclude_ruleengine)

    # Exclude ruleengine
    def fetch_services_start_up_time_and_total_time_without_creating_containers_exclude_ruleengine(self):
        # wait for service start
        time.sleep( 5 )
        global result2
        result2 = get_services_start_up_time_and_total_time(self.start_time, services_exclude_ruleengine)    


    def show_the_summary_table(self):
        show_the_summary_table_in_html(result1)

    def show_the_summary_table2(self):
        show_the_summary_table_in_html( result2)

    def show_the_comparison_table(self):
        html = """ 
        <table style="border: 1px solid black;white-space: initial;"> 
            <tr style="border: 1px solid black;">
                <th style="border: 1px solid black;">
                    Micro service			 	 
                </th>
                <th style="border: 1px solid black;">
                    Startup time(with creating)
                </th>
                <th style="border: 1px solid black;">
                    Startup time(without creating)
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
                    {} seconds
                </td>
                <td style="border: 1px solid black;">
                    {} seconds
                </td>
            </tr>
        """.format(
                k, result1[k], result2[k], 
            )

        html = html + "</table>"
        logger.info(html, html=True)

    def fetch_statup_time_from_service(self,service):
        time.sleep( 5 )
        startedTime = fetch_started_time_by_service(service)    

        startupTime = 0
        if(startedTime==0):
            logger.console('StartupTime: '+ str(startupTime))
        else:
            startupTime = startedTime - self.start_time
            logger.console('StartupTime: '+ str(startupTime))

def findTotalStartupTime(result):
    largestTime = 0
    for k in result:
        if largestTime < result[k]:
            largestTime = result[k]
    
    return largestTime

def get_services_start_up_time_and_total_time(start_time,containers):
    result = {}
    for k in containers:
        startedTime = fetch_started_time_by_service(k)
        if(startedTime==0):
            result[k] = 0
        else:
            startupTime = startedTime - start_time
            result[k] = startupTime

    totalStartupTime = findTotalStartupTime(result)
    result["Total startup time"] = totalStartupTime
    logger.info(result)
    return result


def fetch_started_time_by_service(service):
    containerName = service
    logger.info("Fetch the service: "+containerName,also_console=True)
    try:
        container = client.containers.get(containerName)
        msg = container.logs(until=int(time.time()))
    
        # level=INFO ts=2019-06-18T07:17:18.5245679Z app=edgex-core-data source=main.go:70 msg="Service started in: 120.62ms" 
        x = re.findall( services[containerName]["regexMsg"], str(msg))
        if (len(x)==0):
            return 0
        startedMsg = x[len(x)-1]

        logger.info("[Service started msg] "+startedMsg,also_console=True)
        # 2019-06-18T07:17:18.524567
        x = re.findall(services[containerName]["regexTime"], startedMsg)
        if (len(x)==0):
            return 0
        startedDateTime = x[len(x)-1]
        logger.info("startedDateTime is: "+startedDateTime,also_console=True)

        datePattern = "%Y-%m-%dT%H:%M:%S.%f"
        if "T" not in startedDateTime: 
            datePattern = "%Y-%m-%d %H:%M:%S.%f"
        dt = datetime.strptime(startedDateTime, datePattern).replace(tzinfo=pytz.UTC)

        startedTime = dt.timestamp()

        return startedTime
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
                Startup time
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
                {} seconds
            </td>
        </tr>
    """.format(
            k, result[k], 
        )

    html = html + "</table>"
    logger.info(html, html=True)