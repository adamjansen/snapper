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
    author='Adam Jansen',
    author_email='adam@adamjansen.com',
    description='Simple ZFS snapshot tool',
    entry_points='''
        [console_scripts]
        snapper=snapper:cli
    '''
)
