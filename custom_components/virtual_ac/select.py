"""Virtual AC Select Entities for Fan and Swing."""

from __future__ import annotations

from homeassistant.components.select import SelectEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_NAME
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import (
    DOMAIN,
    FAN_AUTO,
    FAN_HIGH,
    FAN_LOW,
    FAN_MEDIUM,
    SWING_OFF,
    SWING_ON,
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Virtual AC select platform."""
    device_name = entry.data.get(CONF_NAME, "Virtual AC")

    # Get coordinator to access climate entity
    coordinator = None
    if DOMAIN in hass.data and entry.entry_id in hass.data[DOMAIN]:
        coordinator = hass.data[DOMAIN][entry.entry_id].get("coordinator")

    entities = [
        VirtualACFanSelect(entry, device_name, coordinator),
        VirtualACSwingSelect(entry, device_name, coordinator),
    ]

    async_add_entities(entities)


class VirtualACBaseSelect(SelectEntity):
    """Base class for Virtual AC select entities."""

    _attr_has_entity_name = True

    def __init__(
        self,
        entry: ConfigEntry,
        device_name: str,
        coordinator,
    ) -> None:
        """Initialize the select entity."""
        self._entry = entry
        self._device_name = device_name
        self._coordinator = coordinator
        self._climate_entity = None

        # Device info
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, entry.entry_id)},
            name=device_name,
            manufacturer="Virtual AC",
            model="Virtual Air Conditioner",
            sw_version="1.0.0",
        )

    async def async_added_to_hass(self) -> None:
        """When entity is added to hass."""
        await super().async_added_to_hass()

        # Get initial state
        if state := self.hass.states.get(self._climate_entity_id):
            self._climate_entity = state
            self.async_write_ha_state()


class VirtualACFanSelect(VirtualACBaseSelect):
    """Fan speed select entity."""

    _attr_options = [FAN_AUTO, FAN_LOW, FAN_MEDIUM, FAN_HIGH]
    _attr_translation_key = "fan_mode"

    def __init__(
        self,
        entry: ConfigEntry,
        device_name: str,
        coordinator,
    ) -> None:
        """Initialize the fan select."""
        super().__init__(entry, device_name, coordinator)
        self._attr_unique_id = f"{entry.entry_id}_fan_mode"
        self.entity_id = f"select.{device_name.lower().replace(' ', '_')}_fan_mode"

    @property
    def current_option(self) -> str | None:
        """Return the current fan mode."""
        if self._climate_entity:
            return self._climate_entity.attributes.get("fan_mode")
        return FAN_AUTO

    async def async_select_option(self, option: str) -> None:
        """Change the fan mode."""
        # Call the climate entity's service
        await self.hass.services.async_call(
            "climate",
            "set_fan_mode",
            {
                "entity_id": self._climate_entity_id,
                "fan_mode": option,
            },
        )

    @callback
    def _handle_state_change(self, entity_id: str, old_state, new_state) -> None:
        """Handle climate entity state changes."""
        if new_state:
            self._climate_entity = new_state
            self.async_write_ha_state()

    async def async_added_to_hass(self) -> None:
        """When entity is added to hass."""
        await super().async_added_to_hass()

        # Listen for climate entity state changes
        self.async_on_remove(
            self.hass.helpers.event.async_track_state_change(
                self._climate_entity_id,
                self._handle_state_change,
            )
        )


class VirtualACSwingSelect(VirtualACBaseSelect):
    """Swing mode select entity."""

    _attr_options = [SWING_OFF, SWING_ON]
    _attr_translation_key = "swing_mode"

    def __init__(
        self,
        entry: ConfigEntry,
        device_name: str,
        coordinator,
    ) -> None:
        """Initialize the swing select."""
        super().__init__(entry, device_name, coordinator)
        self._attr_unique_id = f"{entry.entry_id}_swing_mode"
        self.entity_id = f"select.{device_name.lower().replace(' ', '_')}_swing_mode"

    @property
    def current_option(self) -> str | None:
        """Return the current swing mode."""
        if self._climate_entity:
            return self._climate_entity.attributes.get("swing_mode")
        return SWING_OFF

    async def async_select_option(self, option: str) -> None:
        """Change the swing mode."""
        # Call the climate entity's service
        await self.hass.services.async_call(
            "climate",
            "set_swing_mode",
            {
                "entity_id": self._climate_entity_id,
                "swing_mode": option,
            },
        )

    @callback
    def _handle_state_change(self, entity_id: str, old_state, new_state) -> None:
        """Handle climate entity state changes."""
        if new_state:
            self._climate_entity = new_state
            self.async_write_ha_state()

    async def async_added_to_hass(self) -> None:
        """When entity is added to hass."""
        await super().async_added_to_hass()

        # Listen for climate entity state changes
        self.async_on_remove(
            self.hass.helpers.event.async_track_state_change(
                self._climate_entity_id,
                self._handle_state_change,
            )
        )
