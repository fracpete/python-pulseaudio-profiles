# setup.py
# Copyright (C) 2020 Fracpete (fracpete at gmail dot com)

from setuptools import setup


def _read(f):
    """
    Reads in the content of the file.
    :param f: the file to read
    :type f: str
    :return: the content
    :rtype: str
    """
    return open(f, 'rb').read()


setup(
    name="python-pulseaudio-profiles",
    description="Simple library to create and apply pulseaudio profiles.",
    long_description=(
        _read('DESCRIPTION.rst') + b'\n' +
        _read('CHANGES.rst')).decode('utf-8'),
    url="https://github.com/fracpete/python-pulseaudio-profiles",
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Topic :: Multimedia :: Sound/Audio',
        'Programming Language :: Python :: 3',
        'Operating System :: POSIX :: Linux',
    ],
    license='MIT License',
    package_dir={
        '': 'src'
    },
    packages=[
        "pypulseprofiles",
    ],
    version="0.0.2",
    author='Peter "fracpete" Reutemann',
    author_email='fracpete@gmail.com',
    install_requires=[
        "pulsectl",
        "pyyaml",
    ],
    entry_points={
        "console_scripts": [
            "ppp-info=pypulseprofiles.info:sys_main",
            "ppp-create=pypulseprofiles.create:sys_main",
            "ppp-apply=pypulseprofiles.apply:sys_main",
            "ppp-list=pypulseprofiles.list:sys_main",
            "ppp-rm=pypulseprofiles.delete:sys_main",
        ]
    }
)
