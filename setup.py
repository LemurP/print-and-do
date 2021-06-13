from glob import glob
from os.path import splitext, basename

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pado",
    version="0.0.0",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/lemurp/print-and-do',
    packages=setuptools.find_packages('src'),
    package_dir={'': 'src'},
    py_modules=[splitext(basename(path))[0] for path in glob('src/*.py')],
    install_requires=[
        'click >= 8.0',
        'rich >= 10',
        'appdirs >= 1.4.4'
    ],
    extras_require={
        'dev': [
            'click >= 8.0',
            'colorama==0.4.4',
            'commonmark==0.9.1',
            'Pygments==2.8.1',
            'rich==10.1.0',
            'typing-extensions==3.7.4.3',
            'appdirs >= 1.4.4'
        ]
    },
    entry_points={
        'console_scripts': [
            'pado = pado.cli:main',
        ]
    },
    license='OSI Approved :: Apache Software License',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
)
