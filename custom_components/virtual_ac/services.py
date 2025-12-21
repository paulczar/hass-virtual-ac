"""Services for Virtual AC integration."""

from __future__ import annotations

import logging
import voluptuous as vol

from homeassistant.core import HomeAssistant, ServiceCall, callback
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers import entity_registry as er

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

ATTR_CURRENT_TEMPERATURE = "current_temperature"
ATTR_CURRENT_HUMIDITY = "current_humidity"
ATTR_EXTERNAL_TEMPERATURE = "external_temperature"
ATTR_EXTERNAL_HUMIDITY = "external_humidity"
ATTR_CLIMATE_ENTITY = "climate_entity"
ATTR_WEATHER_ENTITY = "weather_entity"

SERVICE_SET_STATE = "set_state"
SERVICE_SYNC_FROM_ENTITIES = "sync_from_entities"

# Schema without entity_id - we handle it in code from target or data
SET_STATE_SCHEMA = vol.Schema(
    {
        vol.Optional(ATTR_CURRENT_TEMPERATURE): vol.Coerce(float),
        vol.Optional(ATTR_CURRENT_HUMIDITY): vol.Coerce(float),
        vol.Optional(ATTR_EXTERNAL_TEMPERATURE): vol.Coerce(float),
        vol.Optional(ATTR_EXTERNAL_HUMIDITY): vol.Coerce(float),
    },
    extra=vol.ALLOW_EXTRA,  # Allow entity_id and target to be passed
)


@callback
def async_setup_services(hass: HomeAssistant) -> None:
    """Set up services for Virtual AC."""

    async def async_set_state(call: ServiceCall) -> None:
        """Set current temperature and/or humidity for testing."""
        # Handle both target selector (UI/YAML) and direct entity_id
        entity_id = call.data.get("entity_id")
        if not entity_id:
            # Try to get from target (UI selector or YAML target:)
            if hasattr(call, "target") and call.target:
                entity_ids = call.target.entity_id
                if entity_ids:
                    entity_id = entity_ids[0] if isinstance(entity_ids, list) else entity_ids
            # Fallback: try from data target (for backwards compatibility)
            if not entity_id:
                target = call.data.get("target", {})
                entity_ids = target.get("entity_id", [])
                if entity_ids:
                    entity_id = entity_ids[0] if isinstance(entity_ids, list) else entity_ids
        if not entity_id:
            raise ValueError("entity_id is required. Provide it directly in data, via target selector, or in YAML target: section.")

        # Find the climate entity ID
        climate_entity_id = None
        if entity_id.startswith("climate."):
            climate_entity_id = entity_id
        else:
            # For sensor/select entities, find the associated climate entity
            entity_registry = er.async_get(hass)
            entity = entity_registry.async_get(entity_id)
            if entity:
                # Find climate entity with same config entry
                entry_id = entity.config_entry_id
                if entry_id in hass.data.get(DOMAIN, {}):
                    climate_entity = hass.data[DOMAIN][entry_id].get("climate_entity")
                    if climate_entity:
                        climate_entity_id = climate_entity.entity_id
            else:
                # Try to find by device name pattern
                for entry in hass.config_entries.async_entries(DOMAIN):
                    device_name = entry.data.get("name", "Virtual AC")
                    climate_id = f"climate.{device_name.lower().replace(' ', '_')}"
                    if hass.states.get(climate_id):
                        climate_entity_id = climate_id
                        break

        if climate_entity_id is None:
            raise ValueError(f"Could not find climate entity for {entity_id}")

        # Get the climate entity object
        entity_registry = er.async_get(hass)
        climate_entity_reg = entity_registry.async_get(climate_entity_id)
        if climate_entity_reg is None:
            raise ValueError(f"Climate entity {climate_entity_id} not in registry")

        entry_id = climate_entity_reg.config_entry_id

        if entry_id not in hass.data.get(DOMAIN, {}):
            raise ValueError(f"Config entry {entry_id} not found")

        climate_entity = hass.data[DOMAIN][entry_id].get("climate_entity")
        if climate_entity is None:
            raise ValueError(f"Climate entity object for {entry_id} not found")

        # Call the climate entity's method to update state
        await climate_entity.async_set_current_state(
            current_temperature=call.data.get(ATTR_CURRENT_TEMPERATURE),
            current_humidity=call.data.get(ATTR_CURRENT_HUMIDITY),
            external_temperature=call.data.get(ATTR_EXTERNAL_TEMPERATURE),
            external_humidity=call.data.get(ATTR_EXTERNAL_HUMIDITY),
        )

    async def async_sync_from_entities(call: ServiceCall) -> None:
        """Sync temperature and humidity from another climate entity and/or weather entity."""
        # Handle both target selector (UI/YAML) and direct entity_id
        entity_id = call.data.get("entity_id")
        _LOGGER.debug("Service call data: %s", call.data)
        _LOGGER.debug("Has target attr: %s", hasattr(call, "target"))

        if not entity_id:
            # Try to get from target (UI selector or YAML target:)
            if hasattr(call, "target") and call.target:
                _LOGGER.debug("call.target: %s", call.target)
                _LOGGER.debug("call.target.entity_id: %s", getattr(call.target, "entity_id", None))
                entity_ids = getattr(call.target, "entity_id", None)
                if entity_ids:
                    entity_id = entity_ids[0] if isinstance(entity_ids, list) else entity_ids
                    _LOGGER.debug("Extracted entity_id from call.target: %s", entity_id)
            # Fallback: try from data target (for backwards compatibility)
            if not entity_id:
                target = call.data.get("target", {})
                _LOGGER.debug("Trying data.target: %s", target)
                if target:
                    entity_ids = target.get("entity_id", [])
                    if entity_ids:
                        entity_id = entity_ids[0] if isinstance(entity_ids, list) else entity_ids
                        _LOGGER.debug("Extracted entity_id from data.target: %s", entity_id)

        _LOGGER.debug("Final entity_id: %s", entity_id)
        if not entity_id:
            raise ValueError("entity_id is required. Provide it directly in data, via target selector, or in YAML target: section.")

        # Find the climate entity ID
        climate_entity_id = None
        if entity_id.startswith("climate."):
            climate_entity_id = entity_id
        else:
            # For sensor/select entities, find the associated climate entity
            entity_registry = er.async_get(hass)
            entity = entity_registry.async_get(entity_id)
            if entity:
                # Find climate entity with same config entry
                entry_id = entity.config_entry_id
                if entry_id in hass.data.get(DOMAIN, {}):
                    climate_entity = hass.data[DOMAIN][entry_id].get("climate_entity")
                    if climate_entity:
                        climate_entity_id = climate_entity.entity_id
            else:
                # Try to find by device name pattern
                for entry in hass.config_entries.async_entries(DOMAIN):
                    device_name = entry.data.get("name", "Virtual AC")
                    climate_id = f"climate.{device_name.lower().replace(' ', '_')}"
                    if hass.states.get(climate_id):
                        climate_entity_id = climate_id
                        break

        if climate_entity_id is None:
            raise ValueError(f"Could not find climate entity for {entity_id}")

        # Get the climate entity object
        entity_registry = er.async_get(hass)
        climate_entity_reg = entity_registry.async_get(climate_entity_id)
        if climate_entity_reg is None:
            raise ValueError(f"Climate entity {climate_entity_id} not in registry")

        entry_id = climate_entity_reg.config_entry_id

        if entry_id not in hass.data.get(DOMAIN, {}):
            raise ValueError(f"Config entry {entry_id} not found")

        climate_entity = hass.data[DOMAIN][entry_id].get("climate_entity")
        if climate_entity is None:
            raise ValueError(f"Climate entity object for {entry_id} not found")

        # Read from source climate entity if provided
        source_climate_id = call.data.get(ATTR_CLIMATE_ENTITY)
        source_weather_id = call.data.get(ATTR_WEATHER_ENTITY)

        current_temp = None
        current_humidity = None
        external_temp = None
        external_humidity = None

        # Read from climate entity
        if source_climate_id:
            climate_state = hass.states.get(source_climate_id)
            if climate_state is None:
                _LOGGER.warning("Climate entity %s not found", source_climate_id)
            else:
                # Get temperature from climate entity
                temp_attr = climate_state.attributes.get("current_temperature")
                if temp_attr is not None:
                    try:
                        current_temp = float(temp_attr)
                        _LOGGER.debug("Read temperature %.2f from climate entity %s", current_temp, source_climate_id)
                    except (ValueError, TypeError):
                        _LOGGER.warning("Could not parse temperature from %s: %s", source_climate_id, temp_attr)

                # Get humidity from climate entity
                humidity_attr = climate_state.attributes.get("current_humidity")
                if humidity_attr is None:
                    # Try alternative attribute names
                    humidity_attr = climate_state.attributes.get("humidity")
                if humidity_attr is not None:
                    try:
                        current_humidity = float(humidity_attr)
                        _LOGGER.debug("Read humidity %.2f from climate entity %s", current_humidity, source_climate_id)
                    except (ValueError, TypeError):
                        _LOGGER.warning("Could not parse humidity from %s: %s", source_climate_id, humidity_attr)

        # Read from weather entity
        if source_weather_id:
            weather_state = hass.states.get(source_weather_id)
            if weather_state is None:
                _LOGGER.warning("Weather entity %s not found", source_weather_id)
            else:
                # Get temperature from weather entity
                temp_attr = weather_state.attributes.get("temperature")
                if temp_attr is None:
                    # Try alternative attribute names
                    temp_attr = weather_state.state
                if temp_attr is not None:
                    try:
                        external_temp = float(temp_attr)
                        _LOGGER.debug("Read temperature %.2f from weather entity %s", external_temp, source_weather_id)
                    except (ValueError, TypeError):
                        _LOGGER.warning("Could not parse temperature from %s: %s", source_weather_id, temp_attr)

                # Get humidity from weather entity
                humidity_attr = weather_state.attributes.get("humidity")
                if humidity_attr is not None:
                    try:
                        external_humidity = float(humidity_attr)
                        _LOGGER.debug("Read humidity %.2f from weather entity %s", external_humidity, source_weather_id)
                    except (ValueError, TypeError):
                        _LOGGER.warning("Could not parse humidity from %s: %s", source_weather_id, humidity_attr)

        # Update the virtual AC with the read values
        if current_temp is not None or current_humidity is not None or external_temp is not None or external_humidity is not None:
            await climate_entity.async_set_current_state(
                current_temperature=current_temp,
                current_humidity=current_humidity,
                external_temperature=external_temp,
                external_humidity=external_humidity,
            )
            _LOGGER.info(
                "Synced Virtual AC %s: temp=%s, humidity=%s, external_temp=%s, external_humidity=%s",
                climate_entity_id,
                current_temp,
                current_humidity,
                external_temp,
                external_humidity,
            )
        else:
            _LOGGER.warning("No values were read from source entities. Please provide climate_entity and/or weather_entity.")

    # Schema without entity_id - we handle it in code from target or data
    SYNC_FROM_ENTITIES_SCHEMA = vol.Schema(
        {
            vol.Optional(ATTR_CLIMATE_ENTITY): cv.entity_id,
            vol.Optional(ATTR_WEATHER_ENTITY): cv.entity_id,
        },
        extra=vol.ALLOW_EXTRA,  # Allow entity_id and target to be passed
    )

    hass.services.async_register(DOMAIN, SERVICE_SET_STATE, async_set_state, schema=SET_STATE_SCHEMA)
    hass.services.async_register(DOMAIN, SERVICE_SYNC_FROM_ENTITIES, async_sync_from_entities, schema=SYNC_FROM_ENTITIES_SCHEMA)
