# L-System Generator

A powerful and interactive L-System generator that allows you to visualize, customize, and animate fractal systems using turtle graphics.

## Overview

This application provides a user-friendly interface for exploring Lindenmayer Systems (L-Systems), which are a mathematical formalism used to model the growth processes of plant development and create beautiful fractal patterns.

## Features

- **Interactive Drawing**: Visualize L-Systems in real-time
- **Predefined Systems**: Includes several classic fractals like Koch Curve, Sierpinski Triangle, Dragon Curve, and more
- **Customization**: Create and modify your own L-Systems with custom rules and parameters
- **Animation**: Generate GIF animations showing the evolution of an L-System through iterations
- **Export/Import**: Save custom systems for future use

## Prerequisites

- Python 3.6 or higher
- PIL (Pillow) library for image processing
- **Ghostscript**: Required for PostScript to image conversion
  - Download from: [Ghostscript Downloads](https://ghostscript.com/releases/gsdnld.html)
  - Make sure Ghostscript is added to your system PATH

## Installation

1. Clone this repository
2. Install required Python packages:
```bash
pip install -r requirements.txt
```
3. Install Ghostscript (link above)
4. Run the application:
```bash
python main.py
```

## Usage

### Basic Controls

- Select a predefined L-System from the dropdown menu
- Adjust the number of iterations (higher values create more complex patterns)
- Click "Draw L-System" to render the fractal

### Creating Custom Systems

1. Modify any of the parameters:
- **Axiom**: The starting string
- **Variables**: Characters that will be replaced according to rules
- **Rules**: Replacement patterns for each variable
- **Angle**: The turning angle (in degrees)
- **Distance**: Length of each forward step
- **Heading Angle**: Initial direction of the turtle
- **Stack Settings**: Controls branching behavior

2. Click "Export Custom System" to save your creation

### Animation Mode

1. Set the desired number of iterations
2. Move the slider to "Animation (GIF)"
3. Click "Draw L-System"
4. Wait for the animation to be generated

## File Locations

- **Custom Systems**: Saved in `data/custom/` directory as JSON files
- **Animation GIFs**: Saved in `animations/` directory
- **Example Systems**: Located in `data/examples/` directory

## L-System Syntax

- `A-U | 1-9`: Draw forward by the specified distance
- `a-u`: Move forward without drawing
- `V-Z | v-z`: Don't do anything (no operation)
- `+`: Turn right by the specified angle
- `-`: Turn left by the specified angle
- `|`: Turn around (180 degrees)
- `[`: Save current position and angle
- `]`: Return to last saved position and angle

## Examples

The application comes with several predefined L-Systems:
- Koch Curve and Koch Triangle
- Sierpinski Triangle
- Dragon Curve
- Fractal Plant
- Tree structures

## Troubleshooting

If you encounter issues with GIF generation, ensure Ghostscript is correctly installed and accessible in your system PATH.