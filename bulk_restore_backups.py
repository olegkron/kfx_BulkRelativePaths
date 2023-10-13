import os

from restore_script_from_backup import restore_script_from_backup


def bulk_restore_backups(shots_dir_path):
	if not os.path.exists(shots_dir_path):
		print(f"The directory {shots_dir_path} does not exist.")
		return

	# List all directories in the SHOTS folder
	all_folders = [f for f in os.listdir(shots_dir_path) if os.path.isdir(os.path.join(shots_dir_path, f))]

	if not all_folders:
		print("No shot directories found.")
		return

	# Ask the user to select which folders to restore backups
	print("Select the shot directories to restore backups:")
	for i, folder in enumerate(all_folders):
		print(f"{i + 1}: {folder}")

	selected_indices = input("Enter the numbers of the directories to restore backups (comma-separated): ").strip().split(',')
	selected_indices = [int(idx) - 1 for idx in selected_indices if idx.isdigit() and 1 <= int(idx) <= len(all_folders)]

	if not selected_indices:
		print("No valid directories selected for restoring backups.")
		return

	for idx in selected_indices:
		folder = all_folders[idx]
		shot_dir_path = os.path.join(shots_dir_path, folder)
		print(f"Restoring backups for {shot_dir_path}...")

		# Call restore_script_from_backup for each selected folder
		restore_script_from_backup(shot_dir_path)

		print(f"Completed restoring backups for {shot_dir_path}\n")
