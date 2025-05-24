from blanketml import parser


def main(args: list[str]) -> None:
    """
    Main function to parse command line arguments and execute the parser.

    Args:
        args (list[str]): List of command line arguments.
    """
    res = parser.parse(args)
    print(res)
