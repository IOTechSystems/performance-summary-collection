import math
import http.client
import json
import time
from robot.api import logger

global result
result = {
    "devices": {},
    "total_average_exported_time": 0
}


class EventExportedTime(object):

    def mark_pushed_config_is_enable(self):
        conn = http.client.HTTPConnection(host="localhost", port=8500)
        conn.request(method="PUT", url="/v1/kv/edgex/core/1.0/edgex-export-distro/Writable/MarkPushed", body="true")
        try:
            r1 = conn.getresponse()
        except Exception as e:
            raise e
        if int(r1.status) == 200:
            logger.info("Enable MarkPushed.", also_console=True)
        else:
            raise Exception("Fail to enable MarkPushed.")

    def export_registration_is_added(self):
        conn = http.client.HTTPConnection(host="localhost", port=48071)

        requestBody = {
            "name": "nodered_integer_device",
            "addressable": {
                "name": "edgex_post_integer_data_to_mqtt",
                "protocol": "TCP",
                "address": "mqtt-broker",
                "port": 1883,
                "user": "", "password": "",
                "topic": "Random-Integer-Device-Topic",
                "publisher": "EdgeX"},
            "format": "JSON",
            "filter": {
                "deviceIdentifiers": ["Random-Integer-Device", "Random-UnsignedInteger-Device", "Random-Boolean-Device"]},
            "enable": True,
            "destination": "MQTT_TOPIC"
        }
        jsonBody = json.dumps(requestBody)
        conn.request(
            method="POST",
            url="/api/v1/registration",
            body=jsonBody,
            headers={'Content-type': 'application/json'})
        try:
            r1 = conn.getresponse()
        except Exception as e:
            raise e
        if int(r1.status) == 200:
            logger.info("Registration Added.", also_console=True)
        else:
            raise Exception("Fail to add registration. status:" + str(r1.status))

        # Sleep for device-virtual to generate the event
        time.sleep(100)

    def query_event(self):
        result["devices"]["Random-Integer-Device"] = get_device_events("Random-Integer-Device")
        result["devices"]["Random-Boolean-Device"] = get_device_events("Random-Boolean-Device")
        result["devices"]["Random-UnsignedInteger-Device"] = get_device_events("Random-UnsignedInteger-Device")

    def fetch_the_exported_time(self):
        events = []
        for device in result["devices"]:
            for event in result["devices"][device]:
                if "pushed" in event:
                    event["origin"] = get_origin_time(event["origin"])
                    event["exported"] = event["pushed"] - event["origin"]
                    events.append(event)
                else:
                    event["pushed"] = ""
                    event["exported"] = ""

        total_exported_time = 0
        for e in events:
            total_exported_time += e["exported"]

        if total_exported_time != 0:
            result["total_average_exported_time"] = total_exported_time / len(events)

    def show_the_summary_table(self):
        show_the_summary_table_in_html()


def show_the_summary_table_in_html():
    html = """ 
    <h3 style="margin:0px">Event exported time:</h3>
    <div style="margin:0px">Total average exported time: {} ms</div>
    <table style="border: 1px solid black;white-space: initial;"> 
        <tr style="border: 1px solid black;">
            <th style="border: 1px solid black;">
                Device			 	 
            </th>
            <th style="border: 1px solid black;" colspan="5">
                Event exported time ( pushed - origin )
            </th>
        </tr>
    """.format(result["total_average_exported_time"])

    for device in result["devices"]:
        html = html + """ 
        <tr style="border: 1px solid black;">
            <td style="border: 1px solid black;">
                {}			 	 
            </td>
            """.format(device)

        for event in result["devices"][device]:
            if event["exported"] == "":
                html = html + """<td style="border: 1px solid black;"> N/A </td>"""
            else:
                html = html + """ 
                        <td style="border: 1px solid black;">{} ms <br/>({} - {})</td>
                    """.format(event["exported"], event["pushed"], event["origin"])

        html = html + "</tr>"

    html = html + "</table>"
    logger.info(html, html=True)


def get_device_events(device):
    conn = http.client.HTTPConnection(host="localhost", port=48080)
    conn.request(method="GET", url="/api/v1/event/device/" + device + "/5")
    try:
        res = conn.getresponse()
    except Exception as e:
        raise e
    if int(res.status) == 200:
        responseBody = res.read().decode()
        return json.loads(responseBody)
    else:
        raise Exception("Fail to enable MarkPushed.")


# check origin time is nanoseconds level and convert to milliseconds level
def get_origin_time(origin_time):
    if origin_time > math.pow(10, 18):
        origin_time = int(origin_time / math.pow(10, 6))

    return origin_time
