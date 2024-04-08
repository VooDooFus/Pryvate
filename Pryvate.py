import os
import re
from tqdm import tqdm

def search_for_private_keys(directory):
    private_key_pattern = re.compile(r'(?<![A-Za-z0-9])[1-9A-HJ-NP-Za-km-z]{51,52}(?![A-Za-z0-9])')
    found_private_keys = []

    # Count total number of files
    total_files = sum(len(files) for _, _, files in os.walk(directory))

    for root, _, files in os.walk(directory):
        for file_name in tqdm(files, total=total_files, desc="Scanning files"):
            file_path = os.path.join(root, file_name)
            # Skip system files and directories that we don't have permission to access
            if os.path.islink(file_path) or os.path.ismount(file_path):
                continue
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
                    contents = file.read()
                    private_keys = private_key_pattern.findall(contents)
                    if private_keys:
                        found_private_keys.extend(private_keys)
            except (PermissionError, FileNotFoundError):
                pass
            except Exception as e:
                print(f"Error reading {file_path}: {e}")
    
    return found_private_keys

def main():
    drives = [f"{d}:\\" for d in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ' if os.path.exists(f"{d}:")]
    for drive in drives:
        print(f"Scanning {drive} for Bitcoin private keys...")
        private_keys = search_for_private_keys(drive)
        if private_keys:
            print(f"Found {len(private_keys)} Bitcoin private keys on {drive}")
            for private_key in private_keys:
                print(private_key)
        else:
            print("No Bitcoin private keys found on this drive.")

if __name__ == "__main__":
    main()
