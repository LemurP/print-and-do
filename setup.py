import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="print-and-do",
    version="0.1",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_namespace_packages(exclude=['test']),
    install_requires=[
        'click >= 7.0',
        'rich >= 10',
    ],
    license='OSI Approved :: Apache Software License',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
)