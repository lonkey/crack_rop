"""
Argument Parser
"""
import argparse


def parse_args():
    parser = argparse.ArgumentParser(
        prog="parse_nmod.py",
        description="Parse nmod output and run rp++ on each.",
        epilog="Example: python crack_rop.py modules.txt",
    )
    parser.add_argument(
        "-g",
        "--gadget_size",
        type=int,
        default=5,
        help="Maximum gadget size, default is 5",
    )
    parser.add_argument(
        "-n",
        "--allow_null",
        default=False,
        help="Allow the address to start with '00', default is False",
        action="store_true",
    )
    parser.add_argument(
        "-a",
        "--allow_aslr",
        default=False,
        help="Allow binaries protected by ASLR, default is False",
        action="store_true",
    )
    parser.add_argument(
        "-d",
        "--allow_dep",
        default=False,
        help="Allow binaries protected by DEP, default is False",
        action="store_true",
    )
    parser.add_argument(
        "-s",
        "--require_safe_seh_off",
        default=False,
        help="Only include binaries where SafeSEH is OFF, default is False",
        action="store_true",
    )
    parser.add_argument(
        "-x",
        "--auto-delete",
        default=False,
        action="store_true",
        help="Will not ask before deleting existing folders, default is False.",
    )
    parser.add_argument("-b", "--badchars", type=str, help="Bad Characters (format: '\\x00\\x0a')")
    parser.add_argument(
        "-o",
        "--use-offsets",
        default=False,
        action="store_true",
        help="Will use offsets instead of exact addresses.",
    )
    parser.add_argument("input_file", type=str, help="Path to nmod output file.")
    return parser.parse_args()
