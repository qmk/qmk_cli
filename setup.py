from configparser import ConfigParser
from setuptools import setup, find_packages

setup_cfg = ConfigParser()
setup_cfg.read('setup.cfg')
metadata = setup_cfg['metadata']

if __name__ == "__main__":
    with open('README.md', encoding='utf-8') as readme_file:
        long_description = readme_file.read()
    setup(
        name=metadata['dist-name'],
        description='A program to help users work with QMK Firmware.',
        entry_points={
            'console_scripts': ['%s = %s' % i for i in setup_cfg['entry_points'].items()],
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
        py_modules=['qmk_cli'],
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
        python_requires=metadata['requires-python'],
        install_requires=[
            "appdirs==1.4.4",
            "argcomplete==1.12.3",
            "attrs==21.2.0",
            "colorama==0.4.4",
            "coverage==5.5",
            "qmk-dotty-dict==1.3.0.post1",
            "flake8==3.9.2",
            "halo==0.0.31",
            "hid==1.0.4",
            "hjson==3.0.2",
            "jsonschema==3.2.0",
            "log-symbols==0.0.14",
            "mccabe==0.6.1",
            "milc==1.4.2",
            "nose2==0.10.0",
            "pycodestyle==2.7.0",
            "pyflakes==2.3.1",
            "Pygments==2.9.0",
            "pyrsistent==0.18.0",
            "pyusb==1.2.1",
            "setuptools>=45",
            "six==1.16.0",
            "spinners==0.0.24",
            "termcolor==1.1.0",
            "yapf==0.31.0"
        ]
    )
