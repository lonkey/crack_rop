"""Writes all gadgets to the MASTER_NAME.txt file"""
import lib.utils


def main(line, **kwargs):
    config = lib.utils.read_config()
    master_name = config["DEFAULT"]["master_name"]

    # Do not include the metadata in master
    if not line.startswith("rop"):
        return line
    output_dir_path = kwargs["output_dir_path"]
    file_path = output_dir_path.joinpath(master_name + ".txt")
    lib.utils.write_line(file_path, line)
    return line
