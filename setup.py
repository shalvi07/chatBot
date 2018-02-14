from setuptools import setup

requires = [
    'pyramid',
    'waitress',
    'pyramid_chameleon',
    'pymongo',
    'pyramid_debugtoolbar',
    'requests',
    'pymongo',
    'python-dateutil'
]

setup(name='chatApp',
      install_requires=requires,
      entry_points="""\
      [paste.app_factory]
      main = chatApp:main
      """,
)
