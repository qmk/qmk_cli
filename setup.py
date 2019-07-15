from configparser import ConfigParser
from setuptools import setup, find_packages

import toml

setup_cfg = ConfigParser()
setup_cfg.read('setup.cfg')
pyproject = toml.load('pyproject.toml')
metadata = pyproject['tool']['flit']['metadata']

if __name__ == "__main__":
    setup(
        name=metadata['dist-name'],
        description=open(metadata['description-file']).read(),
        entry_points={
            'console_scripts': ['%s = %s' % l for l in pyproject['tool']['flit']['scripts'].items()]
        },
        license='MIT License',
        url=metadata['home-page'],
        version=setup_cfg['bumpversion']['current_version'],
        author=metadata['author'],
        author_email=metadata['author-email'],
        maintainer=metadata['author'],
        maintainer_email=metadata['author-email'],
        long_description=open('README.md').read(),
        long_description_content_type="text/markdown",
        packages=find_packages(),
        classifiers=metadata['classifiers'],
        install_requires=metadata['requires'],
    )
