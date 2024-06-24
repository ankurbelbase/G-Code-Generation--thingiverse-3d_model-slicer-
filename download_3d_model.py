import os
import requests
import time

# API token for accessing Thingiverse API
api_token = "API_KEY"

# Directories where STL and G-code models will be saved
save_stl_directory = "/save/stl/directory"
save_gcode_directory = "/save/gcode/directory"

# Create the directories if they don't exist
if not os.path.exists(save_stl_directory):
    os.makedirs(save_stl_directory)
if not os.path.exists(save_gcode_directory):
    os.makedirs(save_gcode_directory)

# Maximum number of models to download
max_items = 10000
# Maximum file size for download (100 MB)
MAX_FILE_SIZE = 1024 * 1024 * 100

# Thingiverse API base URL
THINGIVERSE_API_URL = 'https://api.thingiverse.com'

def main():
    """
    Main function to download models incrementally from Thingiverse.
    """
    headers = {'Authorization': f'Bearer {api_token}'}
    session = requests.Session()

    # Starting Thing ID for downloading models
    start_thing_id = 6190257  # Replace with the appropriate starting Thingiverse object ID

    # Loop through Thing IDs and download models if they are accessible
    for thing_id in range(start_thing_id, start_thing_id + max_items):
        if is_model_accessible(session, headers, thing_id):
            download_first_model(session, headers, thing_id)

def is_model_accessible(session, headers, thing_id):
    """
    Check if a model is accessible (public and free).
    
    Args:
        session: Requests session object.
        headers: Headers for the request.
        thing_id: Thingiverse model ID.

    Returns:
        bool: True if the model is accessible, False otherwise.
    """
    url = f'{THINGIVERSE_API_URL}/things/{thing_id}'
    try:
        response = session.get(url, headers=headers)
        response.raise_for_status()
        model_info = response.json()
        is_private = model_info.get('is_private', False)
        is_purchased = model_info.get('is_purchased', False)
        return not is_private and not is_purchased
    except requests.exceptions.RequestException as e:
        print(f'Failed to check accessibility for Thing ID {thing_id}: {e}')
        return False

def download_first_model(session, headers, thing_id):
    """
    Download the first STL and G-code models for a given Thing ID.

    Args:
        session: Requests session object.
        headers: Headers for the request.
        thing_id: Thingiverse model ID.
    """
    url = f'{THINGIVERSE_API_URL}/things/{thing_id}/files'
    file_path_stl = f'{save_stl_directory}/model_{thing_id}.stl'
    file_path_gcode = f'{save_gcode_directory}/model_{thing_id}.gcode'

    # Skip download if files already exist
    if os.path.exists(file_path_stl) or os.path.exists(file_path_gcode):
        print(f'Model files for Thing ID {thing_id} already exist. Skipping download.')
        return

    try:
        response = session.get(url, headers=headers)
        response.raise_for_status()
        files = response.json()
    except requests.exceptions.RequestException as e:
        print(f'Failed to get files for Thing ID {thing_id}: {e}')
        return

    stl_downloaded = False  # Track if an STL file has been downloaded
    gcode_downloads = 0  # Track the number of G-code files downloaded

    for file in files:
        file_name = file['name']
        file_size = file['size']
        download_url = file['download_url']

        # Download the first STL file
        if file_name.endswith('.stl') and not stl_downloaded and file_size is not None and isinstance(file_size, int) and file_size < MAX_FILE_SIZE:
            download_file(session, headers, download_url, file_path_stl)
            stl_downloaded = True  # Mark that an STL file has been downloaded
        # Download G-code files
        elif file_name.endswith('.gcode') and file_size is not None and isinstance(file_size, int) and file_size < MAX_FILE_SIZE:
            download_file(session, headers, download_url, file_path_gcode)
            gcode_downloads += 1

def download_file(session, headers, url, file_path):
    """
    Download a file from a given URL and save it to the specified file path.

    Args:
        session: Requests session object.
        headers: Headers for the request.
        url: URL of the file to be downloaded.
        file_path: Local path where the file will be saved.
    """
    for attempt in range(3):  # Retry up to 3 times
        try:
            response = session.get(url, headers=headers, allow_redirects=True)
            response.raise_for_status()
            with open(file_path, 'wb') as f:
                f.write(response.content)
            print(f'File saved at {file_path}.')
            break  # Exit the loop if download is successful
        except requests.exceptions.RequestException as e:
            print(f'Failed to download file from {url}, attempt {attempt + 1}: {e}')
            time.sleep(1)  # Retry after 1 second

if __name__ == '__main__':
    main()
