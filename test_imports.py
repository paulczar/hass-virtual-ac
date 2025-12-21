#!/usr/bin/env python3
"""Test script to validate imports and basic syntax of the Virtual AC integration."""

import sys
from pathlib import Path

# Add the project root to the path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_imports():
    """Test that all modules can be imported."""
    print("Testing imports...")

    try:
        from custom_components.virtual_ac import const
        print("✓ const.py imported successfully")
    except Exception as e:
        print(f"✗ Failed to import const.py: {e}")
        return False

    try:
        from custom_components.virtual_ac import config_flow
        print("✓ config_flow.py imported successfully")

        # Test that classes exist
        assert hasattr(config_flow, 'VirtualACConfigFlow'), "VirtualACConfigFlow not found"
        assert hasattr(config_flow, 'VirtualACOptionsFlowHandler'), "VirtualACOptionsFlowHandler not found"
        print("✓ Config flow classes found")
    except Exception as e:
        print(f"✗ Failed to import config_flow.py: {e}")
        import traceback
        traceback.print_exc()
        return False

    try:
        from custom_components.virtual_ac import climate
        print("✓ climate.py imported successfully")
    except Exception as e:
        print(f"✗ Failed to import climate.py: {e}")
        return False

    try:
        from custom_components.virtual_ac import coordinator
        print("✓ coordinator.py imported successfully")
    except Exception as e:
        print(f"✗ Failed to import coordinator.py: {e}")
        return False

    try:
        from custom_components.virtual_ac import sensor
        print("✓ sensor.py imported successfully")
    except Exception as e:
        print(f"✗ Failed to import sensor.py: {e}")
        return False

    try:
        from custom_components.virtual_ac import select
        print("✓ select.py imported successfully")
    except Exception as e:
        print(f"✗ Failed to import select.py: {e}")
        return False

    try:
        from custom_components.virtual_ac import services
        print("✓ services.py imported successfully")
    except Exception as e:
        print(f"✗ Failed to import services.py: {e}")
        return False

    print("\nAll imports successful!")
    return True

if __name__ == "__main__":
    success = test_imports()
    sys.exit(0 if success else 1)
