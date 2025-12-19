"""Services for Virtual AC integration."""

from __future__ import annotations

import voluptuous as vol

from homeassistant.core import HomeAssistant, ServiceCall, callback
from homeassistant.helpers import config_validation as cv

from .const import DOMAIN

ATTR_CURRENT_TEMPERATURE = "current_temperature"
ATTR_CURRENT_HUMIDITY = "current_humidity"
ATTR_EXTERNAL_TEMPERATURE = "external_temperature"
ATTR_EXTERNAL_HUMIDITY = "external_humidity"

SERVICE_SET_STATE = "set_state"

SET_STATE_SCHEMA = vol.Schema(
    {
        vol.Required("entity_id"): cv.entity_id,
        vol.Optional(ATTR_CURRENT_TEMPERATURE): vol.Coerce(float),
        vol.Optional(ATTR_CURRENT_HUMIDITY): vol.Coerce(float),
        vol.Optional(ATTR_EXTERNAL_TEMPERATURE): vol.Coerce(float),
        vol.Optional(ATTR_EXTERNAL_HUMIDITY): vol.Coerce(float),
    }
)


@callback
def async_setup_services(hass: HomeAssistant) -> None:
    """Set up services for Virtual AC."""

    async def async_set_state(call: ServiceCall) -> None:
        """Set current temperature and/or humidity for testing."""
        entity_id = call.data["entity_id"]
        
        # Find the climate entity ID
        climate_entity_id = None
        if entity_id.startswith("climate."):
            climate_entity_id = entity_id
        else:
            # For sensor/select entities, find the associated climate entity
            entity_registry = hass.helpers.entity_registry.async_get(hass)
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
        entity_registry = hass.helpers.entity_registry.async_get(hass)
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

    hass.services.async_register(DOMAIN, SERVICE_SET_STATE, async_set_state, schema=SET_STATE_SCHEMA)
