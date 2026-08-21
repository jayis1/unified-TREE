from datetime import timedelta

from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DOMAIN


class UnifiedTreeCoordinator(DataUpdateCoordinator):
    def __init__(self, hass, api):
        super().__init__(hass, logger=__import__("logging").getLogger(__name__), name=DOMAIN, update_interval=timedelta(seconds=30))
        self.api = api

    async def _async_update_data(self):
        try:
            health = await self.api.health()
            summary = await self.api.summary()
            return {"health": health, "summary": summary}
        except Exception as error:
            raise UpdateFailed(f"Unable to update unified TREE: {error}") from error
