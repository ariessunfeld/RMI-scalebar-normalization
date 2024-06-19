# RMI-scalebar-normalization

This repository contains utility scripts for automatically rescaling and normalizing the scalebars in ChemCam and SuperCam RMI mosaics. Scripts should be edited to use appropriate paths and reviewed carefully to avoid overwriting existing images.

# Setup (macOS)

- Clone this repository
- Create a new virtual environment: `python3.11 -m venv venv`
- Activate the virtual environment: `source /venv/bin/activate`
- Install the dependencies: `pip install -r requirements.txt`
- Open `convert.py` and edit the `BASE_IMAGE_DIRECTORY` path, the `OUTPUT_DIRECTORY` path, and the `TARGETS_TO_CONVERT` list
  - Ensure that `BASE_IMAGE_DIRECTORY` contains RMI mosaics with the filename pattern `...[name]_after.png`
  - Ensure that each target name listed in `TARGETS_TO_CONVERT` occurs in at least one file in `BASE_IMAGE_DIRECTORY`

# Usage

After follwing the setup steps, run `python convert.py`. The targets you specified in `TARGETS_TO_CONVERT` should now have scalebar-corrected versions in `OUTPUT_DIRECTORY`.

