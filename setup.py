from setuptools import setup, find_packages

setup(
    name='getIPsFromDomains',
    version='1.0.0',
    description='Private package to getIPsFromDomains, a tool to get IPs from a list of domains...',
    url='git@github.com:JavaliMZ/getIPsFromDomains.git',
    author='Sylvain Júlio',
    author_email='syjulio123@gmail.com',
    license='unlicense',
    packages=find_packages(),  # Automatically finds all packages in the directory
    zip_safe=False,
    install_requires=[
        'tqdm',
        'tabulate',
        'termcolor'
    ],
    entry_points={
        'console_scripts': [
            'getIPsFromDomains=getIPsFromDomains:main'
        ]
    }
)
