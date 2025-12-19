# Logo for Virtual AC Integration

This directory contains the logo for the Virtual AC integration.

## Files

- `logo.svg` - Source SVG logo file
- `logo.png` - PNG version (needs to be generated)

## Converting SVG to PNG

Home Assistant requires a `logo.png` file (256x256 pixels recommended). To convert the SVG to PNG:

### Option 1: Using Python (cairosvg)

```bash
pip install cairosvg
python ../../convert_logo.py
```

### Option 2: Using Inkscape

```bash
inkscape logo.svg --export-filename=logo.png --export-width=256 --export-height=256
```

### Option 3: Using ImageMagick

```bash
convert -background none -size 256x256 logo.svg logo.png
```

### Option 4: Online Converter

Use an online SVG to PNG converter like:
- https://cloudconvert.com/svg-to-png
- https://convertio.co/svg-png/

Set the output size to 256x256 pixels.

## Brand Repository (Optional)

For official branding in Home Assistant, you can also submit the logo to the [Home Assistant Brands repository](https://github.com/home-assistant/brands) under `custom_integrations/virtual_ac/`.
