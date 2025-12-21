#!/bin/bash
# Setup script for development environment

set -e

echo "Setting up development environment for Virtual AC integration..."

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install development dependencies
echo "Installing development dependencies..."
pip install -r requirements-dev.txt

echo ""
echo "Development environment setup complete!"
echo ""
echo "To activate the virtual environment in the future, run:"
echo "  source venv/bin/activate"
echo ""
echo "To test imports, run:"
echo "  python3 -c 'from custom_components.virtual_ac.config_flow import VirtualACOptionsFlowHandler; print(\"Import successful\")'"
