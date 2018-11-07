# -*- coding: utf-8 -*-

from os.path import join
from setuptools import setup, find_packages

name = 'zopache'
version = '0.7'
readme = open('README.md').read()
history = open(join('docs', 'HISTORY.txt')).read()

install_requires = [
    'crom',
    'cromlech.auth',
    'cromlech.browser',
    'cromlech.content',
    'cromlech.file',
    'cromlech.i18n',
    'cromlech.configuration',
    'cromlech.dawnlight',
    'cromlech.grok',
    'cromlech.i18n',
    'cromlech.security',
    'cromlech.location',
    'cromlech.webob',
    'cromlech.zodb',
    'dolmen.container',
    'dolmen.breadcrumbs',
    'dolmen.forms.base',
    'dolmen.forms.ztk',
    'dolmen.message',
    'dolmen.tales',
    'dolmen.template',
    'dolmen.view',
    'dolmen.viewlet',
    'dolmen.widget.file',
    'python-slugify',
    'setuptools',
    'zopache',
    'zopache.copy',
    'zope.interface',
    'zope.location',
    'zope.schema',
    'arrow',
    'beautifulsoup4',    
    'jsmin',
    'DateTime',
    'dm.historical',
    'dolmen.forms.base >= 2.0',
    'fanstatic',
    'pillow',
    'setuptools',
    'zope.cachedescriptors',
    'z3c.schema',
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
       entry_points={
           'paste.app_factory': [
                'demo = zopache.application.wsgi:demo_application',
                ],
           'fanstatic.libraries': [
                'ttwicons = zopache.ttw:library',
                ],
        },
              
      )
