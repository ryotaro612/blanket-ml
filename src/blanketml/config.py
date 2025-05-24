import tomllib


def load(config_path: str) -> dict:
    """
    Load a configuration file from the given path.

    Args:
        config_path (str): The path to the configuration file.

    Returns:
        dict: The loaded configuration as a dictionary.
    """

    with open(config_path, "rb") as f:
        config = tomllib.load(f)
        return config
