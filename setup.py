import subprocess
from pathlib import Path

from setuptools import find_packages, setup
from setuptools.command.install import install

from _version import __version__

script = f"""
chmod +x auto_runner.py
mkdir -p {Path.home()}/bin/
cp auto_runner.py {Path.home()}/bin/auto-runner
"""


class PostInstallCommand(install):
    """Pre-installation for installation mode."""

    def run(self):
        super().run()
        print("Running post install script")
        for cmd in script.split("\n"):
            if cmd.strip():
                subprocess.run(cmd, shell=True, check=True)


setup(
    name="auto_runner",
    version=__version__,
    author="André Graça",
    author_email="andrepgraca+github_auto_runner@gmail.com",
    description=open("README.md").read(255),
    long_description=open("README.md").read(),
    platforms="Python",
    packages=find_packages(),
    install_requires=[
        "animations @ git+https://github.com/AndreGraca98/console-animations.git"
    ],
    cmdclass={
        "install": PostInstallCommand,
    },
)
