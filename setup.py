import setuptools
import os

os.system("pip install git+https://github.com/openai/CLIP.git") 
os.system("pip install sentence-transformers")


setuptools.setup(
    name="ZSIClite",
    version="1.0",
    author="sam-shridhar1950f",
    author_email="",
    description="Zeroshot Image Classification Lite",
    long_description="Zero Shot Image Classification (Lighweight Version)",
    url="https://github.com/sam-shridhar1950f/ZSIClite.git",
    packages=setuptools.find_packages(),
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: MIT",
        "Operating System :: OS Independent",
    ],
)