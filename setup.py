from pathlib import Path

from setuptools import find_packages, setup

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

setup(
    name="simulateur_traffic_DBH",
    version="0.1.1",
    author="Dhia BEN HAMOUDA",
    author_email="dhiabenhamouda2002@gmail.com",
    description="Un simulateur de trafic pour étudier les comportements des véhicules.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(include=["simulateur_trafic", "simulateur_trafic.*"]),
    include_package_data=True,
    package_data={"simulateur_trafic": ["data/*.json"]},
    python_requires=">=3.10,<3.14",
)
