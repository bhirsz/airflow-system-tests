# Copyright 2022 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import io
import os

import setuptools

name = "composer-system"
module_name = "composer_system"
description = "Run Composer system tests in CI"
release_status = (
    "Development Status :: 3 - Alpha"  # see https://pypi.org/classifiers/
)
dependencies = [
    "click>=7.0",
    "google-auth==1.30.*",
    "google-cloud-build",
    "rich_click==1.4.0",
]
# extras = {
#     "tests": [
#         "pytest",
#         "nox",
#     ],
#     "dev": [
#         "pre-commit",
#     ],
# }

package_root = os.path.abspath(os.path.dirname(__file__))
packages = setuptools.find_packages(exclude=("tests",))

with io.open("README.md", "r") as fh:
    long_description = fh.read()

version = {}
with open(os.path.join(package_root, f"{module_name}/version.py")) as fp:
    exec(fp.read(), version)
version = version["__version__"]

setuptools.setup(
    name=name,
    version=version,
    description=description,
    # author="Google", # TODO:
    # author_email="theaflowers@google.com", # TODO:
    license="Apache 2.0",
    # url='',  # TODO: (b/226562556): Fill missing metadata
    keywords="google airflow composer tests",
    classifiers=[
        release_status,
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent",
        "Topic :: Internet",
    ],
    platforms="Posix; MacOS X; Windows",
    packages=packages,
    python_requires=">=3.7",
    install_requires=dependencies,
    # extras_require=extras,
    include_package_data=True,
    zip_safe=False,
    entry_points={
        "console_scripts": f"{name}={module_name}.__main__:cli",
    },
)
