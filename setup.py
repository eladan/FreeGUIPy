from setuptools import setup, find_packages
import sys, os

# TelephonyPy is copyright (c) 2012, Noel Morgan <noel@telephonypy.org>

version = '0.1'

setup(name='FreeGUIPy',
      version='0.1',
      description="Next generation GUI configurator for FreeSWITCH.",
      long_description="""Next generation GUI configurator for FreeSWITCH.""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='telephonypy ',
      author='Noel Morgan',
      author_email='noel@vwci.com',
      url='http://www.freeguipy.org',
      license='See http://www.python.org/2.6/license.html',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=True,
      install_requires=[
          "Paste>=1.7.5.1",
          "PasteScript>=1.7.5",
          "Beaker>=1.6.4",
          "FormEncode>=1.2.4",
          "Jinja2>=2.6",
          "Genshi>=0.6",
          "WebError>=0.10.3",
          "WebHelpers>=1.3",
          "psycopg2>=2.4",
          "transaction>=1.3",
          "zope.sqlalchemy>=0.7.1",
          "Pygments>=1.5",
          "MarkupSafe>=0.15",
          "decorator>=3.4.0",
          "SQLAlchemy>=0.7.9",
          "WebOb>=0.5.1"
      ],
      setup_requires=["PasteScript>=1.7.5"],
      entry_points="""
        [paste.app_factory]
        main = freeguipy.config:app_factory
      """,)
