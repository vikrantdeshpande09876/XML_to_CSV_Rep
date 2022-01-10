from setuptools import setup, find_packages

setup(
    name='XML2CSV',
    version='2.5.0',
    author='Vikrant Deshpande',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=['flask', 'Flask-Assets', 'openpyxl', 'lxml', 'Flask-WTF', 'pandas']
)