"""Config flow for Virtual AC integration."""

from __future__ import annotations

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import HomeAssistant, callback
from homeassistant.data_entry_flow import FlowResult
from homeassistant.const import CONF_NAME

from .const import (
    DOMAIN,
    CONF_INITIAL_TEMP,
    CONF_INITIAL_HUMIDITY,
    CONF_TEMP_UNIT,
    CONF_MIN_TEMP,
    CONF_MAX_TEMP,
    CONF_PRECISION,
    CONF_SIMULATION_MODE,
    CONF_COOLING_RATE,
    CONF_HEATING_RATE,
    CONF_DRY_HUMIDITY_RATE,
    CONF_AMBIENT_TEMP,
    CONF_AMBIENT_HUMIDITY,
    CONF_AMBIENT_DRIFT_RATE,
    CONF_UPDATE_INTERVAL,
    DEFAULT_INITIAL_TEMP,
    DEFAULT_INITIAL_HUMIDITY,
    DEFAULT_TEMP_UNIT,
    DEFAULT_MIN_TEMP,
    DEFAULT_MAX_TEMP,
    DEFAULT_PRECISION,
    DEFAULT_SIMULATION_MODE,
    DEFAULT_COOLING_RATE,
    DEFAULT_HEATING_RATE,
    DEFAULT_DRY_HUMIDITY_RATE,
    DEFAULT_AMBIENT_TEMP,
    DEFAULT_AMBIENT_HUMIDITY,
    DEFAULT_AMBIENT_DRIFT_RATE,
    DEFAULT_UPDATE_INTERVAL,
    SIMULATION_MODE_INSTANT,
    SIMULATION_MODE_REALISTIC,
)


STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_NAME): str,
        vol.Optional(CONF_INITIAL_TEMP, default=DEFAULT_INITIAL_TEMP): vol.Coerce(float),
        vol.Optional(CONF_INITIAL_HUMIDITY, default=DEFAULT_INITIAL_HUMIDITY): vol.Coerce(float),
        vol.Optional(CONF_AMBIENT_TEMP, default=DEFAULT_AMBIENT_TEMP): vol.Coerce(float),
        vol.Optional(CONF_AMBIENT_HUMIDITY, default=DEFAULT_AMBIENT_HUMIDITY): vol.Coerce(float),
        vol.Optional(CONF_TEMP_UNIT, default=DEFAULT_TEMP_UNIT): vol.In(["celsius", "fahrenheit"]),
        vol.Optional(CONF_MIN_TEMP, default=DEFAULT_MIN_TEMP): vol.Coerce(float),
        vol.Optional(CONF_MAX_TEMP, default=DEFAULT_MAX_TEMP): vol.Coerce(float),
        vol.Optional(CONF_PRECISION, default=DEFAULT_PRECISION): vol.Coerce(float),
    }
)

STEP_ADVANCED_DATA_SCHEMA = vol.Schema(
    {
        vol.Optional(CONF_SIMULATION_MODE, default=DEFAULT_SIMULATION_MODE): vol.In(
            [SIMULATION_MODE_INSTANT, SIMULATION_MODE_REALISTIC]
        ),
        vol.Optional(CONF_COOLING_RATE, default=DEFAULT_COOLING_RATE): vol.Coerce(float),
        vol.Optional(CONF_HEATING_RATE, default=DEFAULT_HEATING_RATE): vol.Coerce(float),
        vol.Optional(CONF_DRY_HUMIDITY_RATE, default=DEFAULT_DRY_HUMIDITY_RATE): vol.Coerce(float),
        vol.Optional(CONF_AMBIENT_DRIFT_RATE, default=DEFAULT_AMBIENT_DRIFT_RATE): vol.Coerce(float),
        vol.Optional(CONF_UPDATE_INTERVAL, default=DEFAULT_UPDATE_INTERVAL): vol.Coerce(int),
    }
)


class VirtualACConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Virtual AC."""

    VERSION = 1

    def __init__(self) -> None:
        """Initialize the config flow."""
        self.user_input: dict = {}

    async def async_step_user(
        self, user_input: dict | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}

        if user_input is not None:
            # Validate input
            if not user_input.get(CONF_NAME):
                errors[CONF_NAME] = "invalid_name"
            elif not 0 <= user_input.get(CONF_INITIAL_HUMIDITY, 0) <= 100:
                errors[CONF_INITIAL_HUMIDITY] = "invalid_humidity"
            elif not 0 <= user_input.get(CONF_AMBIENT_HUMIDITY, 0) <= 100:
                errors[CONF_AMBIENT_HUMIDITY] = "invalid_humidity"
            elif user_input.get(CONF_MIN_TEMP, 0) >= user_input.get(CONF_MAX_TEMP, 100):
                errors["base"] = "invalid_temp"
            else:
                self.user_input = user_input
                return await self.async_step_advanced()

        return self.async_show_form(
            step_id="user",
            data_schema=STEP_USER_DATA_SCHEMA,
            errors=errors,
        )

    async def async_step_advanced(
        self, user_input: dict | None = None
    ) -> FlowResult:
        """Handle the advanced configuration step."""
        if user_input is not None:
            # Merge user input with advanced settings
            config = {**self.user_input, **user_input}

            # Create unique ID based on name
            await self.async_set_unique_id(config[CONF_NAME])
            self._abort_if_unique_id_configured()

            return self.async_create_entry(title=config[CONF_NAME], data=config)

        return self.async_show_form(
            step_id="advanced",
            data_schema=STEP_ADVANCED_DATA_SCHEMA,
        )

    @staticmethod
    @callback
    def async_get_options_flow(
        config_entry: config_entries.ConfigEntry,
    ) -> VirtualACOptionsFlowHandler:
        """Get the options flow for this handler."""
        return VirtualACOptionsFlowHandler(config_entry)


class VirtualACOptionsFlowHandler(config_entries.OptionsFlow):
    """Handle options flow for Virtual AC."""

    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        """Initialize options flow."""
        self.config_entry = config_entry

    async def async_step_init(
        self, user_input: dict | None = None
    ) -> FlowResult:
        """Manage the options."""
        if user_input is not None:
            # Update config entry with new options
            return self.async_create_entry(title="", data=user_input)

        # Pre-fill with current values
        options_schema = vol.Schema(
            {
                vol.Optional(
                    CONF_SIMULATION_MODE,
                    default=self.config_entry.data.get(
                        CONF_SIMULATION_MODE, DEFAULT_SIMULATION_MODE
                    ),
                ): vol.In([SIMULATION_MODE_INSTANT, SIMULATION_MODE_REALISTIC]),
                vol.Optional(
                    CONF_COOLING_RATE,
                    default=self.config_entry.data.get(
                        CONF_COOLING_RATE, DEFAULT_COOLING_RATE
                    ),
                ): vol.Coerce(float),
                vol.Optional(
                    CONF_HEATING_RATE,
                    default=self.config_entry.data.get(
                        CONF_HEATING_RATE, DEFAULT_HEATING_RATE
                    ),
                ): vol.Coerce(float),
                vol.Optional(
                    CONF_DRY_HUMIDITY_RATE,
                    default=self.config_entry.data.get(
                        CONF_DRY_HUMIDITY_RATE, DEFAULT_DRY_HUMIDITY_RATE
                    ),
                ): vol.Coerce(float),
                vol.Optional(
                    CONF_AMBIENT_DRIFT_RATE,
                    default=self.config_entry.data.get(
                        CONF_AMBIENT_DRIFT_RATE, DEFAULT_AMBIENT_DRIFT_RATE
                    ),
                ): vol.Coerce(float),
                vol.Optional(
                    CONF_UPDATE_INTERVAL,
                    default=self.config_entry.data.get(
                        CONF_UPDATE_INTERVAL, DEFAULT_UPDATE_INTERVAL
                    ),
                ): vol.Coerce(int),
            }
        )

        return self.async_show_form(step_id="init", data_schema=options_schema)
