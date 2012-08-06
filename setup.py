import os

from setuptools import setup
from setuptools import find_packages

here = os.path.abspath(os.path.dirname(__file__))
try:
    README = open(os.path.join(here, 'README.rst')).read()
    CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()
except IOError:
    README = CHANGES = ''

install_requires = [
    'docopt',
    'jinja2',
    'pyyaml',
    ]

tests_require = [
    'pytest',
    'pytest-cov',
    'pytest-pep8',
    'pytest-xdist',
    ]

setup(name='cu',
      version='0.1.0',
      description="Simple customer relationship management using YAML.",
      long_description='\n\n'.join([README, CHANGES]),
      classifiers=[
        "Programming Language :: Python",
        ],
      author='Christian Neumann',
      author_email='cneumann@datenkarussell.de',
      url='https://github.com/chrneumann/cu',
      keywords='cu customer relationship management',
      license="BSD-Clause-2",
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=install_requires,
      tests_require=tests_require,
      entry_points="""\
      [console_scripts]
      cu-mail = cu.mail:main
      """,
      extras_require={
          'testing': tests_require,
          },
      )
