from setuptools import setup, find_packages

# Read the contents of requirements.txt
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name="cohda_driver",
    version="0.1.0",
    # author="Your Name",
    # author_email="your.email@example.com",
    # description="A brief description of your project",
    # url="https://github.com/yourusername/cohda_driver",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=8.2.2",
            "pylint>=2.3.1",
        ],
    },
)
