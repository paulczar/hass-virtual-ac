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

    # Create entities
    entities = [
        VirtualACFanSelect(entry, device_name, coordinator),
        VirtualACSwingSelect(entry, device_name, coordinator),
    ]

    # Add entities to Home Assistant
    async_add_entities(entities, update_before_add=True)


class VirtualACBaseSelect(SelectEntity):
    """Base class for Virtual AC select entities."""

    _attr_has_entity_name = True
    _attr_name = None
    _attr_available = True

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
        self._climate_entity_id = f"climate.{device_name.lower().replace(' ', '_')}"

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

        # Get initial state and update
        self._update_state()

        # Write initial state to ensure entity is available
        self.async_write_ha_state()

        # Listen for climate entity state changes
        self.async_on_remove(
            self.hass.helpers.event.async_track_state_change(
                self._climate_entity_id,
                self._handle_state_change,
            )
        )

    @callback
    def _update_state(self) -> None:
        """Update state from climate entity."""
        if self.hass:
            if state := self.hass.states.get(self._climate_entity_id):
                self._climate_entity = state
                self.async_write_ha_state()
            else:
                # Climate entity not found yet, but still write state with default
                self.async_write_ha_state()

    @callback
    def _handle_state_change(self, entity_id: str, old_state, new_state) -> None:
        """Handle climate entity state changes."""
        if new_state:
            self._climate_entity = new_state
            self.async_write_ha_state()


class VirtualACFanSelect(VirtualACBaseSelect):
    """Fan speed select entity."""

    _attr_options = [FAN_AUTO, FAN_LOW, FAN_MEDIUM, FAN_HIGH]

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
        self._attr_name = "Fan Speed"

    @property
    def current_option(self) -> str:
        """Return the current fan mode."""
        # Try cached state first
        if self._climate_entity:
            fan_mode = self._climate_entity.attributes.get("fan_mode")
            if fan_mode in self._attr_options:
                return fan_mode

        # Try to get from hass state if not cached
        if self.hass:
            if state := self.hass.states.get(self._climate_entity_id):
                fan_mode = state.attributes.get("fan_mode")
                if fan_mode in self._attr_options:
                    return fan_mode

        # Default fallback
        return FAN_AUTO

    async def async_select_option(self, option: str) -> None:
        """Change the fan mode."""
        if option not in self._attr_options:
            raise ValueError(f"Invalid option: {option}")

        # Call the climate entity's service
        await self.hass.services.async_call(
            "climate",
            "set_fan_mode",
            {
                "entity_id": self._climate_entity_id,
                "fan_mode": option,
            },
        )

        # Update our state immediately
        self._update_state()



class VirtualACSwingSelect(VirtualACBaseSelect):
    """Swing mode select entity."""

    _attr_options = [SWING_OFF, SWING_ON]

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
        self._attr_name = "Swing Mode"

    @property
    def current_option(self) -> str:
        """Return the current swing mode."""
        # Try cached state first
        if self._climate_entity:
            swing_mode = self._climate_entity.attributes.get("swing_mode")
            if swing_mode in self._attr_options:
                return swing_mode

        # Try to get from hass state if not cached
        if self.hass:
            if state := self.hass.states.get(self._climate_entity_id):
                swing_mode = state.attributes.get("swing_mode")
                if swing_mode in self._attr_options:
                    return swing_mode

        # Default fallback
        return SWING_OFF

    async def async_select_option(self, option: str) -> None:
        """Change the swing mode."""
        if option not in self._attr_options:
            raise ValueError(f"Invalid option: {option}")

        # Call the climate entity's service
        await self.hass.services.async_call(
            "climate",
            "set_swing_mode",
            {
                "entity_id": self._climate_entity_id,
                "swing_mode": option,
            },
        )

        # Update our state immediately
        self._update_state()
