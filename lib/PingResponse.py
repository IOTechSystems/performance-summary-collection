from robot.api import logger


class PingResponse(object):

    def __init__(self):
        global result
        result = {}

    def record_response(self, service, res):
        result[service] = res

    def show_the_summary_table(self):
        show_the_summary_table_in_html(result)


def show_the_summary_table_in_html(result):
    html = """ 
    <table style="border: 1px solid black;white-space: initial;"> 
        <tr style="border: 1px solid black;">
            <th style="border: 1px solid black;">
                Micro service			 	 
            </th>
            <th style="border: 1px solid black;">
                response body
            </th>
            <th style="border: 1px solid black;">
                response time
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
                {} ms
            </td>
        </tr>
    """.format(
            k, result[k]["body"], float(result[k]["seconds"]) * 1000
        )

    html = html + "</table>"
    logger.info(html, html=True)
