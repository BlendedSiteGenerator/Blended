from setuptools import setup

setup(name='blended',
      version='1.2',
      description='Python HTML flat-file website generator',
      url='https://github.com/johnroper100/Blended',
      author='John Roper',
      author_email='johnroper100@gmail.com',
      license='GPL3.0',
      packages=['blended'],
      install_requires=[
          'Click',
          'colorama',
      ],
      entry_points={
          'console_scripts': [
              'blended=blended.__main__:cli',
          ],
      },
      zip_safe=False)
