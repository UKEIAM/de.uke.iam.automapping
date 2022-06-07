#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from __future__ import absolute_import
from __future__ import print_function

from setuptools import find_packages
from setuptools import setup

with open("requirements.txt", "r", encoding="utf-8") as requirements:
    setup(
        name="automapping",
        version="0.0.1",
        description="Map free text columns automatically into medical standards",
        author="Christopher Gundler",
        author_email="c.gundler@uke.de",
        url="https://github.com/UKEIAM/de.uke.iam.automapping",
        package_dir={"": "src"},
        packages=find_packages(where="src"),
        include_package_data=True,
        zip_safe=True,
        python_requires=">=3.8",
        install_requires=requirements.readlines(),
        setup_requires=[
            "pytest-runner",
        ],
    )
