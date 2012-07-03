"""
jQuery Package Manager -- Plugin server mock
Setup file
"""
import sys

from setuptools import setup, find_packages


if 'register' in sys.argv or 'upload' in sys.argv:
    raise Exception("jqpmserver is just a mock for testing jqpm "
                    "and should not be on PyPI!")


setup(
    name="jqpmserver",
    description="Mock server for testing jQuery Package Manager",
    license='BSD',
    version='0.1',
    author='Karol Kuczmarski "Xion"',
    author_email="karol.kuczmarski@gmail.com",

    install_requires=[
        'Flask',
        'requests',
        'python-dateutil',
    ],

    packages=find_packages(),
    entry_points={'console_scripts': ['jqpmserver=jqpmserver:main']},
)
