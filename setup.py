from setuptools import setup, find_packages
from pathlib import Path

BASE_DIR = Path(__file__).parent

with open(BASE_DIR / 'README.md') as fp:
    README = fp.read()

with open(BASE_DIR / 'requirements.txt') as fp:
    REQUIREMENTS = fp.read().splitlines()

VERSION = '0.1.0'

setup(name='virtues-of-leos',
      version=VERSION,
      author='Pack of Leos',
      url='https://github.com/packofleos/virtues-of-leos',
      description='A django webapp for Leos to compete in doing something good.',
      long_description=README,
      long_description_content_type='text/markdown',
      license='GPL-3.0',
      install_requires=REQUIREMENTS,
      include_package_data=True,
      packages = ['virtues'],
      classifiers=[
          'Environment :: Web Environment',
          'Framework :: Django',
          'Framework :: Django :: 3.1',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: GNU Affero General Public License v3',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3 :: Only',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: 3.8',
          'Topic :: Internet :: WWW/HTTP',
          'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        ]
)
