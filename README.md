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
- **Temperature Precision**: Temperature precision (default: 0.1°C)

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

## Troubleshooting

### Entity not appearing
- Ensure the integration is properly installed in `custom_components`
- Restart Home Assistant
- Check the logs for errors

### Temperature not changing
- Check simulation mode (instant vs realistic)
- In realistic mode, wait for update interval
- Verify HVAC mode is not OFF

### Humidity not changing
- DRY mode has the most significant humidity change
- COOL mode has slight humidity decrease
- FAN_ONLY and OFF modes don't change humidity

## Support

For issues, feature requests, or questions:
- Open an issue on GitHub: https://github.com/pczarkow/haas-ac-simulator/issues

## License

Licensed under the Apache License, Version 2.0. See [LICENSE](LICENSE) for details.
