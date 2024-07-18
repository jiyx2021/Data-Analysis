import os
import glob

dataset_folder = 'python/data'

# File related preprocessing steps, such as renaming user-detail.txt, or removing all the pictures
def rename_user_details(dataset_folder):
    for root, dirs, files in os.walk(dataset_folder):
        # Check if 'detail.txt' is in the files
        if 'detail.txt' in files:
            # Calculate the relative path from the dataset folder
            relative_path = os.path.relpath(root, dataset_folder)
            # Split the relative path to count the levels
            path_parts = relative_path.split(os.sep)
            # If the depth is 1, it's a user directory
            if len(path_parts) == 1:
                user_details_path = os.path.join(root, 'detail.txt')
                new_user_details_path = os.path.join(root, 'user-detail.txt')
                os.rename(user_details_path, new_user_details_path)
                print(f"Renamed {user_details_path} to {new_user_details_path}")

# Example usage
# rename_user_details(dataset_folder)

# Delete all the images within our data file
def delete_jpg_files(root_dir):
    # Find all .jpg files within the root directory and its subdirectories
    jpg_files = glob.glob(os.path.join(root_dir, '**', '*.jpg'), recursive=True)
    
    # Iterate over the list of .jpg files and delete each one
    for file_path in jpg_files:
        try:
            os.remove(file_path)
            print(f"Deleted: {file_path}")
        except OSError as e:
            print(f"Error deleting {file_path}: {e}")

# Example usage
delete_jpg_files(dataset_folder)