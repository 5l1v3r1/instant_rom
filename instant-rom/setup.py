from setuptools import setup
from sys import platform

setup(name='instantrom',
      version='1.0',
      description='Instantly download any Rom!',
      author='JackofSpades707',
      author_email='jackofspades707@hotmail.com',
      license='MIT',
      packages=['instantrom'],
      scripts=['bin/instantrom.py']
      install_requires=[
          'requests',
          'bs4'
      ]
      zip_safe=True)
