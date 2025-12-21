# How to View Home Assistant Logs

When debugging a 500 error or other issues, you need to see the actual Python traceback. Here's how to access Home Assistant logs:

## Method 1: Via Home Assistant UI (Easiest)

1. **Go to Settings → System → Logs**
   - This shows recent log entries
   - Look for errors in red
   - Click on an error to see full details

2. **Enable Debug Logging for the Integration:**
   Add this to your `configuration.yaml`:
   ```yaml
   logger:
     default: info
     logs:
       custom_components.virtual_ac: debug
       homeassistant.components.config: debug
   ```
   Then restart Home Assistant.

3. **Download Full Logs:**
   - In Settings → System → Logs
   - Click the three dots menu (⋮) in the top right
   - Select "Download Full Logs"
   - This downloads a complete log file you can search through

## Method 2: Via SSH/Terminal (Most Detailed)

### Home Assistant OS (HAOS):
```bash
# SSH into your Home Assistant instance
# Then view the log file:
tail -f /config/home-assistant.log

# Or view last 100 lines:
tail -n 100 /config/home-assistant.log

# Or search for errors:
grep -i error /config/home-assistant.log | tail -20

# Or search for virtual_ac specifically:
grep -i virtual_ac /config/home-assistant.log | tail -50
```

### Docker Installation:
```bash
# View logs from the container:
docker logs -f homeassistant

# Or if using docker-compose:
docker-compose logs -f homeassistant

# View last 100 lines:
docker logs --tail 100 homeassistant
```

### Python venv Installation:
```bash
# Logs are usually in the directory where you run Home Assistant
# Or check ~/.homeassistant/home-assistant.log
tail -f ~/.homeassistant/home-assistant.log
```

## Method 3: Via Supervisor (HAOS)

1. Go to **Settings → Add-ons → SSH & Web Terminal** (or similar)
2. Open the terminal
3. Run: `tail -f /config/home-assistant.log`

## Method 4: Enable Debug Logging via UI (Home Assistant 2023.3+)

1. Go to **Settings → System → Logs**
2. Click the **"Download Full Logs"** button
3. Or use the logger integration UI if available

## Finding the 500 Error

When you trigger the 500 error (by clicking Configure on the device), look for:

1. **Python traceback** - Shows the exact line where the error occurred
2. **Error messages** containing:
   - `virtual_ac`
   - `config_flow`
   - `OptionsFlow`
   - `async_get_options_flow`
   - `async_step_init`

## Quick Debug Commands

```bash
# View live logs (follow mode)
tail -f /config/home-assistant.log

# Search for errors in last 50 lines
tail -n 50 /config/home-assistant.log | grep -i error

# Search for virtual_ac errors
grep -i "virtual_ac.*error" /config/home-assistant.log | tail -20

# Search for config flow errors
grep -i "config.*flow.*error" /config/home-assistant.log | tail -20

# View all errors from last hour
grep -i error /config/home-assistant.log | grep "$(date +%Y-%m-%d)" | tail -50
```

## After Enabling Debug Logging

After adding the logger configuration and restarting, when you trigger the 500 error, you should see detailed logs like:

```
ERROR custom_components.virtual_ac.config_flow - Error creating options flow handler: ...
ERROR custom_components.virtual_ac.config_flow - Error in options flow init step: ...
```

These will include the full Python traceback showing exactly what went wrong.

## Pro Tip

If you're still having trouble finding the logs:
1. Enable debug logging for `homeassistant.components.config` as well
2. This will show all config flow related errors
3. The error should appear immediately after you click "Configure"
