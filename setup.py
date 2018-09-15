from setuptools import setup

NAME = 'connect_four'
setup(
    name=NAME,
    packages=[
        'connect_four',
        'lensa_lint.resources',
    ],
    # package_data={},
    version='0.0.1',
    description='',
    author='Andras Radnai',
    author_email='r7ar7a@gmail.com',
    install_requires=[
        'flask', 'flask_socketio', 'redis', ''
    ],
    tests_require=['pytest'],
    entry_points={
        'console_scripts': ['llintpy=lensa_lint.cli:main'],
    },
    classifiers=[],
)
