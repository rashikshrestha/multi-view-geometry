from setuptools import setup, find_packages

setup(
    name="multi-view-geometry",
    version="0.1.0",
    author="Rashik Shrestha",
    author_email="rashikshrestha01@gmail.com",
    description="Open Source Library with common utility functions for Multi View Geometry problems.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/rashikshrestha/multi-view-geometry",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    license="Apache License 2.0",
    python_requires=">=3.6",
    install_requires=[
        "numpy",
        "plotly"
    ],
)