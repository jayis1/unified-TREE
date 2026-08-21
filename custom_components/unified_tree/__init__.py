from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .api import UnifiedTreeApi
from .const import DOMAIN, PLATFORMS
from .coordinator import UnifiedTreeCoordinator


async def async_setup_entry(hass, entry):
    api = UnifiedTreeApi(async_get_clientsession(hass), entry.data["url"])
    coordinator = UnifiedTreeCoordinator(hass, api)
    await coordinator.async_config_entry_first_refresh()
    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = coordinator
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass, entry):
    unloaded = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unloaded:
        hass.data[DOMAIN].pop(entry.entry_id)
    return unloaded
