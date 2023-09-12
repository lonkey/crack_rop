"""
Entrypoint for crack_rop
"""
import sys
from pathlib import Path

import lib.utils
import lib.options
import lib.parsenmod
import lib.formatrp


def main(args):
    # Sanity Checks
    if not Path("config.ini").is_file():
        print(
            "Cound not find config file. Try copying"
            "'config.ini.sample' to 'config.ini'. Exiting..."
        )
        sys.exit(-1)

    config = lib.utils.read_config()
    input_file = Path(args.input_file)

    rp_path = Path(config["DEFAULT"]["rp_path"])
    if not rp_path.is_file():
        print(f"Could not find rp++: {rp_path}")
        sys.exit(-1)

    if not input_file.is_file():
        print(f"Could not open input file: {input_file}")
        sys.exit(-1)

    # Parse nmod
    pn = lib.parsenmod.ParseNmod(args)

    if len(pn.parsed_data) == 0:
        print("Could not find any binaries that satisfy the requirements... Exiting")
        sys.exit(-1)

    # Run RP++ for each binary
    for binary_data in pn.parsed_data:
        lib.utils.run_rp(binary_data, args.gadget_size, args.use_offsets)

    # Create master output folder
    lib.utils.create_folder(pn.parent_dir, config["DEFAULT"]["master_name"], args.auto_delete)

    # Format rp++ output
    lib.formatrp.Format_RP(args, pn.parsed_data)


if __name__ == "__main__":
    _args = lib.options.parse_args()
    main(_args)
