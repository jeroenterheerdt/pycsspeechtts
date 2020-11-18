from setuptools import setup, find_packages
with open("../README.md", "r") as fh:
    long_description = fh.read()
setup(name='pycsspeechtts',
      version='1.0.4',
      description='Python 3 interface to Microsoft Cognitive Services Text To Speech',
      long_description=long_description,
      long_description_content_type="text/markdown",
      url='https://github.com/jeroenterheerdt/pycsspeechtts',
      author='Jeroen ter Heerdt',
      license='MIT',
      install_requires=['requests>=2.0'],
      tests_require=['mock'],
      test_suite='tests',
      packages=find_packages(exclude=["dist"]),
      zip_safe=True)
