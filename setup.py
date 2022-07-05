import setuptools
import os

os.system("pip install git+https://github.com/openai/CLIP.git") 



setuptools.setup(
    name="ZSIClight",
    version="1.0",
    author="sam-shridhar1950f",
    author_email="",
    description="Zeroshot Image Classification Light",
    long_description="Zero Shot Image Classification (Lighweight Version) Version 2",
    url="https://github.com/sam-shridhar1950f/ZSIClight.git",
    packages=setuptools.find_packages(),
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: MIT",
        "Operating System :: OS Independent",
    ],
)
