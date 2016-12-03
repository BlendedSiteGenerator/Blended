from setuptools import setup

setup(name='blended',
      version='1.0',
      description='Python website generator',
      url='http://jmroper.com',
      author='John Roper',
      author_email='johnroper100@gmail.com',
      license='GPL3.0',
      packages=['blended'],
      install_requires=[
          'Click',
          'colorama',
      ],
      zip_safe=False)
