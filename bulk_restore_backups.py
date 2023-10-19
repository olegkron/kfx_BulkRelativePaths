import os

from logs import log
from restore_script_from_backup import restore_script_from_backup


def bulk_restore_backups(shots_dir_path):
	if not os.path.exists(shots_dir_path):
		log(f"The directory {shots_dir_path} does not exist.", 'ERROR')
		return

	# List all directories in the SHOTS folder
	all_folders = [f for f in os.listdir(shots_dir_path) if os.path.isdir(os.path.join(shots_dir_path, f))]

	if not all_folders:
		log("No shot directories found.", 'ERROR')
		return

	log("Enter the numbers of the directories to restore backups (comma-separated), 'q' to quit, or 'all' to select all:", 'WARNING')

	for i, folder in enumerate(all_folders):
		print(f"{i + 1}: {folder}")

	user_input = input("Your selection: ").strip()

	if user_input.lower() == 'q':
		log("Quit selected. No directories will be restored.", 'INFO')
		return
	elif user_input.lower() == 'all':
		selected_indices = list(range(len(all_folders)))
	else:
		selected_indices = [int(idx) - 1 for idx in user_input.split(',') if idx.isdigit() and 1 <= int(idx) <= len(all_folders)]

	if not selected_indices:
		log("No valid directories selected for restoring backups.", 'ERROR')
		return

	for idx in selected_indices:
		folder = all_folders[idx]
		shot_dir_path = os.path.join(shots_dir_path, folder)
		restore_script_from_backup(shot_dir_path)
	# log(f"Restored backups for {shot_dir_path}", 'INFO')

	log("Completed restoring backups for selected directories.", 'INFO')
