from distutils.core import setup
import setuptools

setup (
        # Application name:
        name="space-shooter-premraj59",

        # Version number (initial):
        version="0.1.0",

        #Application author details:
        author="Prem Raj",
        author_email="premraj59128@protonmail.com",

        #Packages
        packages=["app"],

        # Include additional files
        include_package_data=True,

        # Details
        url="https://github.com/premraj59/Space-Shooters-Pygame/",

        #
        # license="LICENSE.txt",
        description="Useful towel-related stuff.",

        # long_description=open("README.txt").read(),

        # Dependent packages (distributions)
        install_requires=[
            "pygame",
        ],
    )
