import setuptools

with open("readme.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="PyCharmSync",
    version="0.0.1",
    author="py-am-i",
    author_email="duckpuncherirl@gmail.com",
    description="PyCharmSync is a simple tool for uploading changed project files to a remote host, about as soon as they change.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Wykleph/PyCharmSync",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
