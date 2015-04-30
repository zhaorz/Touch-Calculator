"""
setup.py
~~~~~~~~~~~~~~~
Uses py2app to build a standalone program.

Usage:
    python setup.py py2app
"""

from setuptools import setup

APP = ['main.py']
DATA_FILES = [
    ('', ['model']),
    ('', ['graphics'])
    ]
OPTIONS = {
    'argv_emulation': False,
    'iconfile': 'TouchCalculator.icns',
    'plist':dict(
        CFBundleName="Touch Calculator",
        CFBundleDisplayName="Touch Calculator",
        CFBundleVersion="1.1"
        )
    }

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
