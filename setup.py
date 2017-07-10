from setuptools import setup,find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))
vers = 'dev' 

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
        name='borgstractor',
        version=vers,

        description='Interactive wrapper for extracting files from borg archives',
        long_description=long_description,

        url='https://github.com/rickh94/borgstractor.git',
        author='Rick Henry',
        author_email='fredericmhenry@gmail.com',

        license='GPLv3',
        python_requires='>=3',

        packages=find_packages(),

        entry_points={
            'console_scripts': [
                'borgstractor = borgstractor.borgstractor:main',
                ],
            },
        )
        


