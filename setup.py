from setuptools import setup

setup(
    name='snapper',
    version='0.1',
    packages=['snapper'],
    install_requires=[
        'click',
    ],
    url='',
    license='MIT',
    author='adam',
    author_email='',
    description='',
    entry_points='''
        [console_scripts]
        snapper=snapper.cli
    '''
)
