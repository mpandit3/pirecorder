#! /usr/bin/env python
#
# Controlled media recording library for the Rasperry-Pi
# Copyright (c) 2018-2019 Jolle Jolles <j.w.jolles@gmail.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at:
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import print_function
from setuptools import setup, find_packages
import sys

exec(open('animrec/__version__.py').read())


DESCRIPTION = """
A python module for controlled and automated image and video recording
"""
LONG_DESCRIPTION = """\
AnimRec is a python package designed to help facilitate controlled and
automated image and video recording, especially on the raspberry pi, with the
behavioural scientist in mind.
"""

DISTNAME = 'animrec'
MAINTAINER = 'Jolle Jolles'
MAINTAINER_EMAIL = 'j.w.jolles@gmail.com'
URL = 'http://jollejolles.com'
DOWNLOAD_URL = 'https://github.com/JolleJolles/animrec'
LICENSE = 'Apache Software License 2.0'


def check_dependencies():
    install_requires = []

    # Make sure dependencies exist
    try:
        import crontab
        crontab.CronTab(user = "")
    except:
        install_requires.append('python-crontab')
    try:
        import croniter
    except ImportError:
        install_requires.append('croniter')
    try:
        import cron_descriptor
    except ImportError:
        install_requires.append('cron-descriptor')
    try:
        import socket
    except ImportError:
        install_requires.append('socket')
    try:
        import yaml
    except ImportError:
        install_requires.append('pyyaml')
    try:
        import future
    except ImportError:
        install_requires.append('future')
    try:
        import localconfig
    except ImportError:
        if sys.version_info[0] == 2:
            install_requires.append('localconfig==0.4.2')
        if sys.version_info[0] == 3:
            install_requires.append('localconfig')
    try:
        import animlab
    except ImportError:
        print("Package animlab is required. To install development version:")
        print("pip install git+https://github.com/JolleJolles/animlab.git")

    return install_requires


if __name__ == "__main__":

    install_requires = check_dependencies()

    setup(name=DISTNAME,
          author=MAINTAINER,
          author_email=MAINTAINER_EMAIL,
          maintainer=MAINTAINER,
          maintainer_email=MAINTAINER_EMAIL,
          description=DESCRIPTION,
          long_description=LONG_DESCRIPTION,
          url=URL,
          entry_points={
                     'console_scripts': ['ar_calib = animrec.calibrate:Calibrate',
                     'rec = animrec.rec:rec'],
          },
          download_url=DOWNLOAD_URL,
          version=__version__,
          install_requires=install_requires,
          packages=find_packages(),
          include_package_data=True,
          classifiers=[
                     'Intended Audience :: Science/Research',
                     'Programming Language :: Python :: 2.7',
                     'Programming Language :: Python :: 3',
                     'License :: OSI Approved :: Apache Software License',
                     'Topic :: Scientific/Engineering :: Visualization',
                     'Topic :: Scientific/Engineering :: Image Recognition',
                     'Topic :: Scientific/Engineering :: Information Analysis',
                     'Topic :: Multimedia :: Video'
                     'Operating System :: POSIX',
                     'Operating System :: Unix',
                     'Operating System :: MacOS'],
          )
