#! /usr/bin/env python3

import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="podiff2",
    version="0.0.1",
    author="eshagh",
    author_email="eshagh094@gmail.com",
    description="compare two .po/gettext files for differences ",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/eshagh79/podiff2",
    project_urls={
        "Bug Tracker": "https://github.com/eshagh79/podiff2/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
    ],
    keywords='po gettext compare diff',
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    install_requires=['polib'],
    python_requires=">=3.6",
    entry_points={
        "console_scripts": [
            "podiff2 = podiff2.podiff:main",
        ],
    },
)
