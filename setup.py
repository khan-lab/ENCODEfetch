from setuptools import setup, find_packages

setup(
    name="encodefetch",
    version="1.0.1",
    packages=find_packages(),
    install_requires=[
        "requests>=2.25.1",
        "pandas>=1.3.0",
        "click>=8.0.0",
        "rich>=13.0.0",
        "rich-click>=1.6.1",
        "tqdm>=4.60.0"
    ],
    entry_points={
        "console_scripts": [
            "encodefetch=encodefetch.cli:main"
        ]
    },
    author="Aziz Khan",
    author_email="azez.khan@gmail.com",
    description="ENCODEfetch: a command-line tool for retrieving matched case-control data and standardized metadata from ENCODE.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/khan-lab/ENCODEfetch",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
