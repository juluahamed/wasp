from setuptools import setup

setup(
    name='wasp',
    packages=['wasp'],
    include_package_data=True,
    install_requires=[
        'flask','flask_sqlalchemy',
    ],
    
)
