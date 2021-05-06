"""An experimental package for a buziness segument project."""
from setuptools import setup, find_packages

setup(
    name="beat_analytics",
    version="0.0.1",
    packages=find_packages(exclude=["tests", "tests.*"]),
    install_requires=["click", "google-cloud-bigquery", "python-dotenv", "jsonlines"],
    entry_points={"console_scripts": ["beat_analytics=beat_analytics:main"]},
    extras_require={
        "dev": ["black", "ipython"],
    },
)
