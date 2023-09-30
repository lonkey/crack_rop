"""Sorts a file by line length ascending"""
import lib.utils


def build_index(file_path):
    """Builds a list of tuples of (line offset, line length)"""
    index = []
    with open(file_path, "r", encoding="utf-8") as f:
        while True:
            offset = f.tell()
            line = f.readline()
            if not line:
                break
            length = len(line)
            index.append((offset, length))
    index.sort(key=lambda x: x[1])
    return index


def sort_file(output_dir_path, file_name):
    print(f"Sorting {file_name}")
    # parent_dir = output_dir_path.parent.absolute()
    # file_path = output_dir_path.joinpath(file_name)
    source_file_path = output_dir_path.joinpath(file_name + ".txt")
    dest_file_path = output_dir_path.joinpath("_temp.txt")
    index = build_index(source_file_path)
    with open(source_file_path, "r", encoding="utf-8") as f:
        with open(dest_file_path, "w", encoding="utf-8") as g:
            for offset, length in index:
                f.seek(offset)
                content = f.read(length)
                g.write(content)
    # replace original with temp
    dest_file_path.replace(source_file_path)


def main(output_dir_path):
    config = lib.utils.read_config()
    sort_file(output_dir_path, config["DEFAULT"]["master_name"])
