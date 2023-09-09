"""Create a file for each type of clean gadget I find"""
import re


# Immediate values are hex values that will be used to check for instructions.
# For example, if I am looking for an immediate value of 0x40. I enter '0x40' into
# this global variable. The script will search for stuff like:
# `mov eax, 0x00000040 ; ret`
IMMEDIATE_VALUES = [0x0, 0x1, 0x4, 0x1C, 0x40, 0x1000, 0xFFFFFFFF]

# GADGETS is a list of dictionaries. Each dictionary will create a file with the
# name of the value of 'file_name'. The regexs are a list that are used to find
# clean gadgets.
# Any found gadgets are in a file with the name of "`file_name`.txt"
GADGETS = [
    {
        "file_name": "add_adc",
        "regexs": [r"# (?:add|adc) (?:e..|[abcd][hl]), (?:e..|{key_values}); ret"],
    },
    {
        "file_name": "and_or",
        "regexs": [r"# (?:or|and) (?P<dest>e..), (?!\1)(?:e..|{key_values}); ret"],
    },
    {"file_name": "dec", "regexs": [r"# dec e..; ret"]},
    {"file_name": "inc", "regexs": [r"# inc e..; ret"]},
    {
        "file_name": "mul_imul",
        "regexs": [
            r"# (?:mul|imul) e.., (?:e..|{key_values}); ret",
            r"# (?:mul|imul) e..; ret",
        ],
    },
    {
        "file_name": "lea",
        "regexs": [r"# lea (?P<dest>e..), (?:dword )?\[(?!\1)e..\]; ret"],
    },
    {"file_name": "mov", "regexs": [r"# mov (?:e..|..), (?:e..|..|{key_values}); ret"]},
    {
        "file_name": "mov_deref_dest",
        "regexs": [r"# mov (?:dword )?\[(?P<dest>e..)\], (?!\1)e..; ret"],
    },
    {
        "file_name": "mov_deref_src",
        "regexs": [
            r"# mov (?P<dest>e..), (?:dword )?\[(?!\1)e..\]; ret",
        ],
    },
    {"file_name": "neg_not", "regexs": [r"# (?:neg|not) e..; ret"]},
    {"file_name": "pop", "regexs": [r"# pop e..; ret"]},
    {"file_name": "push", "regexs": [r"# push (?:e..|{key_values}); ret"]},
    {
        "file_name": "sub_sbb",
        "regexs": [r"# (?:sub|sbb) e.., (?:e..|{key_values}); ret"],
    },
    {"file_name": "xchg", "regexs": [r"# xchg e.., e..; ret"]},
    {"file_name": "xor", "regexs": [r"# xor e.., e..; ret"]},
    {
        "file_name": "esp",
        "regexs": [
            r"(?!.*pop esp)# push esp; pop e..; ret",
            r"(?=.*esp)# xchg e.., e..; ret",
            r"# (?:add|adc|sub|sbb) esp, (?:0x[0-9a-fA-F]{2,8}|\[e..\]); ret",
        ],
    },
]

FOUND = {}


def main(line, **kwargs):
    output_dir_path = kwargs["output_dir_path"]
    # No large retn's
    if ("retn 0x" in line) and ("retn 0x00" not in line):
        return line
    key_values = set()
    for value in IMMEDIATE_VALUES:
        key_values.add(f"0x{value:02x}")
        key_values.add(f"0x{value:04x}")
        key_values.add(f"0x{value:08x}")
    for item in GADGETS:
        output_path = output_dir_path.joinpath(f"{item['file_name']}.txt")
        for regex in item["regexs"]:
            if "{key_values}" in regex:
                regex = regex.format(key_values="|".join(key_values))
            s = re.search(regex, line)
            if s:
                if FOUND.get(item["file_name"]):
                    FOUND[item["file_name"]].append(line)
                else:
                    FOUND[item["file_name"]] = [line]
                with open(output_path, "a", encoding="utf-8") as f:
                    f.write(line + "\n")
    return line
