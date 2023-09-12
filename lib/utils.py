import os
import sys
import shutil
import configparser
import subprocess


def lazy_read(*args, **kwargs):
    with open(*args, **kwargs) as file:
        yield from file


def delete_folder_contents(folder_path):
    """Deletes the contents of the output directory"""
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:  # pylint: disable=broad-exception-caught
            print(f"Failed to delete {file_path}. Reason: {e}")


def create_folder(parent_dir, binary_name, auto_delete):
    """Creates a folder for script output, returns folder path"""
    binary_name = binary_name.replace(".", "_")
    folder_path = parent_dir.joinpath(binary_name)
    try:
        os.mkdir(folder_path)
    except FileExistsError:
        if not auto_delete:
            print(
                (
                    f"\r*** Folder {folder_path} already exists. "
                    "I am going to erase all of its contents."
                )
            )
            input("Press enter to continue, otherwise Ctrl+C to exit.")
        delete_folder_contents(folder_path)
    return folder_path


def run_rp(data, gadget_size, use_offsets, encoding="utf-8"):
    config = read_config()
    command = f'{config["DEFAULT"]["rp_path"]} -f "{data["binary_path"]}" -r {gadget_size}'
    if use_offsets:
        command += " --va 0"
    print(f"Running: {command}")
    try:
        proc = subprocess.run(command, capture_output=True, check=True)
    except subprocess.CalledProcessError:
        print(
            "Error running RP++. Are you using a new(ish) version?"
            " Check the README for info. Exiting..."
        )
        sys.exit(-1)
    with open(data["output_path"], "w", encoding=encoding) as f:
        stdout = proc.stdout.decode().splitlines()
        for line in stdout:
            f.write(line + "\n")


def read_config():
    config = configparser.ConfigParser()
    config.read("config.ini")
    return config


def format_badchars(badchars: str) -> list:
    """Returns a list of bad characters from a string"""
    badchars_list = []
    if badchars:
        # remove the first empty list item
        temp = badchars.split("\\x")[1:]
    else:
        temp = []
    for entry in temp:
        badchars_list.append(entry.lower())
    return badchars_list


def chunk_it(orig, chunk_size):
    """Returns a list by breaking up a string into chunk_size items"""
    chunks = [orig[chunk : chunk + chunk_size] for chunk in range(0, len(orig), chunk_size)]  # noqa
    return chunks


def write_line(output_file_path, line, encoding="utf-8"):
    """Writes a single line to output file."""
    with open(output_file_path, "a", encoding=encoding) as f:
        f.write(line + "\n")
