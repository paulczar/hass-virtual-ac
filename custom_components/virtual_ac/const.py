"""Constants for Virtual AC integration."""

DOMAIN = "virtual_ac"

# Configuration keys
CONF_INITIAL_TEMP = "initial_temp"
CONF_INITIAL_HUMIDITY = "initial_humidity"
CONF_TEMP_UNIT = "temp_unit"
CONF_MIN_TEMP = "min_temp"
CONF_MAX_TEMP = "max_temp"
CONF_PRECISION = "precision"
CONF_SIMULATION_MODE = "simulation_mode"
CONF_COOLING_RATE = "cooling_rate"
CONF_HEATING_RATE = "heating_rate"
CONF_DRY_HUMIDITY_RATE = "dry_humidity_rate"
CONF_AMBIENT_TEMP = "ambient_temp"
CONF_AMBIENT_HUMIDITY = "ambient_humidity"
CONF_AMBIENT_DRIFT_RATE = "ambient_drift_rate"
CONF_UPDATE_INTERVAL = "update_interval"

# Default values
DEFAULT_INITIAL_TEMP = 22.0
DEFAULT_INITIAL_HUMIDITY = 50.0
DEFAULT_TEMP_UNIT = "celsius"
DEFAULT_MIN_TEMP = 16.0
DEFAULT_MAX_TEMP = 30.0
DEFAULT_PRECISION = 0.5
DEFAULT_SIMULATION_MODE = "instant"
DEFAULT_COOLING_RATE = 0.5  # °C per minute
DEFAULT_HEATING_RATE = 0.5  # °C per minute
DEFAULT_DRY_HUMIDITY_RATE = 2.0  # % per minute
DEFAULT_AMBIENT_TEMP = 20.0
DEFAULT_AMBIENT_HUMIDITY = 60.0
DEFAULT_AMBIENT_DRIFT_RATE = 0.1  # °C per minute when OFF
DEFAULT_UPDATE_INTERVAL = 10  # seconds

# Simulation modes
SIMULATION_MODE_INSTANT = "instant"
SIMULATION_MODE_REALISTIC = "realistic"

# Preset modes
PRESET_ECO = "eco"
PRESET_COMFORT = "comfort"
PRESET_SLEEP = "sleep"
PRESET_AWAY = "away"

# Fan modes
FAN_AUTO = "auto"
FAN_LOW = "low"
FAN_MEDIUM = "medium"
FAN_HIGH = "high"

# Swing modes
SWING_OFF = "off"
SWING_ON = "on"
