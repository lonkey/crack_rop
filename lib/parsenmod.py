"""
Parses nmod output
"""
import re
import sys
from pathlib import Path


class ParseNmod:
    """
    Class for parsing nmod
    """

    def __init__(self, args):
        self.allow_null = args.allow_null
        self.allow_aslr = args.allow_aslr
        self.allow_dep = args.allow_dep
        self.require_safe_seh_off = args.require_safe_seh_off
        self.input_file = Path(args.input_file)
        self.parent_dir = self.input_file.parent.absolute()
        self.parsed_data = self.read_nmod()

    def read_input(self):
        lines = []
        with open(self.input_file, "r", encoding="utf-8") as f:
            read_lines = f.read().splitlines()
        for line in read_lines:
            # Filter any lines that are blank
            if len(line) == 0:
                continue
            # Allows me to comment out lines
            if line.startswith("#"):
                continue
            lines.append(line)
        return lines

    def parse_line(self, line):
        parts = line.split()
        base_address = parts[0]
        safe_seh_off = parts[4] == "OFF"
        has_aslr = "*ASLR" in line
        has_dep = "*DEP" in line
        library_name = parts[2]

        pattern = r".*(C:\\.*)$"
        m = re.match(pattern, line)
        if not m:
            print(f"Could not find a binary path for line:\r{line}")
            sys.exit(-1)
        binary_path = Path(m[1])
        output_file_name = binary_path.parts[-1].split(".")[0].lower() + ".txt"
        output_dir = self.parent_dir.joinpath("output")
        output_file_path = output_dir.joinpath(output_file_name)
        return {
            "base_address": base_address,
            "binary_path": binary_path,
            "safe_seh_off": safe_seh_off,
            "has_aslr": has_aslr,
            "has_dep": has_dep,
            "output_path": output_file_path,
            "library_name": library_name,
        }

    def read_nmod(self):
        lines = self.read_input()
        valid_lines = []
        for line in lines:
            data = self.parse_line(line)
            if data["base_address"].startswith("00") and not self.allow_null:
                continue
            if data["has_aslr"] and not self.allow_aslr:
                continue
            if data["has_dep"] and not self.allow_dep:
                continue
            if not data["safe_seh_off"] and self.require_safe_seh_off:
                continue
            if not len(line) > 0:
                continue
            valid_lines.append(line)
        data = []
        for line in valid_lines:
            data.append(self.parse_line(line))
        return data
