__author__ = 'miroslav.stepanek'

from setuptools import setup, find_packages

setup(name='config_shelf',
      version='0.1',
      description='Software configuration tool',
      author='miroslav.stepanek',
      author_email='info@mirousek.eu',
      packages=find_packages(),
      entry_points={
          'console_scripts': [
              'config_shelf = config_shelf.main:main',
          ]
      },
      install_requires=['GitPython', 'lxml']
      )
