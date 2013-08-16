from setuptools import setup

from flaskinit.metadata import __version__, __description__


if __name__ == '__main__':
  setup(
    name='flaskinit',
    version=__version__,
    description=__description__,
    long_description=open('README.rst').read(),
    license='MIT',
    author='Mark Steve Samson',
    author_email='hello@marksteve.com',
    packages=['flaskinit'],
    install_requires=open('requirements.txt').readlines(),
    entry_points=dict(console_scripts=['flaskinit = flaskinit:main']),
    zip_safe=False,
    include_package_data=True,
  )
