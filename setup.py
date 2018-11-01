# -*- coding: utf-8 -*-

from os.path import join
from setuptools import setup, find_packages

name = 'zopache'
version = '0.7'
readme = open('README.md').read()
history = open(join('docs', 'HISTORY.txt')).read()

install_requires = [
    'arrow',
    'jsmin',
    'crom',
    'cromlech.browser >= 0.5',
    'cromlech.content',
    'cromlech.file',
    'cromlech.i18n',
    'dolmen.widget.file',
    'DateTime',
    'dm.historical',
    'dolmen.forms.base >= 2.0',
    'dolmen.message',
    'fanstatic',
    'setuptools',
    'zope.cachedescriptors',
    'z3c.schema',
    'zopache.copy',
    'zope.event',
    'zope.interface',
    'zope.lifecycleevent',
    'zope.location',
    'zope.password',    
    'zope.schema',
    'restrictedpython',    
    ]

tests_require = [
    'cromlech.browser [test]',
    'dolmen.forms.ztk >= 2.0',
    ]

setup(name=name,
      version=version,
      description="CRUD forms and actions for Zopache",
      long_description=u"%s\n\n%s" % (readme, history),
      keywords='Zopache Crud Forms',
      author='The Dolmen Team + Chrisotpher Lozinski',
      author_email='lozinski@PythonLinks.info',
      url='http://www.dolmen-project.org',
      license='ZPL + CV', 
      packages=find_packages('src', exclude=['ez_setup']),
      package_dir={'': 'src'},
      namespace_packages=['zopache'],
      include_package_data=True,
      zip_safe=False,
      tests_require=tests_require,
      install_requires=install_requires,
      extras_require={'test': tests_require},
      test_suite="zopache.crud",
      classifiers=[
          'Environment :: Web Environment',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          ],
      )
