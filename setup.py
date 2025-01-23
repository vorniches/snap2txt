from setuptools import setup, find_packages

setup(
    name='snap2txt',
    version='0.2.0',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'snap2txt = snap2txt.__main__:main'
        ]
    },
    include_package_data=True,
    package_data={
        'snap2txt': ['.il', '.wl'],
    },
    author='Sergei Vorniches',
    author_email='vorniches@gmail.com',
    description='A tool to save project structure and contents to a text file',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/vorniches/snap2txt',
    license='MIT',
    install_requires=[
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
