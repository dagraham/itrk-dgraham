import os
import sys


def process_arguments():
    """
    Process sys.argv to get the necessary parameters, like the database file location.
    """
    backup_count = 7
    log_level = 20

    if len(sys.argv) > 1:
        try:
            log_level = int(sys.argv[1])
            sys.argv.pop(1)
        except ValueError:
            log_level = log_level

    envhome = os.environ.get("ITRKHOME")
    if len(sys.argv) > 1:
        itrk_home = sys.argv[1]
    elif envhome:
        itrk_home = envhome
    else:
        itrk_home = os.getcwd()

    backup_dir = os.path.join(itrk_home, "backup")

    md_path = os.path.join(itrk_home, "notes")

    restore = len(sys.argv) > 2 and sys.argv[2] == "restore"

    return trf_home, log_level, restore, backup_dir, db_path


# Get command-line arguments: Process the command-line arguments to get the database file location
itrk_home, log_level, restore, backup_dir, md_path = process_arguments()
