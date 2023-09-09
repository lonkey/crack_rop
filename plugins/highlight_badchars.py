"""Adds an indicator for addresses with bad chars"""
import re

import lib.utils


def main(line, **kwargs):
    if not kwargs["badchars"]:
        return line
    badchars = lib.utils.format_badchars(kwargs["badchars"])
    pattern = r"0x([0-9a-f]+): .*$"
    m = re.match(pattern, line)
    if m:
        if kwargs["use_offsets"] and kwargs["base_address"]:
            offset = int(m[1], 16)
            # Add the base address and the offset and format it as hex
            final_address = f"{(int(kwargs['base_address'], 16) + offset):08x}"
        else:
            final_address = m[1]
        address_chunks = lib.utils.chunk_it(final_address, 2)
        # Check if any of the badchars are in the address chunks
        matches = [i for i in badchars if i in address_chunks]
        if matches:
            addition = f"**** badchars: {', '.join(matches)} ****"
            line += addition
    return line
