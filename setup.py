from setuptools import setup

setup(name='blended',
      version='3.0',
      description='Static Site Generation Using Python',
      url='https://github.com/johnroper100/Blended',
      author='John Roper',
      author_email='johnroper100@gmail.com',
      license='GPL3.0',
      packages=['blended'],
      install_requires=[
          'click',
          'colorama',
          'watchdog',
          'Markdown',
          'textile',
      ],
      entry_points={
          'console_scripts': [
              'blended=blended.__main__:cli',
          ],
      },
      zip_safe=False)
