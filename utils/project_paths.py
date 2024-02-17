import os

class ProjectPaths:
    # Get the current directory (the directory where this script is located)
    current_directory = os.path.dirname(os.path.abspath(__file__))

    # Define project folder paths
    root = os.path.abspath(os.path.join(current_directory, os.pardir))
    
    # Define subfolder paths relative to the root
    storage_dir = os.path.join(root, "storage")
    
    # Define processed images folder paths relative to the storage_dir
    images_dir = os.path.join(storage_dir, "images")
    
    @classmethod
    def init(cls):
       """
        Create the project folders if they don't exist.
       """
       os.makedirs(cls.storage_dir, exist_ok=True)

       os.makedirs(cls.images_dir, exist_ok=True)
       

# Initialize the project paths
ProjectPaths.init()
