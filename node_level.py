import urllib.request
import json
import pandas
import os
import time


def node_level():
    nodes_url = 'http://10.60.38.181:10001/api/v1/model/nodes/'
    # /api/v1/model/nodes/: Returns a list of all available nodes.

    with urllib.request.urlopen(nodes_url) as data_nodes:
        nodes = json.load(data_nodes)

        for node in nodes:

            metrics_url = nodes_url + node + "/metrics/"
            # /api/v1/model/nodes/{node-name}/metrics/: Returns a list of available node-level metrics.

            with urllib.request.urlopen(metrics_url) as data_metrics:
                d = {}

                metrics = json.load(data_metrics)

                for metric_name in metrics:
                    timestamps = []
                    values = []

                    end_time = time.time()
                    x = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(end_time-150))
                    # y = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(end_time))
                    # metric_url = metrics_url + metric_name + '?start=' + x + '&end=' + y

                    metric_url = metrics_url + metric_name + '?start=' + x
                    # /api/v1/model/nodes/{node-name}/metrics/{metric-name}?start=X&end=Y:
                    # Returns a set of (Timestamp, Value) pairs for the requested node-level metric,
                    # within the time range specified by start and end.

                    with urllib.request.urlopen(metric_url) as statistics:
                        statistic = json.load(statistics)

                        for i in statistic['metrics']:
                            timestamps += [i['timestamp']]
                            values += [i['value']]

                    d[metric_name] = pandas.Series(values, index=timestamps)

                df = pandas.DataFrame(d)
            df.to_csv(node + '.csv', mode='a', header=not os.path.exists(node + '.csv'))


while True:
    node_level()
    time.sleep(150)
# Press control + c to stop the process
