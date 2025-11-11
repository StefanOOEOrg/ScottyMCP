"""Setup script for TransitMCP."""

from setuptools import setup, find_packages

setup(
    name="transitmcp",
    version="0.2.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.10",
    install_requires=[
        "mcp>=1.2.0",
        "pyhafas>=0.4.0",
    ],
    entry_points={
        "console_scripts": [
            "transitmcp=transitmcp.server:main",
        ],
    },
)
