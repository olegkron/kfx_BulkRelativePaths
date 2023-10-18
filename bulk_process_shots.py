import os

from get_shot_scripts import get_shot_scripts


def bulk_process_shots(shots_dir_path, should_move_assets):
	if not os.path.exists(shots_dir_path):
		print(f"The directory {shots_dir_path} does not exist.")
		return

	# List all directories under shots directory
	shot_dirs = [d for d in os.listdir(shots_dir_path) if os.path.isdir(os.path.join(shots_dir_path, d))]

	if not shot_dirs:
		print("No shot directories found.")
		return

	# Ask the user to select which folders to process
	print("Select the shot directories to process:")
	for i, shot_dir in enumerate(shot_dirs):
		print(f"{i + 1}: {shot_dir}")

	selected_indices = input("Enter the numbers of the directories to process (comma-separated): ").strip().split(',')
	selected_indices = [int(idx) - 1 for idx in selected_indices if idx.isdigit() and 1 <= int(idx) <= len(shot_dirs)]

	if not selected_indices:
		print("No valid directories selected for processing.")
		return

	for idx in selected_indices:
		shot_dir = shot_dirs[idx]
		shot_dir_path = os.path.join(shots_dir_path, shot_dir)
		print(f"Processing {shot_dir_path}...")

		# Call get_shot_scripts for each selected shot directory
		get_shot_scripts(shot_dir_path, should_move_assets)
		print(f"Completed processing for {shot_dir_path}\n")
