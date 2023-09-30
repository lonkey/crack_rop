"""
Creates a file of all Move/Copy Gadgets

This plugin is slow. This plugin will create a markdown file of just mov/copy gadgets
grouped by source -> dest. If the "highlight_badchars" plugin is enabled it will filter
out the gadgets with bad chars.

I use this and copy/paste the results to obsidian so I can have the Table of Contents
and quick access to the action I want.
"""
import re
import itertools

import lib.utils


REGEXS = [
    r".*mov {dest}, {source}(?!.*pop {dest}.*).*(?:ret[ ]*;|retn 0x00[012][0-9A-F][ ]*;).*",
    r".*lea {dest}, \[{source}(?:[\+-]0x.*?)?\].*(?:ret[ ]*;|retn 0x00[012][0-9A-F][ ]*;).*",
    r".*push {source}.*pop {dest}.*(?:ret[ ]*;|retn 0x00[012][0-9A-F][ ]*;).*",
    r".*(?:add|adc|xor|or|and|sub|sbb) {dest}, {source}(?!.*pop {dest}.*).*(?:ret[ ]*;|retn 0x00[012][0-9A-F][ ]*;).*",
    r".*xchg (?:{source}|{dest}), (?:{source}|{dest}).*(?:ret[ ]*;|retn 0x00[012][0-9A-F][ ]*;).*",
]
REGISTERS = ["eax", "ebx", "ecx", "edx", "esi", "edi", "ebp"]
PERMS = list(itertools.permutations(REGISTERS, 2))


def write_output(dest_file_path, findings):
    first = True
    with open(dest_file_path, "w", encoding="utf-8") as dest_f:
        for source in findings:
            first_source = True
            if first:
                dest_f.write(f"## {source.upper()}\n\n")
            else:
                dest_f.write(f"\n\n## {source.upper()}\n\n")
            first = False
            dest_f.write("### Move/Copy\n\n")
            for dest in findings[source]:
                if first_source:
                    dest_f.write(f"#### {source.upper()} -> {dest.upper()}\n\n")
                else:
                    dest_f.write(f"\n\n#### {source.upper()} -> {dest.upper()}\n\n")
                first_source = False
                dest_f.write("```python\n")
                dest_f.write("\n".join(findings[source][dest]))
                dest_f.write("\n```")


def main(output_dir_path):
    config = lib.utils.read_config()
    master_name = config["DEFAULT"]["master_name"]
    print(f"Finding Move/Copy in  {master_name}.txt")
    source_file_path = output_dir_path.joinpath(master_name + ".txt")
    dest_file_path = output_dir_path.joinpath("_move_copy.md")
    findings = {}
    with open(source_file_path, "r", encoding="utf-8") as f:
        content = f.read()
        for perm in PERMS:
            comb_matches = []
            source = perm[0]
            dest = perm[1]
            for regx in REGEXS:
                regx = re.compile(regx.format(source=source, dest=dest))
                matches = re.findall(regx, content)
                comb_matches += matches
            badwords = ["badchars", "esp", "call"]
            filtered_matches = [
                item for item in comb_matches if all(x not in item for x in badwords)
            ]
            if filtered_matches:
                if findings.get(source):  # source already exists
                    if findings[source].get(dest):  # dest already exists
                        # We add to existing dest
                        findings[source][dest] += sorted(filtered_matches, key=len)
                    else:
                        # We establish dest
                        findings[source][dest] = sorted(filtered_matches, key=len)
                else:
                    # We establish source
                    findings[source] = {dest: sorted(filtered_matches, key=len)}
    write_output(dest_file_path, findings)
