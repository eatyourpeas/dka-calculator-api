from setuptools import _install_setup_requires, setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='bsped-dka-calculator',
    version='0.0.1',
    description='A fluid and medicine calculator for resuscitation of paediatric diabetic ketoacidosis using the British Society of Paediatric Endocrinology guidelines.',
    long_description="https://github.com/eatyourpeas/dka-calculator-api/blob/main/README.md",
    url="https://github.com/eatyourpeas/dka-calculator-api/blob/main/README.md",
    author='@dan-leach, @eatyourpeas, RCPCH, BSPED',

    author_email='eatyourpeasapps@gmail.com',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Scientific/Engineering :: Medical Science Apps.'
    ],
    keywords='Paediatric DKA, ketoacidosis, diabetes, type 1, BSPED, british society of paediatric endocrinology and diabetes',  
    
    packages=find_packages(),  
    python_requires='>=3.5',
    install_requires=[
        'pytest',
    ],  
    extras_require={  
        'dev': ['check-manifest'],
        'test': ['coverage'],
    },
    include_package_data=True,
    project_urls={  
        'Bug Reports': 'https://github.com/rcpch/digital-growth-charts/issues',
        'API management': 'https://dev.rcpch.ac.uk',
        'Source': 'https://github.com/eatyourpeas/bsped-dka-calculator',
    },
)
