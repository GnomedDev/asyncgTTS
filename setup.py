from setuptools import setup
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='asyncgTTS',
    packages=['asyncgTTS'],
    version='0.1.0',
    license='MIT',
    description='Async interfaces to the official Google Text to Speech or easygtts APIs',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Gnome-py',
    author_email='gnome6669.py@gmail.com',
    url='https://github.com/gnome-py/asyncgTTS',
    download_url='https://github.com/Gnome-py/asyncgTTS/archive/v0.1.0.tar.gz',
    keywords=['async', 'TTS', 'gtts', 'text to speech'],
    install_requires=['aiohttp'],
    classifiers=[
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    ],
)
