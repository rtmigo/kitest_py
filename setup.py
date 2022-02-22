from pathlib import Path

from setuptools import setup, find_packages

name = "kitest"

readme = (Path(__file__).parent / 'README.md').read_text(encoding="utf-8")

setup(
    name=name,
    version="0.0.0",

    author="Artёm IG",
    author_email="ortemeo@gmail.com",

    packages=find_packages(include=['kitest', 'kitest.*']),
    package_data={'kitest': ['data/**/*']},

    python_requires='>=3.10',
    install_requires=[],

    long_description=readme,
    long_description_content_type='text/markdown',

    license="MIT",

    entry_points={
        'console_scripts': [
            'kitest = kitest:__main__.cli',
        ]},

    keywords="".split(),

    classifiers=[
        "Programming Language :: Python :: 3.10",
        "Environment :: Console",
        "Typing :: Typed",
        "Operating System :: POSIX",
        "Operating System :: Microsoft :: Windows"
    ],
)
