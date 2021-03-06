from setuptools import setup, find_packages

version = '1.10.9.dev0'

setup(name='Products.Archetypes',
      version=version,
      description="Archetypes is a developers framework for rapidly "
                  "developing and deploying rich, full featured content "
                  "types within the context of Zope/CMF and Plone.",
      long_description=open("README.txt").read() + "\n" +
                       open("CHANGES.txt").read(),
      classifiers=[
        "Framework :: Plone",
        "Framework :: Plone :: 5.0",
        "Framework :: Zope2",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        ],
      keywords='Archetypes Plone CMF Zope',
      author='Archetypes development team',
      author_email='plone-developers@lists.sourceforge.net',
      url='http://pypi.python.org/pypi/Products.Archetypes',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['Products'],
      include_package_data=True,
      zip_safe=False,
      extras_require=dict(
        test=[
            'zope.annotation',
            'zope.publisher',
            'zope.testing',
            'plone.app.testing',
        ]
      ),
      install_requires=[
          'setuptools',
          'zope.component',
          'zope.contenttype',
          'zope.datetime',
          'zope.deferredimport',
          'zope.event',
          'zope.i18n',
          'zope.i18nmessageid',
          'zope.interface',
          'zope.lifecycleevent',
          'zope.publisher',
          'zope.schema',
          'zope.site',
          'zope.tal',
          'zope.viewlet',
          'Products.CMFCore',
          'Products.CMFFormController',
          'Products.CMFQuickInstallerTool',
          'Products.DCWorkflow',
          'Products.GenericSetup',
          'Products.MimetypesRegistry>=2.0.3',
          'Products.PlacelessTranslationService',
          'Products.PortalTransforms',
          'Products.ZSQLMethods',
          'Products.statusmessages',
          'Products.validation',
          'plone.folder',
          'plone.uuid',
          'plone.app.folder',
          'Acquisition',
          'DateTime',
          'ExtensionClass',
          'transaction',
          'ZODB3',
          'Zope2 >= 2.13.1',
          'plone.app.widgets>=2.0.0.dev0'
      ],
      )
