"""Coordinator for sharing state between climate and sensors."""

from __future__ import annotations

from homeassistant.config_entries import ConfigEntry


class VirtualACCoordinator:
    """Coordinator to share state between climate and sensors."""

    def __init__(self, entry: ConfigEntry) -> None:
        """Initialize coordinator."""
        self.entry = entry
        self._current_temperature: float | None = None
        self._current_humidity: float | None = None
        self._external_temperature: float | None = None
        self._external_humidity: float | None = None
        self._listeners: list[callable] = []

    @property
    def current_temperature(self) -> float | None:
        """Get current temperature."""
        return self._current_temperature

    @property
    def current_humidity(self) -> float | None:
        """Get current humidity."""
        return self._current_humidity

    @property
    def external_temperature(self) -> float | None:
        """Get external temperature."""
        return self._external_temperature

    @property
    def external_humidity(self) -> float | None:
        """Get external humidity."""
        return self._external_humidity

    def update_temperature(self, temperature: float) -> None:
        """Update temperature and notify listeners."""
        self._current_temperature = temperature
        self._notify_listeners()

    def update_humidity(self, humidity: float) -> None:
        """Update humidity and notify listeners."""
        self._current_humidity = humidity
        self._notify_listeners()

    def update_external_temperature(self, temperature: float) -> None:
        """Update external temperature and notify listeners."""
        self._external_temperature = temperature
        self._notify_listeners()

    def update_external_humidity(self, humidity: float) -> None:
        """Update external humidity and notify listeners."""
        self._external_humidity = humidity
        self._notify_listeners()

    def add_listener(self, listener: callable) -> None:
        """Add a listener for updates."""
        self._listeners.append(listener)

    def _notify_listeners(self) -> None:
        """Notify all listeners of updates."""
        for listener in self._listeners:
            listener()
