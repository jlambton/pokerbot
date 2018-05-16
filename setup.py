try:
    from setuptools import setuptools
except ImportError:
    from dsitutils.core import setup

config = {
    'name': 'pokerbot',
    'author': 'James Lambton',
    'author_email': 'lambtonjames@gmail.com',
    'version': '0.1',
    'install_requires': []
    'packages': ['pokerbot']
    'scripts': [],
}

setup(**config)
