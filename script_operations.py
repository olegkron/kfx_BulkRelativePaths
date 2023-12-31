import glob
import os
import re
import shutil

import config
from file_operations import check_file_exists, copy_file_to_destination, create_directory_if_not_exists
from logs import log


def set_script_to_relative_paths(file_path, generate_relative_path_func, shot_dir_path, whitelist=[], blacklist=["Write"]):
	with open(file_path, 'r+') as f:
		content = f.read()

		current_node = None
		should_replace = True

		def replace_read_path(match):
			nonlocal current_node, should_replace
			last_index = match.lastindex

			if last_index == 1:  # Node detection pattern
				current_node = match.group(1)
				if whitelist:
					should_replace = current_node in whitelist
				else:
					should_replace = current_node not in blacklist

			# log(f"Processing node: {current_node}, should replace: {should_replace}", 'DEBUG')
			elif last_index == 2 and should_replace:  # File path replacement pattern
				full_path = match.group(2)
				relative_path = generate_relative_path_func(full_path, shot_dir_path)
				if relative_path is not None:
					return f"file {relative_path}"

			return match.group(0)

		content = re.sub(r'(\w+) {|file (.+)', replace_read_path, content)
		f.seek(0)
		f.write(content)
		f.truncate()


def insert_into_file(file_path, text, line_num):
	with open(file_path, 'r+') as file:
		lines = file.readlines()
		lines.insert(line_num, text)
	with open(file_path, 'w') as file:
		file.writelines(lines)


def set_project_directory_to_script(file_path):
	found_root = False
	found_project_directory = False
	root_end_line = None
	project_directory_line_index = None

	with open(file_path, 'r') as f:
		lines = f.readlines()

	for idx, line in enumerate(lines):
		# Check if the line belongs to a Root object
		if "Root {" in line:
			found_root = True

		# Mark the end of Root object
		if found_root and "}\n" in line:
			root_end_line = idx
			break

		# If inside a Root object, check for project_directory
		if found_root and "project_directory" in line:
			found_project_directory = True
			project_directory_line_index = idx
			new_line = f'project_directory "\\[python {{nuke.script_directory()}}]"\n'
			lines[idx] = new_line

	# If project_directory was not found within Root, add it before the end of Root
	if found_root and not found_project_directory and root_end_line is not None:
		text_to_insert = 'project_directory "\\[python {nuke.script_directory()}]"\n'
		insert_into_file(file_path, text_to_insert, root_end_line)

	# If project_directory was found and updated within Root, update the file
	if found_project_directory:
		with open(file_path, 'w') as f:
			f.writelines(lines)


def file_exists_from_relative_path(relative_path, shot_dir_path):
	# Navigate to the SCRIPTS/NUKE directory
	return True  # force true for now
	script_folder = os.path.join(shot_dir_path, "SCRIPTS", "NUKE")
	os.chdir(script_folder)

	# If the path contains '%04d', it's a sequence, so use glob to find it
	if "%04d" in relative_path:
		# Replace '%04d' with '*' for glob to match any files with that pattern
		fuzzy_path = relative_path.replace("%04d", "*")
		matching_files = glob.glob(fuzzy_path)

		if matching_files:
			# print(f"Found files: {matching_files}")
			return True
		else:
			log(f"File not found: {relative_path}", 'WARNING')
			return False

	# For non-sequence files
	exists = os.path.exists(relative_path)
	if exists:
		return True
	# print(f"Found file: {relative_path}")
	else:
		log(f"File not found: {relative_path}", 'ERROR')
		return False


def generate_relative_path(full_path, shot_dir_path):
	# Normalize the path to ensure it works on both Windows and Unix systems
	full_path = os.path.normpath(full_path)

	# Split the full path into its components
	path_parts = full_path.split(os.sep)

	# Get the directory of the full path to later construct an absolute path for checking
	dir_of_full_path = os.path.dirname(full_path)

	# Iterate through the path components to find the specified directory names
	log(f"Checking path: {full_path}", "DEBUG")
	for idx, part in enumerate(path_parts):
		if part in ["ASSETS", "EXPORTS", "SOURCE"]:
			log(f"Found directory: {part}", 'DEBUG')

			# Replace the left part with '../../' and join back into a string
			relative_path = os.path.join("../../", *path_parts[idx:])

			# Replace backslashes with forward slashes
			relative_path = relative_path.replace(os.sep, '/')

			# Use the function to check if the file exists
			if file_exists_from_relative_path(relative_path, shot_dir_path):
				log(f"Found relative path: {relative_path}", 'DEBUG')
				return relative_path

	# If none of the specified directory names are found, return None
	log(f'Could not find relative path for: {full_path}', 'WARNING')
	return None


def move_nonlocal_assets_to_plates_dir(file_path, shot_dir_path):
	log(f"Starting asset movement for file: {file_path}", 'DEBUG')

	whitelist = ["Read"]
	plates_dir = os.path.join(shot_dir_path, 'ASSETS', 'PLATES')
	log(f"Whitelisted nodes: {whitelist}", 'DEBUG')
	log(f"Plates directory: {plates_dir}", 'DEBUG')

	current_node = None
	should_replace = True

	def should_skip_based_on_path(full_path):
		log(f"Checking if path should be skipped: {full_path}", 'DEBUG')
		if "SOURCE" in full_path:
			log("Asset is a SOURCE file. Skipping.", 'DEBUG')
			return True
		elif any(keyword in full_path for keyword in ["EXPORTS", "ASSETS"]):
			log("Asset within shot. Skipping.", 'DEBUG')
			return True
		return False

	def handle_file_match(match, full_path):
		log(f"Handling file match for: {full_path}", 'DEBUG')
		file_exists = check_file_exists(full_path)
		if file_exists:
			create_directory_if_not_exists(plates_dir)
			destination_path = os.path.join(plates_dir, os.path.basename(full_path))
			copy_file_to_destination(full_path, destination_path)

			# Generate a new relative path
			new_relative_path = generate_relative_path(destination_path, shot_dir_path)
			log(f"File has been moved successfully and path changed to: {new_relative_path}", 'DEBUG')
			return f"file {new_relative_path}"
		return match.group(0)

	def replace_read_path(match):
		nonlocal current_node, should_replace
		last_index = match.lastindex

		if last_index == 1:
			current_node = match.group(1)
			should_replace = current_node in whitelist
		# log(f"Current node: {current_node}, Should replace: {should_replace}", 'DEBUG')
		elif last_index == 2 and should_replace:
			full_path = match.group(2)
			log(f"Full path for replacement: {full_path}", 'DEBUG')

			if should_skip_based_on_path(full_path):
				return match.group(0)

			return handle_file_match(match, full_path)

		return match.group(0)

	with open(file_path, 'r+') as f:
		log(f"Reading file: {file_path}", 'DEBUG')
		content = f.read()
		content = re.sub(r'(\w+) {|file (.+)', replace_read_path, content)
		f.seek(0)
		f.write(content)
		f.truncate()
		log(f"File {file_path} updated successfully", 'DEBUG')
