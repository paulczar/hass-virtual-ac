<div align="center">
  <img src="logo.png" alt="Virtual AC Home Assistant Logo" width="400"/>
</div>

# Virtual Air Conditioner for Home Assistant

A fully-featured virtual air conditioner integration for Home Assistant that simulates a smart AC unit with multiple HVAC modes. Perfect for testing Versatile Thermostat functionality without real hardware constraints.

## Features

- **Instant Response**: No real cycle times - state changes happen immediately (configurable)
- **Full Feature Support**: Supports all HVAC modes (heat, cool, dry, fan_only, auto, off)
- **Realistic Simulation**: Simulates temperature changes, humidity changes, and AC behavior
- **Configurable**: Adjustable parameters for different test scenarios
- **Safe Testing**: No risk of damaging real equipment or wasting energy
- **Integration Ready**: Works seamlessly as a backend for Versatile Thermostat

## Installation

### HACS (Recommended)

1. Open HACS in Home Assistant
2. Go to Integrations
3. Click the three dots in the top right corner
4. Select "Custom repositories"
5. Add this repository URL
6. Select "Integration" as the category
7. Click "Add"
8. Find "Virtual Air Conditioner" in the integrations list
9. Click "Download"
10. Restart Home Assistant

### Manual Installation

1. Copy the `custom_components/virtual_ac` folder to your Home Assistant `custom_components` directory
2. Restart Home Assistant
3. Go to Settings → Devices & Services → Add Integration
4. Search for "Virtual Air Conditioner"
5. Follow the setup wizard

## Configuration

### Basic Configuration

When adding the integration, you'll be prompted for:

- **Name**: Name for your virtual AC (e.g., "Living Room AC")
- **Initial Temperature**: Starting temperature (default: 22.0°C)
- **Initial Humidity**: Starting humidity percentage (default: 50%)
- **Temperature Unit**: Celsius or Fahrenheit (default: Celsius)
- **Minimum Temperature**: Minimum allowed temperature (default: 16.0°C)
- **Maximum Temperature**: Maximum allowed temperature (default: 30.0°C)
- **Temperature Precision**: Temperature precision (default: 0.5°C)

### Advanced Configuration

- **Simulation Mode**:
  - `instant`: State changes happen immediately (fast testing)
  - `realistic`: Simulates gradual temperature/humidity changes
- **Cooling Rate**: Temperature decrease rate in COOL mode (°C per minute, default: 0.5)
- **Heating Rate**: Temperature increase rate in HEAT mode (°C per minute, default: 0.5)
- **Dry Humidity Rate**: Humidity decrease rate in DRY mode (% per minute, default: 2.0)
- **Ambient Temperature**: Target temperature when OFF (default: 20.0°C)
- **Ambient Drift Rate**: Temperature drift rate when OFF (°C per minute, default: 0.1)
- **Update Interval**: Simulation update interval in seconds (default: 10)

### Adjusting Simulation Speed

You can customize the simulation speed by adjusting the rates in realistic mode. This allows you to speed up or slow down the simulation without needing a separate "fast" mode.

**Default Rates:**
- Cooling: 0.5°C per minute (1°C drop = 2 minutes)
- Heating: 0.5°C per minute (1°C rise = 2 minutes)
- Dry humidity: 2.0% per minute (1% drop = 30 seconds)

**Faster Simulation Examples:**
- **2x faster**: Set cooling/heating rate to `1.0` (1°C change = 1 minute)
- **5x faster**: Set cooling/heating rate to `2.5` (1°C change = 24 seconds)
- **10x faster**: Set cooling/heating rate to `5.0` (1°C change = 12 seconds)
- **Dry mode faster**: Set dry humidity rate to `10.0` (1% drop = 6 seconds)

**Slower Simulation Examples:**
- **2x slower**: Set cooling/heating rate to `0.25` (1°C change = 4 minutes)
- **5x slower**: Set cooling/heating rate to `0.1` (1°C change = 10 minutes)

**Fan Speed Multipliers:**
- **LOW**: 50% of base rate (slower)
- **MEDIUM/AUTO**: 100% of base rate (normal)
- **HIGH**: 150% of base rate (faster)

**Update Interval:**
- Smaller values (e.g., `5` seconds) = more frequent updates, smoother simulation
- Larger values (e.g., `30` seconds) = less frequent updates, less CPU usage

**Example: Fast Testing Setup**
```
Simulation Mode: realistic
Cooling Rate: 2.0 (°C/min)
Heating Rate: 2.0 (°C/min)
Dry Humidity Rate: 10.0 (%/min)
Update Interval: 5 (seconds)
```
This gives you 4x faster temperature changes and 5x faster humidity changes while still maintaining observable intermediate states.

## HVAC Modes

### OFF
- No operation
- Temperature drifts toward ambient temperature
- No humidity change

### COOL
- Cools room toward target temperature
- Decreases humidity slightly (condensation)
- Rate configurable via cooling_rate

### HEAT
- Heats room toward target temperature
- Decreases humidity slightly
- Rate configurable via heating_rate

### DRY
- Dehumidifies room
- Decreases humidity significantly
- Slight cooling (less than COOL mode)
- Perfect for testing Versatile Thermostat humidity control

### FAN_ONLY
- Air circulation only
- No temperature change
- No humidity change

### AUTO
- Automatically switches between heat/cool based on target temperature
- Maintains temperature within tolerance

## Preset Modes

- **ECO**: Energy-saving mode (lowers target by 2°C)
- **COMFORT**: Standard comfort mode (no change)
- **SLEEP**: Quiet, energy-efficient mode (lowers target by 1°C)
- **AWAY**: Minimal operation mode (lowers target by 3°C)

## Fan Modes

- **AUTO**: Automatic fan speed
- **LOW**: Low fan speed (50% change rate)
- **MEDIUM**: Medium fan speed (100% change rate)
- **HIGH**: High fan speed (150% change rate)

## Swing Mode

- **OFF**: No swing
- **ON**: Swing enabled (visual indicator only)

## Usage with Versatile Thermostat

1. Install and configure Virtual AC
2. Install Versatile Thermostat
3. In Versatile Thermostat configuration, select your Virtual AC entity
4. Configure Versatile Thermostat settings as desired
5. Test all features including:
   - DRY mode activation on high humidity
   - COOL mode priority over DRY
   - Temperature threshold behavior
   - Mode switching

## Testing Scenarios

### Scenario 1: Basic Mode Switching
- Switch between COOL, HEAT, DRY, OFF
- Verify state updates immediately (instant mode) or gradually (realistic mode)
- Verify temperature/humidity changes appropriately

### Scenario 2: Temperature Control
- Set target temperature
- Verify current temperature approaches target
- Test overshoot behavior in realistic mode

### Scenario 3: DRY Mode Humidity Control
- Set to DRY mode with high humidity
- Verify humidity decreases
- Verify temperature decreases slightly
- Test with Versatile Thermostat humidity control

### Scenario 4: Versatile Thermostat Integration
- Configure Versatile Thermostat to use Virtual AC
- Test all Versatile Thermostat features
- Verify DRY mode activation on high humidity
- Verify COOL mode priority over DRY
- Test temperature threshold behavior

### Scenario 5: Realistic vs Instant Mode
- Test in instant mode (fast testing)
- Test in realistic mode (more realistic behavior)
- Verify both work correctly

## State Attributes

The integration exposes the following state attributes:

- `humidity`: Current humidity percentage
- `simulation_mode`: Current simulation mode (instant/realistic)
- `fan_mode`: Current fan mode
- `swing_mode`: Current swing mode
- `preset_mode`: Current preset mode
- `cooling_rate`: Configured cooling rate
- `heating_rate`: Configured heating rate
- `ambient_temperature`: Ambient temperature setting
- `target_temperature`: Target temperature
- `temperature_difference`: Difference between current and target temperature

## Benefits

1. **Safe Testing**: No risk to real equipment
2. **Fast Testing**: Instant mode allows rapid test cycles
3. **Controlled Environment**: Predictable, repeatable behavior
4. **Full Feature Support**: Test all HVAC modes and features
5. **No Cycle Time Constraints**: Test immediately without waiting
6. **Cost Effective**: No energy costs for testing
7. **Reproducible**: Same conditions every time

## Debug Logging

The integration includes comprehensive debug logging to help troubleshoot simulation behavior. To enable debug logging:

### Enable Debug Logging

1. **Via Configuration File** (recommended):
   Add the following to your `configuration.yaml`:
   ```yaml
   logger:
     default: info
     logs:
       custom_components.virtual_ac: debug
   ```

2. **Via Developer Tools**:
   - Go to **Settings** → **Developer Tools** → **YAML**
   - Add the logger configuration above
   - Click **Restart** to apply changes

3. **Via UI** (Home Assistant 2023.3+):
   - Go to **Settings** → **System** → **Logs**
   - Click the three dots menu → **Download Full Logs**
   - Or use the logger integration UI if available

### What Gets Logged

When debug logging is enabled, you'll see detailed information about:

- **Initialization**: Entity setup with all configuration values
- **Simulation Loop**: Start/stop events and update cycles
- **Mode Changes**: HVAC mode transitions with before/after states
- **Temperature Changes**: Target temperature updates
- **Heating/Cooling**: Detailed temperature changes including:
  - Current and new temperature values
  - Target temperature
  - Change amount and rate
  - Elapsed time since last update
  - Fan speed multiplier
- **Auto Mode**: Decision logic (heating vs cooling needed)
- **OFF Mode**: Ambient temperature drift behavior
- **Update Cycles**: Summary of each simulation update cycle

### Example Log Output

```
DEBUG custom_components.virtual_ac.climate - Virtual AC initialized: name=Test AC, mode=off, simulation_mode=realistic, current_temp=22.00°C, target_temp=22.00°C, heating_rate=0.50°C/min, cooling_rate=0.50°C/min, update_interval=10s
DEBUG custom_components.virtual_ac.climate - Starting simulation loop: mode=heat, update_interval=10s, heating_rate=0.50°C/min, cooling_rate=0.50°C/min
DEBUG custom_components.virtual_ac.climate - HVAC mode changed: off -> heat (simulation_mode: realistic, current_temp: 22.00°C, target_temp: 36.00°C)
DEBUG custom_components.virtual_ac.climate - Target temperature changed: 22.00 -> 36.00°C (current: 22.00°C, mode: heat, simulation_mode: realistic)
DEBUG custom_components.virtual_ac.climate - Heating: 22.00 -> 22.08°C (target: 36.00°C, change: 0.0833°C, rate: 0.50°C/min, elapsed: 0.17 min, fan: 1.0)
DEBUG custom_components.virtual_ac.climate - Update cycle [heat]: temp 22.00->22.08°C (target: 36.00°C), humidity 50.0->49.9%, elapsed: 0.17 min, fan_mult: 1.0
```

### Viewing Logs

- **Via UI**: Settings → System → Logs
- **Via Terminal**: `tail -f ~/.homeassistant/home-assistant.log` (or your log location)
- **Via SSH Add-on**: Use the SSH add-on terminal

## Troubleshooting

### Entity not appearing
- Ensure the integration is properly installed in `custom_components`
- Restart Home Assistant
- Check the logs for errors

### Temperature not changing
- Check simulation mode (instant vs realistic)
- In realistic mode, wait for update interval
- Verify HVAC mode is not OFF
- **Enable debug logging** to see detailed simulation progress
- Check logs for simulation loop errors
- **Too slow?** Adjust rates in advanced settings (see "Adjusting Simulation Speed" section)

### Humidity not changing
- DRY mode has the most significant humidity change
- COOL mode has slight humidity decrease
- FAN_ONLY and OFF modes don't change humidity

## Support

For issues, feature requests, or questions:
- Open an issue on GitHub: https://github.com/pczarkow/haas-ac-simulator/issues

## License

Licensed under the Apache License, Version 2.0. See [LICENSE](LICENSE) for details.
