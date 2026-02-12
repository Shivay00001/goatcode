"""
Setup script for GOATCODE
"""

from setuptools import setup, find_packages
import os

here = os.path.abspath(os.path.dirname(__file__))

# Read README
with open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# Read requirements
with open(os.path.join(here, 'requirements.txt'), encoding='utf-8') as f:
    requirements = [line.strip() for line in f if line.strip() and not line.startswith('#')]

setup(
    name='goatcode',
    version='1.1.0',
    description='Production-grade deterministic coding agent with real architecture',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Shivay Singh',
    author_email='shivay@goatcode.dev',
    url='https://github.com/Shivay00001/goatcode',
    packages=find_packages(exclude=['tests', 'tests.*']),
    include_package_data=True,
    python_requires='>=3.9',
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'goatcode=cli.main:main',
        ],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Topic :: Software Development :: Code Generators',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    keywords='ai coding agent automation llm ollama openai anthropic',
    project_urls={
        'Bug Reports': 'https://github.com/Shivay00001/goatcode/issues',
        'Source': 'https://github.com/Shivay00001/goatcode',
    },
)
