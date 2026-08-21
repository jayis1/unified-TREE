from homeassistant.components.binary_sensor import BinarySensorEntity, BinarySensorDeviceClass
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN


async def async_setup_entry(hass, entry, async_add_entities):
    async_add_entities([TreeServerStatus(hass.data[DOMAIN][entry.entry_id])])


class TreeServerStatus(CoordinatorEntity, BinarySensorEntity):
    _attr_name = "Server"
    _attr_unique_id = "unified_tree_server"
    _attr_has_entity_name = True
    _attr_device_class = BinarySensorDeviceClass.CONNECTIVITY
    _attr_device_info = {"identifiers": {(DOMAIN, "server")}, "name": "unified TREE", "manufacturer": "jayis1", "model": "Node control plane"}

    @property
    def is_on(self):
        return self.coordinator.data["health"]["status"] == "ready"
