import voluptuous as vol

from homeassistant import config_entries
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .api import UnifiedTreeApi
from .const import DEFAULT_URL, DOMAIN


class UnifiedTreeConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}
        if user_input:
            url = user_input["url"].rstrip("/")
            try:
                health = await UnifiedTreeApi(async_get_clientsession(self.hass), url).health()
                if health.get("service") != "unified TREE":
                    raise ValueError("unexpected service")
            except Exception:
                errors["base"] = "cannot_connect"
            else:
                await self.async_set_unique_id(url)
                self._abort_if_unique_id_configured()
                return self.async_create_entry(title="unified TREE", data={"url": url})
        return self.async_show_form(step_id="user", data_schema=vol.Schema({vol.Required("url", default=DEFAULT_URL): str}), errors=errors)
