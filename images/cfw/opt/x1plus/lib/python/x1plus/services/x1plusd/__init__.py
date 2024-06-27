# Always invoke this with python3 -m x1plus.services.x1plusd.

import asyncio
import logging, logging.handlers
import x1plus.utils
from .dbus import *
from .settings import SettingsService
from .ota import OTAService
from .sshd import SSHService
from .httpd import HTTPService

logger = logging.getLogger(__name__)


async def main():
    logger.info("x1plusd is starting up")

    router = await get_dbus_router()
    settings = SettingsService(router=router)
    ota = OTAService(router=router, settings=settings)
    ssh = SSHService(settings=settings)
    httpd = HTTPService(router=router, settings=settings)

    asyncio.create_task(settings.task())
    asyncio.create_task(ota.task())
    asyncio.create_task(httpd.task())
    if settings.get("polar_cloud", True):
        from .polar_cloud import PolarPrintService
        polar_cloud = PolarPrintService(router=router, settings=settings)
        asyncio.create_task(polar_cloud.task())

    logger.info("x1plusd is running")
