import argparse

import config
from bulk_process_shots import bulk_process_shots
from bulk_restore_backups import bulk_restore_backups
from logs import log, set_level


def main():
	parser = argparse.ArgumentParser(description='Bulk processing of shots or restoring backups')
	parser.add_argument('-restore', '-r', action='store_true', help='Restore backups instead of processing shots')
	parser.add_argument('-shots', '-s', help='Path to SHOTS directory')
	parser.add_argument('-move_assets', '-a', action='store_true', help='Move assets to PLATES directory')
	parser.add_argument('-loglevel', '-l', help='Set the log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)')
	args = parser.parse_args()

	should_move_assets = args.move_assets or False

	if args.loglevel:
		config.log_level = args.loglevel
		set_level(args.loglevel)

	if args.shots:
		shots_dir_path = args.shots
		if args.restore:
			bulk_restore_backups(shots_dir_path)
		else:
			bulk_process_shots(shots_dir_path, should_move_assets)
	else:
		log("Please provide a path to the SHOTS directory with -shots=PATH_TO_SHOTS", 'ERROR')


if __name__ == '__main__':
	main()
