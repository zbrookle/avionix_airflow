from distutils.core import setup
from pathlib import Path

from setuptools import find_packages

import versioneer

CODE_DIRECTORY = Path(__file__).parent


def read_file(file_path: Path):
    """Source the contents of a file"""
    with open(str(file_path), encoding="utf-8") as file:
        return file.read()


setup(
    name="avionix_airflow",
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    packages=find_packages(),
    long_description=read_file(CODE_DIRECTORY / "README.rst"),
    maintainer="Zach Brookler",
    maintainer_email="zachb1996@yahoo.com",
    description="A package for deploying airflow to kubernetes with included "
    "monitoring (grafana and elasticsearch integration)",
    python_requires=">=3.6.1",
    install_requires=[read_file(CODE_DIRECTORY / "requirements.txt").split("\n")],
    project_urls={
        "Source Code": "https://github.com/zbrookle/avionix_airflow",
        "Documentation": "https://github.com/zbrookle/avionix_airflow",
        "Bug Tracker": "https://github.com/zbrookle/avionix_airflow/issues",
    },
    url="https://github.com/zbrookle/avionix_airflow",
    download_url="https://github.com/zbrookle/avionix_airflow/archive/master.zip",
    keywords=[
        "kuberenetes",
        "helm",
        "docker",
        "infrastructure",
        "airflow",
        "grafana",
        "elasticsearch",
        "filebeat",
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 3.7",
        "Typing :: Typed",
        "Operating System :: OS Independent",
    ],
    long_description_content_type="text/x-rst",
    include_package_data=True,
)
