"""
Setup script for Hybrid BCI Wheelchair package
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

setup(
    name="hybrid-bci-wheelchair",
    version="1.0.0",
    author="Arvind Gyandatt Mishra, Poonam Chawda, Heeral Dedhia, Arvind Sridhar",
    author_email="",
    description="Hybrid Brain-Computer Interface system for wheelchair control",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/NeuArv/hybrid-bci-wheelchair",
    project_urls={
        "Bug Tracker": "https://github.com/NeuArv/hybrid-bci-wheelchair/issues",
        "Documentation": "https://github.com/NeuArv/hybrid-bci-wheelchair/tree/master/docs",
        "Source Code": "https://github.com/NeuArv/hybrid-bci-wheelchair",
    },
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Healthcare Industry",
        "Topic :: Scientific/Engineering :: Human Machine Interfaces",
        "Topic :: Scientific/Engineering :: Medical Science Apps.",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: POSIX :: Linux",
    ],
    python_requires=">=3.7",
    install_requires=[
        "pyserial>=3.5",
    ],
    extras_require={
        "rpi": ["RPi.GPIO>=0.7.1"],
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=3.0.0",
            "black>=22.0.0",
            "flake8>=4.0.0",
            "mypy>=0.950",
        ],
        "data": [
            "numpy>=1.21.0",
            "pandas>=1.3.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "hybrid-bci-demo=scripts.run_demo:main",
            "hybrid-bci-blink=scripts.blink_control_demo:main",
            "hybrid-bci-test=scripts.test_sensors:main",
        ],
    },
    keywords=[
        "BCI",
        "brain-computer-interface",
        "EEG",
        "wheelchair",
        "assistive-technology",
        "neurosky",
        "mindwave",
        "raspberry-pi",
    ],
)
