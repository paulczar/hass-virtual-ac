"""Virtual AC Sensor Entities."""

from __future__ import annotations

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_NAME, PERCENTAGE, UnitOfTemperature
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import VirtualACCoordinator


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Virtual AC sensor platform."""
    # Get coordinator (should already exist from __init__.py)
    coordinator = None
    if DOMAIN in hass.data and entry.entry_id in hass.data[DOMAIN]:
        coordinator = hass.data[DOMAIN][entry.entry_id].get("coordinator")

    if coordinator is None:
        # Fallback: create coordinator if it doesn't exist
        coordinator = VirtualACCoordinator(entry)
        if DOMAIN not in hass.data:
            hass.data[DOMAIN] = {}
        if entry.entry_id not in hass.data[DOMAIN]:
            hass.data[DOMAIN][entry.entry_id] = {}
        hass.data[DOMAIN][entry.entry_id]["coordinator"] = coordinator

    # Create sensor entities
    device_name = entry.data.get(CONF_NAME, "Virtual AC")
    entities = [
        VirtualACIndoorTemperatureSensor(coordinator, entry, device_name),
        VirtualACIndoorHumiditySensor(coordinator, entry, device_name),
        VirtualACOutdoorTemperatureSensor(coordinator, entry, device_name),
        VirtualACOutdoorHumiditySensor(coordinator, entry, device_name),
    ]

    async_add_entities(entities)


class VirtualACBaseSensor(SensorEntity):
    """Base class for Virtual AC sensors."""

    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: VirtualACCoordinator,
        entry: ConfigEntry,
        device_name: str,
    ) -> None:
        """Initialize the sensor."""
        self.coordinator = coordinator
        self._entry = entry
        self._device_name = device_name

        # Device info
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, entry.entry_id)},
            name=device_name,
            manufacturer="Virtual AC",
            model="Virtual Air Conditioner",
            sw_version="1.0.0",
        )

        # Add listener for updates
        coordinator.add_listener(self._handle_coordinator_update)

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle coordinator update."""
        self.async_write_ha_state()

    async def async_added_to_hass(self) -> None:
        """When entity is added to hass."""
        await super().async_added_to_hass()
        # Initial update
        self._handle_coordinator_update()


class VirtualACIndoorTemperatureSensor(VirtualACBaseSensor):
    """Indoor temperature sensor for Virtual AC."""

    _attr_device_class = SensorDeviceClass.TEMPERATURE
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS

    def __init__(
        self,
        coordinator: VirtualACCoordinator,
        entry: ConfigEntry,
        device_name: str,
    ) -> None:
        """Initialize the indoor temperature sensor."""
        super().__init__(coordinator, entry, device_name)
        self._attr_unique_id = f"{entry.entry_id}_indoor_temperature"
        self.entity_id = f"sensor.{device_name.lower().replace(' ', '_')}_indoor_temperature"

    @property
    def name(self) -> str:
        """Return the name of the sensor."""
        return "Indoor"

    @property
    def native_value(self) -> float | None:
        """Return the current indoor temperature."""
        return self.coordinator.current_temperature


class VirtualACIndoorHumiditySensor(VirtualACBaseSensor):
    """Indoor humidity sensor for Virtual AC."""

    _attr_device_class = SensorDeviceClass.HUMIDITY
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_native_unit_of_measurement = PERCENTAGE

    def __init__(
        self,
        coordinator: VirtualACCoordinator,
        entry: ConfigEntry,
        device_name: str,
    ) -> None:
        """Initialize the indoor humidity sensor."""
        super().__init__(coordinator, entry, device_name)
        self._attr_unique_id = f"{entry.entry_id}_indoor_humidity"
        self.entity_id = f"sensor.{device_name.lower().replace(' ', '_')}_indoor_humidity"

    @property
    def name(self) -> str:
        """Return the name of the sensor."""
        return "Indoor Humidity"

    @property
    def native_value(self) -> float | None:
        """Return the current indoor humidity."""
        return self.coordinator.current_humidity


class VirtualACOutdoorTemperatureSensor(VirtualACBaseSensor):
    """Outdoor temperature sensor for Virtual AC."""

    _attr_device_class = SensorDeviceClass.TEMPERATURE
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS

    def __init__(
        self,
        coordinator: VirtualACCoordinator,
        entry: ConfigEntry,
        device_name: str,
    ) -> None:
        """Initialize the outdoor temperature sensor."""
        super().__init__(coordinator, entry, device_name)
        self._attr_unique_id = f"{entry.entry_id}_outdoor_temperature"
        self.entity_id = f"sensor.{device_name.lower().replace(' ', '_')}_outdoor_temperature"

    @property
    def name(self) -> str:
        """Return the name of the sensor."""
        return "Outdoor"

    @property
    def native_value(self) -> float | None:
        """Return the current outdoor temperature."""
        return self.coordinator.external_temperature


class VirtualACOutdoorHumiditySensor(VirtualACBaseSensor):
    """Outdoor humidity sensor for Virtual AC."""

    _attr_device_class = SensorDeviceClass.HUMIDITY
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_native_unit_of_measurement = PERCENTAGE

    def __init__(
        self,
        coordinator: VirtualACCoordinator,
        entry: ConfigEntry,
        device_name: str,
    ) -> None:
        """Initialize the outdoor humidity sensor."""
        super().__init__(coordinator, entry, device_name)
        self._attr_unique_id = f"{entry.entry_id}_outdoor_humidity"
        self.entity_id = f"sensor.{device_name.lower().replace(' ', '_')}_outdoor_humidity"

    @property
    def name(self) -> str:
        """Return the name of the sensor."""
        return "Outdoor Humidity"

    @property
    def native_value(self) -> float | None:
        """Return the current outdoor humidity."""
        return self.coordinator.external_humidity
