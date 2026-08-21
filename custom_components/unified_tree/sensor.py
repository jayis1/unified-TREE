from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN


async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([TreeNodeCount(coordinator), TreeDomainCount(coordinator)])


class TreeSensor(CoordinatorEntity, SensorEntity):
    _attr_has_entity_name = True
    _attr_device_info = {"identifiers": {(DOMAIN, "server")}, "name": "unified TREE", "manufacturer": "jayis1", "model": "Node control plane"}


class TreeNodeCount(TreeSensor):
    _attr_name = "Registered nodes"
    _attr_unique_id = "unified_tree_registered_nodes"
    _attr_icon = "mdi:family-tree"

    @property
    def native_value(self):
        return self.coordinator.data["summary"]["nodes"]


class TreeDomainCount(TreeSensor):
    _attr_name = "Domains"
    _attr_unique_id = "unified_tree_domains"
    _attr_icon = "mdi:shape"

    @property
    def native_value(self):
        return len(self.coordinator.data["summary"]["domains"])
