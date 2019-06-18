import unittest
import re
import time
from datetime import datetime
import pytz

class TestMathFunc(unittest.TestCase):

    def test_find(self):
        regexMsg = "\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}.\d+Z app=\S* \S*=\S* msg=\"Service started in: \d*.\d*ms"
        regexTime = "\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}.\d{6}"

        msg = """
            level=INFO ts=2019-06-18T07:17:18.5245679Z app=edgex-core-data source=main.go:70 msg="Service started in: 120.62ms  resolved..."\nlevel=Service started in" 
                level=INFO ts=2019-06-18T07:17:18.5245679Z app=edgex-core-data source=main.go:70 msg="Service started in: 120.62ms  resolved..."\nlevel=Service started in" 
        """
        x = re.findall(regexMsg, msg)
        print(x)
        startedMsg = x[len(x)-1]
        print(startedMsg)

        x = re.findall(regexTime, startedMsg)
        startedDateTime = x[len(x)-1]
        dt = datetime.strptime(startedDateTime, '%Y-%m-%dT%H:%M:%S.%f').replace(tzinfo=pytz.UTC)
        startedTimestamp = dt.timestamp()
        print(startedTimestamp)

if __name__ == '__main__':
    unittest.main()