from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.const import CONF_HOST, EVENT_HOMEASSISTANT_STOP

from .coordinator import EvonicCoordinator
from .const import DOMAIN, BRAND, LOGGER


class EvonicEntity(CoordinatorEntity[EvonicCoordinator]):
    _attr_has_entity_name = True

    @property
    def device_info(self) -> DeviceInfo:
        return DeviceInfo(
            identifiers={(DOMAIN, self.coordinator.data.info.mac)},
            name=self.coordinator.data.info.ssdp,
            manufacturer=BRAND,
            model=self.coordinator.data.info.ssdp,
            sw_version=self.coordinator.data.info.buildData,
            configuration_url=f"http://{self.platform.config_entry.data[CONF_HOST]}"
        )
