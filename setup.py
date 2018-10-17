import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="robotframework-load-balancer",
    version="0.0.1",
    author="Nico Mueller",
    author_email="nicomueller1991@googlemail.com",
    description="A robotframework test runner that distributes test to more then one system under test",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/niecore/robot-load-balancer",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Framework :: Robot Framework"
    ],
)