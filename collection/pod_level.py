import urllib.request
import json
import pandas
import os
import time


def pod_level():
    namespaces_url = 'http://10.60.38.181:10001/api/v1/model/namespaces/'
# /api/v1/model/namespaces/: Returns a list of all available namespaces.

    with urllib.request.urlopen(namespaces_url) as data_namespaces:
        namespaces = json.load(data_namespaces)

        for namespace in namespaces:
            pods_url = namespaces_url + namespace + "/pods/"
# /api/v1/model/namespaces/{namespace-name}/pods/: Returns a list of all available pods under a given namespace.

            with urllib.request.urlopen(pods_url) as data_pods:
                pods = json.load(data_pods)

                for pod in pods:
                    metrics_url = pods_url + pod + '/metrics/'
# /api/v1/model/namespaces/{namespace-name}/pods/{pod-name}/metrics/: Returns a list of available pod-level metrics

                    with urllib.request.urlopen(metrics_url) as data_metrics:
                        d = {}
                        metrics = json.load(data_metrics)

                        for metric_name in metrics:
                            timestamps = []
                            values = []

                            end_time = time.time()
                            x = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(end_time - 150))
                            # y = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(end_time))
                            # metric_url = metrics_url + metric_name + '?start=' + x + '&end=' + y

                            metric_url = metrics_url + metric_name + '?start=' + x
# /api/v1/model/namespaces/{namespace-name}/pods/{pod-name}/metrics/{metric-name}?start=X&end=Y: Returns a set
# of (Timestamp, Value) pairs for the requested pod-level metric, within the time range specified by start and end.

                            with urllib.request.urlopen(metric_url) as statistics:
                                statistic = json.load(statistics)

                                for i in statistic['metrics']:
                                    timestamps += [i['timestamp']]
                                    values += [i['value']]

                            d[metric_name] = pandas.Series(values, index=timestamps)

                        df = pandas.DataFrame(d)
                    df.to_csv(namespace + '_' + pod + '.csv',mode='a',
                              header=not os.path.exists(namespace + '_' + pod + '.csv'))


while True:
    pod_level()
    time.sleep(150)
# Press control + c to stop the process
