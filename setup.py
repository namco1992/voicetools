# -*- encoding: UTF-8 -*-
import re
from setuptools import setup, find_packages

PACKAGE = "voicetools"
NAME = 'voicetools'

with open('voicetools/__init__.py', 'r') as fd:
    VERSION = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
                        fd.read(), re.MULTILINE).group(1)

if not VERSION:
    raise RuntimeError('Cannot find version information')

setup(name=NAME,
      version=VERSION,
      description="All-in-one voice tools library",
      long_description='All-in-one voice tools library',
      classifiers=(
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Multimedia :: Sound/Audio :: Sound Synthesis',
        'Topic :: Multimedia :: Sound/Audio :: Speech'
          ),  # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='python baidu tts asr wolfram turing',
      author='namco1992',
      author_email='namco1992@gmail.com',
      url='https://github.com/namco1992/voicetools',
      license='MIT',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=True,
      install_requires=[
          'requests', 'wolframalpha'
      ],
)
