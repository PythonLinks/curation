
#-*- coding: utf-8 -*-
import os
from os.path import join

from setuptools import setup, find_packages
from setuptools.extension import Extension

from Cython.Distutils import build_ext
from Cython.Build import cythonize

extensions =[
    Extension("zopache.application/*",
                           ["src/zopache/application/*.py"]),
    Extension("zopache.application/browser/*",
                           ["src/zopache/application/browser/*.py"]),    
    Extension("zopache.business/*", ["src/zopache/business/*.py"]),
    Extension("zopache.crud/*", ["src/zopache/crud/*.py"]),
    Extension("zopache.pages/*", ["src/zopache/pages/*.py"]),
    Extension("zopache.ttw/*", ["src/zopache/ttw/*.py"]),
    Extension("zopache.forms/*",
                 ["src/zopache/forms/*.py"]),
    Extension("zopache.ttw/html", ["src/zopache/ttw/html.pyx"]),
    Extension("zopache.iodide/*", ["src/zopache/iodide/*.py"]),
    Extension("zopache.zmi/*", ["src/zopache/zmi/*.py"]),
    Extension("zopache.python/*", ["src/zopache/python/*.py"]),    
    Extension("zopache.climate/*", ["src/zopache/climate/*.py"]),    
    Extension("zopache.core/*", ["src/zopache/core/*.py"])
                 ]

extensions =[]


name = 'zopache'
version = '0.1'
readme = open('README.md').read()
history = open(join('docs', 'HISTORY.txt')).read()


install_requires = [
    'biscuits',
    'cryptography',
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
    'googlemaps',
    'unicode-slugify',
    'pyramid_mailer',
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
    'repoze.sendmail',
    'setuptools',
    'zope.cachedescriptors',
    'z3c.schema',
    'zope.event',
    'zope.interface',
    'zope.lifecycleevent',
    'zope.password',    
    'zope.schema',
    'restrictedpython',    
    ]

tests_require = [
    'cromlech.browser [test]',
    'dolmen.forms.ztk >= 2.0',
    ]

setup(
      name=name,
      setup_requires=[
                 'cython>=0.x',
             ],

      ext_modules=cythonize(
                extensions,
                compiler_directives=dict(
                    language_level = "3",
                    always_allow_keywords=True)
                ),
      cmdclass=dict(
            build_ext=build_ext
        ),

      version=version,
      description="Zopache the core of the JSON Wikie",
      long_description=u"%s\n\n%s" % (readme, history),
      keywords='JSON NEWS WIKI',
      author='The Cromlech/Dolmen Team + Chrisotpher Lozinski',
      author_email='lozinski@PythonLinks.info',
      url='http://www.pythonlinks.info/json-wiki',
      license='Commercial', 
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
                'zmiicons = zopache.zmi:library',
                'iodide = zopache.iodide:library',                             
                ],
        },
              
      )
