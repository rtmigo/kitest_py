from pathlib import Path

from setuptools import setup, find_packages

name = "tempp"

setup(
    name=name,
    version="0.1.2",

    author="Artёm IG",
    author_email="ortemeo@gmail.com",

    packages=find_packages(include=['tempp', 'tempp.*']),
    package_data={'tempp': ['data' + ('/*' * i) for i in range(20)]},

    python_requires='>=3.10',
    install_requires=[],

    long_description=(Path(__file__).parent / 'README.md')
        .read_text(encoding="utf-8"),
    long_description_content_type='text/markdown',

    license="MIT",

    keywords="testing kotlin java library ci integration".split(),

    classifiers=[
        "Programming Language :: Python :: 3.10",
        "Environment :: Console",
        "Typing :: Typed",
        "Operating System :: POSIX",
        "Operating System :: Microsoft :: Windows"
    ],
)

