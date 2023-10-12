import os
import shutil


def get_latest_script(dir_path):
	# List all the files in dir_path
	files = [f for f in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, f))]

	# Sort files by their names
	sorted_files = sorted(files, reverse=True)

	for file_name in sorted_files:
		if file_name.endswith(".nk"):
			return os.path.join(dir_path, file_name)


def create_file_backup(file_path):
	# if backup file already exists, do not create a new backup
	if os.path.exists(f"{file_path}.backup"):
		return f"{file_path}.backup"
	backup_path = f"{file_path}.backup"
	shutil.copy(file_path, backup_path)
	return backup_path
