import os
import shutil


def restore_script_from_backup(shot_dir_path):
	nuke_folder_path = os.path.join(shot_dir_path, "SCRIPTS", "NUKE")

	if not os.path.exists(nuke_folder_path):
		print(f"The directory {nuke_folder_path} does not exist.")
		return

	# List all files in the Nuke folder
	all_files = os.listdir(nuke_folder_path)

	# Debug: Print all files
	# print(f"All files: {all_files}")

	# Identify Nuke scripts and their backups
	nuke_scripts = [f for f in all_files if f.endswith('.nk')]
	nuke_backups = [f for f in all_files if f.endswith('.nk.backup')]

	# Debug: Print Nuke scripts and backups
	# print(f"Nuke Scripts: {nuke_scripts}")
	# print(f"Nuke Backups: {nuke_backups}")

	# If no backups, return early
	if not nuke_backups:
		print("No backup found.")
		return

	# Sort to get the latest backup
	nuke_backups.sort()

	# Assume the last backup in the sorted list is the latest
	latest_backup = nuke_backups[-1]

	# Identify the original script corresponding to the latest backup
	original_script = latest_backup.replace('.backup', '')

	# If the original script is also present, we should prompt before overwriting
	# if original_script in nuke_scripts:
	# 	should_restore = input(f"{original_script} already exists. Do you want to restore from backup? (y/n): ")
	# 	if should_restore.lower() != 'y':
	# 		return

	# Perform the restore by copying
	backup_path = os.path.join(nuke_folder_path, latest_backup)
	original_path = os.path.join(nuke_folder_path, original_script)

	shutil.copy(backup_path, original_path)
	print(f"Restored {original_script} from {latest_backup}")
