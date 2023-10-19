import os

from get_shot_scripts import get_shot_scripts
from logs import log


def bulk_process_shots(shots_dir_path, should_move_assets):
	if not os.path.exists(shots_dir_path):
		log(f"The directory {shots_dir_path} does not exist.", "ERROR")
		return

	# List all directories under shots directory
	shot_dirs = [d for d in os.listdir(shots_dir_path) if os.path.isdir(os.path.join(shots_dir_path, d))]

	if not shot_dirs:
		log("No shot directories found.", 'ERROR')
		return

	log(f"Enter the numbers of the directories to process{' and move assets ' if should_move_assets else ' '}(comma-separated), 'q' to quit, or 'all' to select all:",
		'WARNING')

	for i, shot_dir in enumerate(shot_dirs):
		print(f"{i + 1}: {shot_dir}")

	user_input = input("Your selection: ").strip()

	if user_input.lower() == 'q':
		log("Quit selected. No directories will be processed.", 'INFO')
		return
	elif user_input.lower() == 'all':
		selected_indices = list(range(len(shot_dirs)))
	else:
		selected_indices = [int(idx) - 1 for idx in user_input.split(',') if idx.isdigit() and 1 <= int(idx) <= len(shot_dirs)]

	if not selected_indices:
		log("No valid directories selected for processing.", 'ERROR')
		return

	for idx in selected_indices:
		shot_dir = shot_dirs[idx]
		shot_dir_path = os.path.join(shots_dir_path, shot_dir)
		get_shot_scripts(shot_dir_path, should_move_assets)

	log("Completed processing for selected directories.", 'INFO')
