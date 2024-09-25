import os
import shutil
from Constant.constant import OUTPUT_TEMP_FOLDER_PATH

class CleanUp :

    def __init__(self):
        pass
    
    def clear_temp_folders():
        # Iterate through all items in the specified directory
        for item in os.listdir(OUTPUT_TEMP_FOLDER_PATH):
            item_path = os.path.join(OUTPUT_TEMP_FOLDER_PATH, item)
            # Check if the item is a directory and starts with 'Temp'
            if os.path.isdir(item_path) and item.startswith('Temp'):
                try:
                    shutil.rmtree(item_path)  # Remove the directory and its contents
                    print(f"Removed: {item_path}")
                except Exception as e:
                    print(f"Error removing {item_path}: {e}")