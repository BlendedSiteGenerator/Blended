from setuptools import setup

setup(name='blended',
      version='1.5',
      description='Static Site Generation Using HTML and Python',
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
