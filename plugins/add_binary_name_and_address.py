"""Add the source binary and the absolute address to the gadget"""
import re


def main(line, **kwargs):
    line += f" ({kwargs['binary_name']}"
    pattern = r"0x([0-9a-f]+): .*$"
    m = re.match(pattern, line)
    if m and kwargs["use_offsets"] and kwargs["base_address"]:
        offset = int(m[1], 16)
        # Add the base address and the offset and format it as hex
        final_address = f"{(int(kwargs['base_address'], 16) + offset):08x}"
        line += f":0x{final_address}"
    line += ")"
    return line
