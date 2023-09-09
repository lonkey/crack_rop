"""Remove the '(1 found)' string"""


def main(line, **kwargs):  # pylint: disable=unused-argument
    line = line.replace(" (1 found)", "")
    return line
