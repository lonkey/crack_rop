"""Writes all gadgets to the MASTER_NAME.txt file"""
import lib.utils


def main(line, **kwargs):
    config = lib.utils.read_config()
    master_name = config["DEFAULT"]["master_name"]

    # Do not include the metadata in master
    if not line.startswith("rop"):
        return line
    output_dir_path = kwargs["output_dir_path"]
    parent_dir = output_dir_path.parent.absolute()
    master_path = parent_dir.joinpath(master_name)
    file_path = master_path.joinpath(master_name + ".txt")
    lib.utils.write_line(file_path, line)
    return line
