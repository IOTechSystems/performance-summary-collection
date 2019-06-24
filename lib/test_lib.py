import re
import unittest
from datetime import datetime

import pytz


class TestMathFunc(unittest.TestCase):

    def test_find(self):
        regexMsg = r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}.\d+Z app=\S* \S*=\S* msg=\"Service started in: \d*.\d*m?s"
        regexTime = r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}.\d{0,6}"
        regexTime2 = r"\d*.\d*m?s"

        msg = """
            level=INFO ts=2019-06-18T07:17:18.5245679Z app=edgex-core-data source=main.go:70 msg="Service started in: 120.62ms  resolved..."\nlevel=Service started in" 
            level=INFO ts=2019-06-18T07:17:18.5245679Z app=edgex-core-data source=main.go:70 msg="Service started in: 120.62ms  resolved..."\nlevel=Service started in" 
            level=INFO ts=2019-06-19T08:30:25.093438Z app=edgex-support-logging source=main.go:53 msg="Starting edgex-support-logging 1.0.0"
            [2019-06-19 08:50:25.925] boot - 7  WARN [main] --- URLConfigurationSource: No URLs will be polled as dynamic configuration sources.
            [2019-06-19 08:50:25.925] boot - 7  INFO [main] --- URLConfigurationSource: To enable URLs as dynamic configuration sources, define System property archaius.configurationSource.additionalUrls or make config.properties available on classpath.
            [2019-06-19 08:50:26.276] boot - 7  INFO [pool-2-thread-1] --- HeartBeat: Support Rules Engine data heart beat
            [2019-06-19 08:50:26.412] boot - 7  INFO [main] --- Application: Started Application in 16.357 seconds (JVM running for 17.754)
            This is the Support Rules Engine Microservice.
            [2019-06-19 08:50:26.511] boot - 7  INFO [main] --- ZeroMQEventSubscriber: Watching for new exported Event messages...
        """
        x = re.findall(regexMsg, msg)
        print("")
        print("1. Matched groups: " + str(x))
        startedMsg = x[len(x) - 1]
        print("2. Latest msg: " + str(startedMsg))

        x = re.findall(regexTime, startedMsg)
        startedDateTime = x[len(x) - 1]
        print("3. Startup datetime: " + str(startedDateTime))

        dt = datetime.strptime(startedDateTime, '%Y-%m-%dT%H:%M:%S.%f').replace(tzinfo=pytz.UTC)
        startedTimestamp = dt.timestamp()
        print("4. Startup time" + str(startedTimestamp))

        x = re.findall(regexTime2, startedMsg)
        spendTime = x[len(x) - 1]
        print("5. Spend time: " + str(spendTime))

    def test_find2(self):
        regexMsg = r"\[\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}.\d+\] boot - \d  INFO \[main\] --- Application: Started Application in \d+.\d+ seconds"
        regexTime = r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}.\d{0,3}"
        regexTime2 = r"\d*.\d* seconds"

        msg = """
            level=INFO ts=2019-06-18T07:17:18.5245679Z app=edgex-core-data source=main.go:70 msg="Service started in: 120.62ms  resolved..."\nlevel=Service started in" 
            level=INFO ts=2019-06-18T07:17:18.5245679Z app=edgex-core-data source=main.go:70 msg="Service started in: 120.62ms  resolved..."\nlevel=Service started in" 
            level=INFO ts=2019-06-19T08:30:25.093438Z app=edgex-support-logging source=main.go:53 msg="Starting edgex-support-logging 1.0.0"
            [2019-06-19 08:50:25.925] boot - 7  WARN [main] --- URLConfigurationSource: No URLs will be polled as dynamic configuration sources.
            [2019-06-19 08:50:25.925] boot - 7  INFO [main] --- URLConfigurationSource: To enable URLs as dynamic configuration sources, define System property archaius.configurationSource.additionalUrls or make config.properties available on classpath.
            [2019-06-19 08:50:26.276] boot - 7  INFO [pool-2-thread-1] --- HeartBeat: Support Rules Engine data heart beat
            [2019-06-19 08:50:26.412] boot - 7  INFO [main] --- Application: Started Application in 16.357 seconds (JVM running for 17.754)
            This is the Support Rules Engine Microservice.
            [2019-06-19 08:50:26.511] boot - 7  INFO [main] --- ZeroMQEventSubscriber: Watching for new exported Event messages...
        """
        x = re.findall(regexMsg, msg)
        print("")
        print("1. Matched groups: " + str(x))
        startedMsg = x[len(x) - 1]
        print("2. Latest msg: " + str(startedMsg))

        x = re.findall(regexTime, startedMsg)
        startedDateTime = x[len(x) - 1]
        print("3. Startup datetime: " + str(startedDateTime))

        dt = datetime.strptime(startedDateTime, '%Y-%m-%d %H:%M:%S.%f').replace(tzinfo=pytz.UTC)
        startedTimestamp = dt.timestamp()
        print("4. Startup time: " + str(startedTimestamp))

        x = re.findall(regexTime2, startedMsg)
        spendTime = x[len(x) - 1]
        print("5. Spend time: " + str(spendTime))


if __name__ == '__main__':
    unittest.main()
