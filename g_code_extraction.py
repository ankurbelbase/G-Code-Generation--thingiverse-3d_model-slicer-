import os
import csv
from collections import defaultdict

# Function to count G-Code and M-Code commands in a file
def count_codes(file_path):
    gcodes = defaultdict(int)  # Dictionary to store G-Code command counts
    mcodes = defaultdict(int)  # Dictionary to store M-Code command counts
    with open(file_path, 'r') as f:
        for line in f:
            if line.startswith('G'):
                command = line.split()[0]  # Extract the G-Code command
                gcodes[command] += 1  # Increment the count for this G-Code command
            elif line.startswith('M'):
                command = line.split()[0]  # Extract the M-Code command
                mcodes[command] += 1  # Increment the count for this M-Code command
    return gcodes, mcodes  # Return the dictionaries with command counts

import glob

# Base directory where your slicer subdirectories are located
BASE_GCODE_DIRECTORY = "BASE/GCODE/DIRECTORY"

# Function to get slicer names and their corresponding directories
def get_slicer_directories(base_directory):
    slicer_directories = {}

    # List immediate subdirectories in the base directory
    subdirectories = [d for d in os.listdir(base_directory) if os.path.isdir(os.path.join(base_directory, d))]

    # Iterate through immediate subdirectories
    for subdirectory in subdirectories:
        slicer_path = os.path.join(base_directory, subdirectory)
        
        # List subdirectories one level deeper
        subdirectories_one_deeper = [d for d in os.listdir(slicer_path) if os.path.isdir(os.path.join(slicer_path, d))]

        # Store slicer name as a key and its corresponding subdirectories one level deeper
        slicer_directories[subdirectory] = [os.path.join(slicer_path, d) for d in subdirectories_one_deeper]

    return slicer_directories

# Get a dictionary of slicers and their corresponding directories
slicer_directories = get_slicer_directories(BASE_GCODE_DIRECTORY)
data = []

# Iterate through each slicer and its directories
for slicer, directories in slicer_directories.items():
    for directory in directories:
        printer = os.path.basename(directory)  # Extract printer name from directory path
        for filename in os.listdir(directory):
            if filename.endswith('.gcode'):
                file_path = os.path.join(directory, filename)  # Get the full path to the G-Code file
                gcodes, mcodes = count_codes(file_path)  # Count the G-Code and M-Code commands in the file
                data.append({
                    'slicer': slicer,
                    'printer': printer,
                    'file': filename,
                    'total_gcodes': sum(gcodes.values()),  # Total number of G-Code commands
                    'total_mcodes': sum(mcodes.values()),  # Total number of M-Code commands
                    **gcodes,  # Add G-Code counts to the dictionary
                    **mcodes   # Add M-Code counts to the dictionary
                })

# Collect all unique G-Code and M-Code commands from the data
commands = set()
for item in data:
    commands.update(item.keys())
commands.difference_update({'slicer', 'printer', 'file', 'total_gcodes', 'total_mcodes'})  # Remove non-command keys
commands = sorted(commands)  # Sort commands for consistent ordering

# Output file path for the CSV file
output_file = 'OUTPUT/CSV/FILE/PATH'

# Write the data to a CSV file
with open(output_file, 'w', newline='') as f:
    writer = csv.writer(f)
    # Write the header row with slicer, printer, file, totals, and command columns
    writer.writerow(['slicer', 'printer', 'file', 'total_gcodes', 'total_mcodes', *commands])
    for item in data:
        # Write each row of data
        writer.writerow([item['slicer'], item['printer'], item['file'], item['total_gcodes'], item['total_mcodes']] + [item.get(command, 0) for command in commands])
