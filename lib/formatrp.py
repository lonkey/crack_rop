import sys
import importlib
from pathlib import Path

import lib.utils


class Format_RP:
    def __init__(self, args, parsed_data):
        self.badchars = args.badchars
        self.parsed_data = parsed_data
        self.auto_delete = args.auto_delete
        self.use_offsets = args.use_offsets

        parent_dir = Path(args.input_file).parent.absolute()
        self.parent_dir = parent_dir.joinpath("output")

        self.config = lib.utils.read_config()

        config_line_plugins = self.config["DEFAULT"]["enabled_line_plugins"].splitlines()
        self.enabled_line_plugins = [i for i in config_line_plugins if i]
        self.line_plugin_modules = []
        for enabled in self.enabled_line_plugins:
            self.line_plugin_modules.append(importlib.import_module("plugins." + enabled))

        config_post_plugins = self.config["DEFAULT"]["enabled_post_plugins"].splitlines()
        self.enabled_post_plugins = [i for i in config_post_plugins if i]
        self.post_plugin_modules = []
        for enabled in self.enabled_post_plugins:
            self.post_plugin_modules.append(importlib.import_module("plugins." + enabled))

        self.format_files()

    def format_line(self, line, output_dir_path, binary_name, **kwargs):
        """
        Formats a single line
        """
        for plugin in self.line_plugin_modules:
            main = getattr(plugin, "main")
            line = main(
                line,
                badchars=self.badchars if self.badchars else None,
                output_dir_path=output_dir_path,
                binary_name=binary_name,
                use_offsets=kwargs["use_offsets"],
                base_address=kwargs["base_address"],
                auto_delete=kwargs["auto_delete"],
            )
        return line

    def format_file(self, binary_data, encoding="utf-8"):
        """
        Formats a single file
        """
        parent_dir = binary_data["output_path"].parent.absolute()
        binary_name = binary_data["binary_path"].name
        output_path = parent_dir.joinpath(binary_name + self.config["DEFAULT"]["formatted_name"])
        master_path = parent_dir.joinpath(self.config["DEFAULT"]["master_name"] + ".txt")

        print(f"Formatting {binary_name}, writing output to {output_path}")

        lib.utils.delete_file(output_path, self.auto_delete)
        lib.utils.delete_file(master_path, self.auto_delete)

        for line in lib.utils.lazy_read(binary_data["output_path"], encoding=encoding):
            line = self.format_line(
                line.strip(),
                parent_dir,
                binary_name,
                use_offsets=self.use_offsets,
                base_address=binary_data["base_address"],
                auto_delete=self.auto_delete,
            )
            lib.utils.write_line(output_path, line)

    def format_files(self):
        """
        Formats all files
        """
        for binary_data in self.parsed_data:
            self.format_file(binary_data)

        for plugin in self.post_plugin_modules:
            main = getattr(plugin, "main")
            main(output_dir_path=self.parent_dir)
