import os

from file_operations import create_file_backup, get_latest_script
from logs import log
from script_operations import generate_relative_path, move_nonlocal_assets_to_plates_dir, set_project_directory_to_script, set_script_to_relative_paths


def get_shot_scripts(shot_dir_path, should_move_assets):
	scripts_dir = os.path.join(shot_dir_path, "SCRIPTS", "NUKE")

	latest_script = get_latest_script(scripts_dir)
	if not latest_script:
		log(f"No .nk files found in {scripts_dir}", 'ERROR')
		return

	backup_path = create_file_backup(latest_script)
	log(f"Backup created: {backup_path}", 'DEBUG')
	set_script_to_relative_paths(latest_script, generate_relative_path, shot_dir_path)
	if should_move_assets:
		log("Moving assets to PLATES directory...", 'INFO')
		move_nonlocal_assets_to_plates_dir(latest_script, shot_dir_path)
	log(f"Created relative paths in: {latest_script}", 'INFO')
	set_project_directory_to_script(latest_script)
