"""Virtual Air Conditioner Climate Entity."""

from __future__ import annotations

import asyncio
import logging
from datetime import datetime
from typing import Any

from homeassistant.components.climate import (
    ClimateEntity,
    ClimateEntityFeature,
    HVACMode,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import ATTR_TEMPERATURE, CONF_NAME, UnitOfTemperature
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.restore_state import RestoreEntity

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
    DEFAULT_AMBIENT_DRIFT_RATE,
    DEFAULT_UPDATE_INTERVAL,
    SIMULATION_MODE_INSTANT,
    SIMULATION_MODE_REALISTIC,
    PRESET_ECO,
    PRESET_COMFORT,
    PRESET_SLEEP,
    PRESET_AWAY,
    FAN_AUTO,
    FAN_LOW,
    FAN_MEDIUM,
    FAN_HIGH,
    SWING_OFF,
    SWING_ON,
)

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Virtual AC climate platform."""
    async_add_entities([VirtualACClimate(hass, entry)])


class VirtualACClimate(ClimateEntity, RestoreEntity):
    """Virtual Air Conditioner Climate Entity."""

    _attr_has_entity_name = True

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        """Initialize the Virtual AC climate entity."""
        self.hass = hass
        self._entry = entry
        self._config = entry.data

        # Device info
        device_name = entry.data.get(CONF_NAME, "Virtual AC")
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, entry.entry_id)},
            name=device_name,
            manufacturer="Virtual AC",
            model="Virtual Air Conditioner",
            sw_version="1.0.0",
        )

        # Unique ID and entity ID
        self._attr_unique_id = f"{entry.entry_id}_climate"
        self.entity_id = f"climate.{device_name.lower().replace(' ', '_')}"

        # HVAC modes
        self._attr_hvac_modes = [
            HVACMode.OFF,
            HVACMode.COOL,
            HVACMode.HEAT,
            HVACMode.DRY,
            HVACMode.FAN_ONLY,
            HVACMode.AUTO,
        ]

        # Supported features
        self._attr_supported_features = (
            ClimateEntityFeature.TARGET_TEMPERATURE
            | ClimateEntityFeature.FAN_MODE
            | ClimateEntityFeature.PRESET_MODE
            | ClimateEntityFeature.SWING_MODE
        )

        # Temperature settings
        temp_unit = self._config.get(CONF_TEMP_UNIT, DEFAULT_TEMP_UNIT)
        self._attr_temperature_unit = (
            UnitOfTemperature.CELSIUS if temp_unit == "celsius" else UnitOfTemperature.FAHRENHEIT
        )
        self._attr_min_temp = self._config.get(CONF_MIN_TEMP, DEFAULT_MIN_TEMP)
        self._attr_max_temp = self._config.get(CONF_MAX_TEMP, DEFAULT_MAX_TEMP)
        self._attr_target_temperature_step = self._config.get(CONF_PRECISION, DEFAULT_PRECISION)

        # Initial state
        self._attr_current_temperature = self._config.get(CONF_INITIAL_TEMP, DEFAULT_INITIAL_TEMP)
        self._attr_current_humidity = self._config.get(CONF_INITIAL_HUMIDITY, DEFAULT_INITIAL_HUMIDITY)
        self._attr_target_temperature = self._attr_current_temperature
        self._attr_hvac_mode = HVACMode.OFF

        # Preset modes
        self._attr_preset_modes = [PRESET_ECO, PRESET_COMFORT, PRESET_SLEEP, PRESET_AWAY]
        self._attr_preset_mode = PRESET_COMFORT

        # Fan modes
        self._attr_fan_modes = [FAN_AUTO, FAN_LOW, FAN_MEDIUM, FAN_HIGH]
        self._attr_fan_mode = FAN_AUTO

        # Swing modes
        self._attr_swing_modes = [SWING_OFF, SWING_ON]
        self._attr_swing_mode = SWING_OFF

        # Simulation settings
        self._simulation_mode = self._config.get(CONF_SIMULATION_MODE, DEFAULT_SIMULATION_MODE)
        self._cooling_rate = self._config.get(CONF_COOLING_RATE, DEFAULT_COOLING_RATE)
        self._heating_rate = self._config.get(CONF_HEATING_RATE, DEFAULT_HEATING_RATE)
        self._dry_humidity_rate = self._config.get(CONF_DRY_HUMIDITY_RATE, DEFAULT_DRY_HUMIDITY_RATE)
        self._ambient_temp = self._config.get(CONF_AMBIENT_TEMP, DEFAULT_AMBIENT_TEMP)
        self._ambient_drift_rate = self._config.get(CONF_AMBIENT_DRIFT_RATE, DEFAULT_AMBIENT_DRIFT_RATE)
        self._update_interval = self._config.get(CONF_UPDATE_INTERVAL, DEFAULT_UPDATE_INTERVAL)

        # Simulation state
        self._simulation_task: asyncio.Task | None = None
        self._last_update: datetime | None = None
        self._last_mode_change: datetime = datetime.now()

    async def async_added_to_hass(self) -> None:
        """When entity is added to hass."""
        await super().async_added_to_hass()

        # Restore state if available
        if (last_state := await self.async_get_last_state()) is not None:
            if last_state.attributes.get("temperature") is not None:
                self._attr_current_temperature = float(last_state.attributes["temperature"])
            if last_state.attributes.get("humidity") is not None:
                self._attr_current_humidity = float(last_state.attributes["humidity"])
            if last_state.attributes.get("target_temp_low") is not None:
                self._attr_target_temperature = float(last_state.attributes["target_temp_low"])

        # Start simulation if in realistic mode
        if self._simulation_mode == SIMULATION_MODE_REALISTIC:
            self._start_simulation()

    async def async_will_remove_from_hass(self) -> None:
        """When entity is removed from hass."""
        await super().async_will_remove_from_hass()
        self._stop_simulation()

    async def async_set_hvac_mode(self, hvac_mode: HVACMode) -> None:
        """Set HVAC mode."""
        self._attr_hvac_mode = hvac_mode
        self._last_mode_change = datetime.now()

        if self._simulation_mode == SIMULATION_MODE_INSTANT:
            # Instant mode: update immediately
            await self._apply_instant_mode(hvac_mode)
        else:
            # Realistic mode: start simulation if not running
            if self._simulation_task is None:
                self._start_simulation()

        self.async_write_ha_state()

    async def async_set_temperature(self, **kwargs: Any) -> None:
        """Set target temperature."""
        if (temperature := kwargs.get(ATTR_TEMPERATURE)) is not None:
            self._attr_target_temperature = temperature

            if self._simulation_mode == SIMULATION_MODE_INSTANT:
                # In instant mode, if we're in AUTO mode, update immediately
                if self._attr_hvac_mode == HVACMode.AUTO:
                    await self._apply_instant_mode(HVACMode.AUTO)

        self.async_write_ha_state()

    async def async_set_preset_mode(self, preset_mode: str) -> None:
        """Set preset mode."""
        self._attr_preset_mode = preset_mode

        # Adjust target temperature based on preset
        if preset_mode == PRESET_ECO:
            # Lower target by 2°C for eco mode
            self._attr_target_temperature = max(
                self._attr_min_temp,
                self._attr_target_temperature - 2.0,
            )
        elif preset_mode == PRESET_COMFORT:
            # Standard comfort temperature (no change)
            pass
        elif preset_mode == PRESET_SLEEP:
            # Lower target by 1°C for sleep mode
            self._attr_target_temperature = max(
                self._attr_min_temp,
                self._attr_target_temperature - 1.0,
            )
        elif preset_mode == PRESET_AWAY:
            # Lower target by 3°C for away mode
            self._attr_target_temperature = max(
                self._attr_min_temp,
                self._attr_target_temperature - 3.0,
            )

        self.async_write_ha_state()

    async def async_set_fan_mode(self, fan_mode: str) -> None:
        """Set fan mode."""
        self._attr_fan_mode = fan_mode
        self.async_write_ha_state()

    async def async_set_swing_mode(self, swing_mode: str) -> None:
        """Set swing mode."""
        self._attr_swing_mode = swing_mode
        self.async_write_ha_state()

    async def _apply_instant_mode(self, hvac_mode: HVACMode) -> None:
        """Apply instant mode changes."""
        if hvac_mode == HVACMode.COOL:
            self._attr_current_temperature = self._attr_target_temperature
            # Slight humidity decrease
            self._attr_current_humidity = max(0, self._attr_current_humidity - 1.0)
        elif hvac_mode == HVACMode.HEAT:
            self._attr_current_temperature = self._attr_target_temperature
            # Slight humidity decrease
            self._attr_current_humidity = max(0, self._attr_current_humidity - 0.5)
        elif hvac_mode == HVACMode.DRY:
            # Slight cooling and significant humidity decrease
            self._attr_current_temperature = max(
                self._attr_min_temp,
                self._attr_current_temperature - 1.0,
            )
            self._attr_current_humidity = max(0, self._attr_current_humidity - 5.0)
        elif hvac_mode == HVACMode.FAN_ONLY:
            # No temperature change
            pass
        elif hvac_mode == HVACMode.AUTO:
            # Auto mode: determine if we need to heat or cool
            if self._attr_current_temperature < self._attr_target_temperature:
                self._attr_current_temperature = self._attr_target_temperature
            elif self._attr_current_temperature > self._attr_target_temperature:
                self._attr_current_temperature = self._attr_target_temperature
        elif hvac_mode == HVACMode.OFF:
            # Temperature drifts toward ambient
            pass

    def _start_simulation(self) -> None:
        """Start the simulation task."""
        if self._simulation_task is None or self._simulation_task.done():
            self._simulation_task = self.hass.async_create_task(self._simulation_loop())
            self._last_update = datetime.now()

    def _stop_simulation(self) -> None:
        """Stop the simulation task."""
        if self._simulation_task is not None and not self._simulation_task.done():
            self._simulation_task.cancel()
            self._simulation_task = None

    async def _simulation_loop(self) -> None:
        """Background task for realistic simulation."""
        while True:
            try:
                await asyncio.sleep(self._update_interval)
                await self._update_simulation()
            except asyncio.CancelledError:
                break
            except Exception as e:
                _LOGGER.error("Error in Virtual AC simulation loop: %s", e)
                break

    async def _update_simulation(self) -> None:
        """Update temperature and humidity based on current mode."""
        if self._last_update is None:
            self._last_update = datetime.now()
            return

        now = datetime.now()
        elapsed_minutes = (now - self._last_update).total_seconds() / 60.0
        self._last_update = now

        # Get fan speed multiplier
        fan_multiplier = self._get_fan_multiplier()

        # Update based on HVAC mode
        if self._attr_hvac_mode == HVACMode.COOL:
            await self._simulate_cooling(elapsed_minutes, fan_multiplier)
        elif self._attr_hvac_mode == HVACMode.HEAT:
            await self._simulate_heating(elapsed_minutes, fan_multiplier)
        elif self._attr_hvac_mode == HVACMode.DRY:
            await self._simulate_dry(elapsed_minutes, fan_multiplier)
        elif self._attr_hvac_mode == HVACMode.FAN_ONLY:
            # No temperature change, slight humidity drift
            pass
        elif self._attr_hvac_mode == HVACMode.AUTO:
            await self._simulate_auto(elapsed_minutes, fan_multiplier)
        elif self._attr_hvac_mode == HVACMode.OFF:
            await self._simulate_off(elapsed_minutes)

        # Ensure values stay within bounds
        self._attr_current_temperature = max(
            self._attr_min_temp,
            min(self._attr_max_temp, self._attr_current_temperature),
        )
        self._attr_current_humidity = max(0, min(100, self._attr_current_humidity))

        self.async_write_ha_state()

    def _get_fan_multiplier(self) -> float:
        """Get fan speed multiplier for change rate."""
        if self._attr_fan_mode == FAN_LOW:
            return 0.5
        elif self._attr_fan_mode == FAN_MEDIUM:
            return 1.0
        elif self._attr_fan_mode == FAN_HIGH:
            return 1.5
        else:  # AUTO
            return 1.0

    async def _simulate_cooling(self, elapsed_minutes: float, fan_multiplier: float) -> None:
        """Simulate cooling mode."""
        if self._attr_current_temperature > self._attr_target_temperature:
            change = self._cooling_rate * elapsed_minutes * fan_multiplier
            self._attr_current_temperature = max(
                self._attr_target_temperature,
                self._attr_current_temperature - change,
            )
            # Slight humidity decrease due to condensation
            self._attr_current_humidity = max(0, self._attr_current_humidity - 0.5 * elapsed_minutes)

    async def _simulate_heating(self, elapsed_minutes: float, fan_multiplier: float) -> None:
        """Simulate heating mode."""
        if self._attr_current_temperature < self._attr_target_temperature:
            change = self._heating_rate * elapsed_minutes * fan_multiplier
            self._attr_current_temperature = min(
                self._attr_target_temperature,
                self._attr_current_temperature + change,
            )
            # Slight humidity decrease
            self._attr_current_humidity = max(0, self._attr_current_humidity - 0.3 * elapsed_minutes)

    async def _simulate_dry(self, elapsed_minutes: float, fan_multiplier: float) -> None:
        """Simulate dry mode."""
        # Slight cooling (less than COOL mode)
        if self._attr_current_temperature > self._attr_min_temp:
            change = self._cooling_rate * 0.3 * elapsed_minutes * fan_multiplier
            self._attr_current_temperature = max(
                self._attr_min_temp,
                self._attr_current_temperature - change,
            )
        # Significant humidity decrease
        self._attr_current_humidity = max(
            0,
            self._attr_current_humidity - self._dry_humidity_rate * elapsed_minutes,
        )

    async def _simulate_auto(self, elapsed_minutes: float, fan_multiplier: float) -> None:
        """Simulate auto mode."""
        temp_diff = self._attr_current_temperature - self._attr_target_temperature
        tolerance = 0.5  # Temperature tolerance

        if temp_diff > tolerance:
            # Need to cool
            await self._simulate_cooling(elapsed_minutes, fan_multiplier)
        elif temp_diff < -tolerance:
            # Need to heat
            await self._simulate_heating(elapsed_minutes, fan_multiplier)
        # Otherwise, maintain current temperature

    async def _simulate_off(self, elapsed_minutes: float) -> None:
        """Simulate off mode - drift toward ambient."""
        if self._attr_current_temperature < self._ambient_temp:
            # Drift up toward ambient
            change = self._ambient_drift_rate * elapsed_minutes
            self._attr_current_temperature = min(
                self._ambient_temp,
                self._attr_current_temperature + change,
            )
        elif self._attr_current_temperature > self._ambient_temp:
            # Drift down toward ambient
            change = self._ambient_drift_rate * elapsed_minutes
            self._attr_current_temperature = max(
                self._ambient_temp,
                self._attr_current_temperature - change,
            )

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return extra state attributes."""
        return {
            "humidity": self._attr_current_humidity,
            "simulation_mode": self._simulation_mode,
            "fan_mode": self._attr_fan_mode,
            "swing_mode": self._attr_swing_mode,
            "preset_mode": self._attr_preset_mode,
            "cooling_rate": self._cooling_rate,
            "heating_rate": self._heating_rate,
            "ambient_temperature": self._ambient_temp,
            "target_temperature": self._attr_target_temperature,
            "temperature_difference": round(
                self._attr_current_temperature - self._attr_target_temperature, 2
            ),
        }
