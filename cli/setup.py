from setuptools import setup, find_packages

setup(
    name='dicom-mngr',
    version='0.1',
    packages=find_packages(),
    py_modules=['cli', 'checks'],
    install_requires=[
        'Click',
        'pydicom'
    ],
    entry_points='''
        [console_scripts]
        dicom-mngr=cli:cli
    '''
)
