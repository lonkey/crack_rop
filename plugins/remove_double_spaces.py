"""Replace double spaces with a single space."""


def main(line, **kwargs):  # pylint: disable=unused-argument
    return " ".join(line.split())
