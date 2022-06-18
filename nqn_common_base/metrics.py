from typing import Callable

from prometheus_client.core import GaugeMetricFamily, REGISTRY


def register_metric(description: str, *, namespace: str, name_override: str = None):
    def inner(func: Callable[[], float]):
        name = name_override or func.__name__

        class MetricsHandler:
            def collect(self):
                g = GaugeMetricFamily(f"{namespace}_{name}", description)
                g.add_metric([], func())
                yield g
        REGISTRY.register(MetricsHandler())
    return inner


def metric_pusher(name: str, description: str, *, namespace: str):
    metric = 0

    @register_metric(description, namespace=namespace, name_override=name)
    def inner():
        nonlocal metric
        rtn = metric
        metric = 0
        return rtn

    class Pusher:
        @staticmethod
        def push(value: float):
            nonlocal metric
            metric = value

        @staticmethod
        def inc(value: int = 1):
            nonlocal metric
            metric += value
    return Pusher
