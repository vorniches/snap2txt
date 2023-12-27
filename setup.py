# setup.py
from setuptools import setup, find_packages

setup(
    name='snap2txt',
    version='0.1.0',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'snap2txt = snap2txt.__main__:main'
        ]
    },
    # Add additional information like author, description, requirements, etc.
    author='Sérgio Vorniches',
    author_email='vorniches@gmail.com',
    description='A tool to save project structure and contents to a text file',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/vorniches/snap2txt',
    license='MIT',
    install_requires=[
        # List any Python package dependencies here
        # e.g., 'requests>=2.25.1'
    ],
    classifiers=[
        # Trove classifiers
        # Full list at https://pypi.org/classifiers/
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
