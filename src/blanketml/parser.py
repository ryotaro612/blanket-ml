import argparse
import typing


class Command(typing.TypedDict):
    config_file: str

def parse(args: list[str]) -> Command:
    """Parse command line arguments."""
    return {'config_file': args[0]} 