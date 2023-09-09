"""Remove the space before ';'"""


def main(line, **kwargs):  # pylint: disable=unused-argument
    line = line.replace(" ;", ";")
    return line
