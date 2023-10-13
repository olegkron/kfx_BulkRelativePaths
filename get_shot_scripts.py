import os

from file_operations import create_file_backup, get_latest_script
from script_operations import generate_relative_path, set_project_directory_to_script, set_script_to_relative_paths


def get_shot_scripts(shot_dir_path):
	scripts_dir = os.path.join(shot_dir_path, "SCRIPTS", "NUKE")

	latest_script = get_latest_script(scripts_dir)
	if not latest_script:
		print(f"No .nk files found in {scripts_dir}")
		return

	backup_path = create_file_backup(latest_script)
	# print(f"Backup created: {backup_path}")
	set_script_to_relative_paths(latest_script, generate_relative_path, shot_dir_path)
	# print(f"Updated relative paths in: {latest_script}")
	set_project_directory_to_script(latest_script)
