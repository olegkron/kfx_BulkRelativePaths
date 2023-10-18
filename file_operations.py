import os
import shutil


def get_latest_script(dir_path):
	# List all the files in dir_path
	files = [f for f in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, f))]

	# Sort files by their names
	sorted_files = sorted(files, reverse=True)

	for file_name in sorted_files:
		if file_name.endswith(".nk"):
			# print(f"Found latest script: {file_name}")
			return os.path.join(dir_path, file_name)


def create_file_backup(file_path):
	# if backup file already exists, do not create a new backup
	if os.path.exists(f"{file_path}.backup"):
		return f"{file_path}.backup"
	backup_path = f"{file_path}.backup"
	shutil.copy(file_path, backup_path)
	return backup_path


def check_file_exists(full_path):
	if "%" in full_path:
		dir_name, file_pattern = os.path.split(full_path)
		file_prefix = file_pattern.split("%")[0]
		for filename in os.listdir(dir_name):
			if filename.startswith(file_prefix):
				return True
	else:
		return os.path.exists(full_path)
	return False


def create_directory_if_not_exists(directory_path):
	if not os.path.exists(directory_path):
		os.makedirs(directory_path)


def copy_file_to_destination(src_path, dest_path):
	shutil.copy(src_path, dest_path)
