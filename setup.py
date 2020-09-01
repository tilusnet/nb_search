from setuptools import setup

setup(name='nb_search',
      version='0.0.1',
      description='Module for searching through Jupyter Notebooks',
      url = 'https://github.com/loevlie/nb_search.py',
      author='Dennis Loevlie',
      author_email='dloevlie@andrew.cmu.edu',
      scripts=['nb_search.py'],
      packages=['nb_search'],
      install_requires=['IPython', 'matplotlib', 'numpy', 'nbformat', 'pandas', 'argparse'],)
