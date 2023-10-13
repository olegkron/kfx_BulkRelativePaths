# Bulk relative paths for SHOTS folder
# 1. scan the SHOTS dir for shots and find the latest version of the script
# 2. makes a backup of the script to the same location
# 3. replaces all file paths in the script with relative paths as well as sets the project directory to \[python \{nuke.script_directory()\}]
# 4. saves the script
# logs which scripts were changed
from bulk_process_shots import bulk_process_shots
from bulk_restore_backups import bulk_restore_backups
import argparse

# print(f"Updated project directory in: {latest_script}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Bulk processing of shots or restoring backups')
    parser.add_argument('--restore', '-r', action='store_true', help='Restore backups instead of processing shots')
    args = parser.parse_args()

    shots_dir_path = "/Users/koalamac/Desktop/SHOTS"

    if args.restore:
        bulk_restore_backups(shots_dir_path)
    else:
        bulk_process_shots(shots_dir_path)
