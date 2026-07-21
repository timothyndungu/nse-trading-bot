"""
NSE Trading Bot Setup File
"""

from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='nse-trading-bot',
    version='0.1.0',
    author='Timothy Ndungu',
    description='AI-powered algorithmic trading bot for Nairobi Securities Exchange',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/timothyndungu/nse-trading-bot',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Financial and Insurance Industry',
        'Topic :: Office/Business :: Financial :: Investment',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
    python_requires='>=3.8',
    install_requires=[
        'tensorflow>=2.13.0',
        'keras>=2.13.0',
        'torch>=2.0.0',
        'scikit-learn>=1.3.1',
        'pandas>=2.0.3',
        'numpy>=1.24.3',
        'yfinance>=0.2.32',
        'requests>=2.31.0',
        'beautifulsoup4>=4.12.2',
        'matplotlib>=3.7.2',
        'seaborn>=0.12.2',
        'plotly>=5.16.1',
        'dash>=2.14.1',
        'dash-bootstrap-components>=1.4.1',
        'python-dotenv>=1.0.0',
        'sqlalchemy>=2.0.21',
        'pytest>=7.4.0',
        'jupyter>=1.0.0',
    ],
    entry_points={
        'console_scripts': [
            'nse-trading-bot=main:main',
        ],
    },
)
