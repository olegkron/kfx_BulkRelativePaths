# Bulk relative paths for SHOTS folder
# 1. scan the SHOTS dir for shots and find the latest version of the script
# 2. makes a backup of the script to the same location
# 3. replaces all file paths in the script with relative paths as well as sets the project directory to \[python \{nuke.script_directory()\}]
# 4. saves the script
# logs which scripts were changed
import os

from file_operations import create_file_backup, get_latest_script
from restore_script_from_backup import restore_script_from_backup
from script_operations import generate_relative_path, set_project_directory_to_script, set_script_to_relative_paths


def bulk_process_shots(shots_dir_path):
	if not os.path.exists(shots_dir_path):
		print(f"The directory {shots_dir_path} does not exist.")
		return

	# List all directories under shots directory
	shot_dirs = [d for d in os.listdir(shots_dir_path) if os.path.isdir(os.path.join(shots_dir_path, d))]

	if not shot_dirs:
		print("No shot directories found.")
		return

	for shot_dir in shot_dirs:
		shot_dir_path = os.path.join(shots_dir_path, shot_dir)
		print(f"Processing {shot_dir_path}...")

		# Call get_shot_scripts for each shot directory
		get_shot_scripts(shot_dir_path)
		print(f"Completed processing for {shot_dir_path}\n")


def bulk_restore_backups(shots_dir_path):
	if not os.path.exists(shots_dir_path):
		print(f"The directory {shots_dir_path} does not exist.")
		return

	# List all directories in the SHOTS folder
	all_folders = [f for f in os.listdir(shots_dir_path) if os.path.isdir(os.path.join(shots_dir_path, f))]

	for folder in all_folders:
		shot_dir_path = os.path.join(shots_dir_path, folder)
		restore_script_from_backup(shot_dir_path)


def get_shot_scripts(shot_dir_path):
	scripts_dir = os.path.join(shot_dir_path, "SCRIPTS", "NUKE")

	latest_script = get_latest_script(scripts_dir)
	if not latest_script:
		print(f"No .nk files found in {scripts_dir}")
		return

	backup_path = create_file_backup(latest_script)
	# print(f"Backup created: {backup_path}")

	set_script_to_relative_paths(latest_script, generate_relative_path, shot_dir_path)
	# 	print(f"Updated relative paths in: {latest_script}")

	set_project_directory_to_script(latest_script)


# 	print(f"Updated project directory in: {latest_script}")


if __name__ == '__main__':
	shot_dir_path = "/Users/koalamac/Desktop/WSP_0091"
	shots_dir_path = "/Users/koalamac/Desktop/SHOTS"
	# get_shot_scripts(shot_dir_path)
	# restore_script_from_backup(shot_dir_path)
	bulk_process_shots(shots_dir_path)
# bulk_restore_backups(shots_dir_path)
