"""Add the source binary name to the line"""


def main(line, **kwargs):
    line += f" ({kwargs['binary_name']})"
    return line
