from setuptools import setup

setup(name='blended',
      version='6.0.0',
      description='The Most Versatile Static HTML Site Generator',
      url='http://jmroper.com/blended/',
      author='John Roper',
      author_email='john@jmroper.com',
      license='GPL3.0',
      packages=['blended'],
      include_package_data=True,
      install_requires=[
          'click',
          'python-frontmatter',
          'mammoth',
          'Markdown',
          'pyjade',
          'textile',
          'docutils',
          'untangle',
      ],
      entry_points={
          'console_scripts': [
              'blended=blended.__init__:cli',
          ],
      },
      zip_safe=False)
