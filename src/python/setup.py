__author__ = 'tom'
from setuptools import setup

# Makes use of the sphinx and sphinx-pypi-upload packages. To build for local development
# use 'python setup.py develop'. To upload a version to pypi use 'python setup.py clean sdist upload'.
# To build docs use 'python setup.py build_sphinx' and to upload docs to pythonhosted.org use
# 'python setup.py upload_sphinx'. Both uploads require 'python setup.py register' to be run, and will
# only work for Tom as they need the pypi account credentials.

setup(
    name='approxeng.picamera',
    version='0.1',
    description='PiCamera based image processing for PiWars robots using OpenCV',
    classifiers=['Programming Language :: Python :: 2.7'],
    url='https://github.com/ApproxEng/approxeng.picamera/',
    author='Tom Oinn',
    author_email='tomoinn@gmail.com',
    license='ASL2.0',
    packages=['approxeng.picamera'],
    install_requires=['imutils==0.4.0'],
    include_package_data=True,
    test_suite='nose.collector',
    tests_require=['nose'],
    dependency_links=[],
    zip_safe=False)
