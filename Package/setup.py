import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="RedPy",
    version="0.0.4",
    author="Prashant Sengar",
    author_email="prashantsengar5@gmail.com",
    description="A Python package to download images from Reddit",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/prashantsengar/RedPy",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=['requests', 'fake-useragent'],
)
