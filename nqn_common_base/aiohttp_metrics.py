import time
from prometheus_client import Histogram, Gauge
from aiohttp.web import Response
from .metrics import register_metric


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

    @register_metric("How long has the longest request been running", namespace=app_name)
    def request_max_time():
        if not buckets:
            return 0
        return time.time() - min(buckets)

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
