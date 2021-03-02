from configparser import ConfigParser
from setuptools import setup, find_packages

setup_cfg = ConfigParser()
setup_cfg.read('setup.cfg')
metadata = setup_cfg['metadata']

if __name__ == "__main__":
    with open('README.md', encoding='utf-8') as readme_file:
        long_description=readme_file.read()
    setup(
        name=metadata['dist-name'],
        description='A program to help users work with QMK Firmware.',
        entry_points={
            'console_scripts': ['%s = %s' % l for l in setup_cfg['entry_points'].items()],
        },
        license='MIT License',
        url=metadata['home-page'],
        version=setup_cfg['bumpversion']['current_version'],
        author=metadata['author'],
        author_email=metadata['author-email'],
        maintainer=metadata['author'],
        maintainer_email=metadata['author-email'],
        long_description=long_description,
        long_description_content_type="text/markdown",
        packages=find_packages(),
        py_modules = ['milc'],
        classifiers=[
            'Development Status :: 3 - Alpha',
            'Environment :: Console',
            'Intended Audience :: Developers',
            'Intended Audience :: System Administrators',
            'Intended Audience :: End Users/Desktop',
            'License :: OSI Approved :: MIT License',
            'Natural Language :: English',
            'Programming Language :: Python :: 3 :: Only',
            'Topic :: Scientific/Engineering',
            'Topic :: Software Development',
            'Topic :: Utilities',
        ],
        requires_python=metadata['requires-python'],
        install_requires=[
            "appdirs",
            "argcomplete",
            "colorama",
            "dotty-dict",
            "flake8",
            "hjson",
            "jsonschema>=3",
            "milc>=1.0.8",
            "nose2",
            "pygments",
            "yapf"
        ],
    )
