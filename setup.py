from setuptools import setup

setup(name='blended',
      version='0.1',
      description='Python website generator',
      url='jmroper.com',
      author='John Roper',
      author_email='johnroper100@gmail.com',
      license='GPL3.0',
      packages=['blended'],
      install_requires=[
          'Click',
          'colorama',
      ],
      zip_safe=False)