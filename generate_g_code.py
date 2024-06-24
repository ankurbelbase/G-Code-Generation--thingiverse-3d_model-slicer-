import os
import glob
import subprocess
import shutil
import time

# Directory where your STL files are located
STL_DIRECTORY = "C:/3DPrinter/STLFiles"

# Directory where the G-code files will be saved
BASE_GCODE_DIRECTORY = "C:/3DPrinter/GCodeFiles"

# Paths to the slicer executables
CURA_PATH = "../cura-slicer.exe"
PRUSASLICER_PATH = "../prusa-slicer.exe"
SLIC3R_PATH = "../slic3r.exe"

# Paths to the configuration files for each slicer and each printer
CURA_CONFIG_PRINTER1 = "../cura_printer_1.ini"
CURA_CONFIG_PRINTER2 = "../cura_printer_2.ini"
PRUSASLICER_CONFIG_PRINTER1 = "../prusa_printer_1.ini"
PRUSASLICER_CONFIG_PRINTER2 = "../prusa_printer_2.ini"
SLIC3R_CONFIG_PRINTER1 = "../slic3r_printer_1.ini"
SLIC3R_CONFIG_PRINTER2 = "../slic3r_printer_2.ini"

# Define the slicers and their configurations
slicers = [
    {
        "name": "cura",
        "path": CURA_PATH,
        "configs": [
            CURA_CONFIG_PRINTER1,
            CURA_CONFIG_PRINTER2
        ],
        "config_option": "--load"
    },
    {
        "name": "prusaslicer",
        "path": PRUSASLICER_PATH,
        "configs": [
            PRUSASLICER_CONFIG_PRINTER1,
            PRUSASLICER_CONFIG_PRINTER2
        ],
        "config_option": "--export-gcode"
    },
    {
        "name": "slic3r",
        "path": SLIC3R_PATH,
        "configs": [
            SLIC3R_CONFIG_PRINTER1,
            SLIC3R_CONFIG_PRINTER2
        ],
        "config_option": "--load"
    }
]

all_files_processed = False

while not all_files_processed:
    gcode_counter = 0
    stl_files = glob.glob(os.path.join(STL_DIRECTORY, "*.stl"))

    # Check if there are any STL files left
    if not stl_files:
        print("All STL files have been processed. Exiting the loop.")
        all_files_processed = True
        break

    # Loop through each STL file
    for stl_path in stl_files:
        stl_file_name = os.path.splitext(os.path.basename(stl_path))[0]

        # Loop through each slicer
        for slicer in slicers:
            slicer_name = slicer["name"]
            slicer_path = slicer["path"]
            slicer_configs = slicer["configs"]
            config_option = slicer["config_option"]

            # Loop through each slicer configuration (for each printer)
            for config in slicer_configs:
                try:
                    # Generate a unique G-code file name
                    gcode_file_name = f"{slicer_name}_{os.path.basename(config)}_{stl_file_name}.gcode"
                    gcode_directory = os.path.join(BASE_GCODE_DIRECTORY, slicer_name, os.path.basename(config))
                    os.makedirs(gcode_directory, exist_ok=True)
                    gcode_path = os.path.join(gcode_directory, gcode_file_name)

                    # Running the Slicer
                    if slicer_name == "prusaslicer":
                        command = [slicer_path, config_option, "--load", config, "-o", gcode_path, stl_path]
                    else:
                        command = [slicer_path, config_option, config, "-o", gcode_path, stl_path]

                    subprocess.run(command, check=True)
                    gcode_counter += 1
                except Exception as e:
                    print(f"An error occurred while generating G-code: {e}")
                    # Log the error for later analysis
                    pass

    # Move the STL files after processing
    for stl_path in stl_files:
        new_stl_directory = "C:/3DPrinter/CompletedSTLFiles"  # Change this to your desired destination folder
        os.makedirs(new_stl_directory, exist_ok=True)
        new_stl_path = os.path.join(new_stl_directory, os.path.basename(stl_path))
        shutil.move(stl_path, new_stl_path)

    print(f"\nTotal G-code files generated: {gcode_counter}")

    # Pause for a while before the next iteration
    time.sleep(60)  # Adjust the sleep duration as needed

# After all files are processed, print summary
gcode_counter = 0
completed_models = []

# Process each slicer configuration
for slicer in slicers:
    slicer_name = slicer["name"]
    slicer_path = slicer["path"]
    slicer_configs = slicer["configs"]
    config_option = slicer["config_option"]

    # Loop through each slicer configuration (for each printer)
    for i, config in enumerate(slicer_configs, start=1):
        # Check if the config file exists
        if not os.path.exists(config):
            print(f"Config file {config} not found. Skipping...")
            continue

        # Loop through each STL file
        for stl_path in glob.glob(os.path.join(STL_DIRECTORY, "*.stl")):
            stl_file_name = os.path.splitext(os.path.basename(stl_path))[0]

            # Define a subdirectory for each slicer and printer
            gcode_directory = os.path.join(BASE_GCODE_DIRECTORY, slicer_name, f"printer{i}")
            os.makedirs(gcode_directory, exist_ok=True)

            gcode_file_name = f"{stl_file_name}.gcode"
            gcode_path = os.path.join(gcode_directory, gcode_file_name)

            # Check if the G-code file already exists; if so, skip this file
            if os.path.exists(gcode_path):
                print(f"G-code file {gcode_path} already exists. Skipping...")
                continue

            # Run slicer command
            try:
                if slicer_name == "prusaslicer":
                    command = [slicer_path, config_option, "--load", config, "-o", gcode_path, stl_path]
                else:
                    command = [slicer_path, config_option, config, "-o", gcode_path, stl_path]

                subprocess.run(command, check=True)
                gcode_counter += 1
            except subprocess.CalledProcessError as e:
                print(f"Failed to generate G-code with {slicer_name} for {stl_file_name}: {e}")

        # After processing, move the STL file
        new_stl_directory = "C:/3DPrinter/CompletedSTLFiles"  # Change this to your desired destination folder
        os.makedirs(new_stl_directory, exist_ok=True)
        new_stl_path = os.path.join(new_stl_directory, os.path.basename(stl_path))
        shutil.move(stl_path, new_stl_path)
        completed_models.append(stl_file_name)

# Print completed models and total G-code files generated
print("Completed models:")
for model in completed_models:
    print(model)
print(f"Total G-code files generated: {gcode_counter}")
