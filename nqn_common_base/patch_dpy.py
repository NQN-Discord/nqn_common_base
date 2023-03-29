from discord.http import Ratelimit
from prometheus_client import Counter
import inspect


dpy_ratelimit_pauses = Counter(
    "dpy_requests_paused",
    "Requests paused due to rate limit",
    labelnames=["path"],
    namespace="ratelimit"
)


def patch_ratelimit():
    orig_aquire = Ratelimit.acquire

    async def acquire(self) -> None:
        if self.is_expired():
            self.reset()
        if self.remaining <= 0:
            previous_frame = inspect.currentframe().f_back
            while "route" not in previous_frame.f_locals:
                previous_frame = previous_frame.f_back
            route = previous_frame.f_locals["route"]
            dpy_ratelimit_pauses.labels(path=f"{route.method} {route.path}").inc()

        await orig_aquire(self)

    Ratelimit.acquire = acquire
