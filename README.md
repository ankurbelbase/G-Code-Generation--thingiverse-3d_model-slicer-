# 3D Model Automation Scripts

## Overview

This repository contains three Python scripts that automate the process of downloading a 3D model from Thingiverse, generating G-code using three different slicers, and extracting specific commands from the generated G-code files.

## Features

1. **Download 3D Model**: Downloads a 3D model from Thingiverse using the provided Thingiverse model object id.
2. **Generate G-code**: Uses three different slicers to generate G-code from the downloaded 3D model.
3. **Extract Commands**: Extracts specific commands from the generated G-code files for further analysis.

## Requirements

- Python 3.x
- Required Python libraries: `requests`, `os`, `re`, `subprocess`
- Slicer software installed and accessible from the command line:
  - Slicer1 (e.g., Cura)
  - Slicer2 (e.g., PrusaSlicer)
  - Slicer3 (e.g., Slic3r)

## Installation

1. Clone the repository:
   ```sh
   git clone [<repository-url>](https://github.com/ankurbelbase/G-Code-Generation--thingiverse-3d_model-slicer-.git)
   cd <repository-directory>
