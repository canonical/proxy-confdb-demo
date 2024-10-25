from setuptools import setup

setup(
    name="browser",
    description="Snap that consumes proxy config",
    version="0.1",
    author="Stephen Mwangi",
    license="MIT",
    python_requires=">=3.10",
    packages=["browser"],
    entry_points={
        "console_scripts": ["browser-cli=browser.main:main"],
    },
)
