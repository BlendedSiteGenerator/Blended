from setuptools import setup

setup(name='blended',
      version='3.5',
      description='Static HTML Site Generation Using Python',
      url='http://jmroper.com/blended/',
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
          'docutils',
          'mammoth',
          'importlib',
      ],
      entry_points={
          'console_scripts': [
              'blended=blended.__main__:cli',
          ],
      },
      zip_safe=False)
