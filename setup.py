from setuptools import setup, find_packages

with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="httpcraft",
    version="0.1.0",
    author="subnetMusk",
    description="A minimal Python tool for crafting and inspecting HTTP requests",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/subnetMusk/httpcraft",
    packages=find_packages(),  # include httpcraft and httpcraft.tests
    install_requires=[
        "requests",
        "beautifulsoup4"
    ],
    extras_require={
        "dev": ["flask", "pytest"],
    },
    entry_points={
        "console_scripts": [
            "httpcraft = httpcraft.cli:main"
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent"
    ],
    python_requires='>=3.7',
)