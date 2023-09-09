"""Changes address column so that it can be copied into python easily"""
import re


def main(line, **kwargs):  # pylint: disable=unused-argument
    library_name = kwargs["binary_name"].split(".")[0]
    pattern = r"(0x[0-9a-f]+): (.*)$"
    m = re.match(pattern, line)
    if m:
        address = m[1]
        instructions = m[2]
        if kwargs["use_offsets"]:
            line = f"rop += p32({library_name}_ba + {address})  # {instructions}"
        else:
            line = f"rop += p32({address})  # {instructions}"
    return line
