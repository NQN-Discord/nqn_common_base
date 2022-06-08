import time
from prometheus_client import Histogram, Gauge
from prometheus_client.core import GaugeMetricFamily, REGISTRY
from aiohttp.web import Response


def metrics_middleware(app_name: str = "aiohttp"):
    request_latency = Histogram(
        "request_latency",
        "Latency of requests",
        labelnames=["method", "endpoint", "status"],
        namespace=app_name
    )
    request_in_progress = Gauge(
        "request_in_progress",
        "Current number of requests",
        labelnames=["method", "endpoint"],
        namespace=app_name
    )
    buckets = set()

    class MetricsHandler:
        def __init__(self):
            REGISTRY.register(self)

        def collect(self):
            g = GaugeMetricFamily(
                f"{app_name}_request_max_time",
                "How long has the longest request been running"
            )
            g.add_metric([], self.max_time())
            yield g

        def max_time(self):
            if not buckets:
                return 0
            return time.time() - min(buckets)

    max_time = MetricsHandler()

    async def _outer(app, handler):
        async def _inner(request):
            request_in_progress.labels(method=request.method, endpoint=request.path).inc()

            start_time = time.time()

            buckets.add(start_time)
            response = Response(status=500)
            try:
                response = await handler(request)
            finally:
                buckets.discard(start_time)

                request_latency.labels(method=request.method, endpoint=request.path, status=response.status).observe(time.time() - start_time)
                request_in_progress.labels(method=request.method, endpoint=request.path).dec()
            return response
        return _inner
    return _outer
