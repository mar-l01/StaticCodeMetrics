import pathlib
from setuptools import setup

# for long description, use README_PyPi.md
README = (pathlib.Path(__file__).parent / "README_PyPi.md").read_text()

setup(
    name='staticcodemetric-scm-pkg',
    description='A summary of static-code metrics',
    long_description=README,
    long_description_content_type='text/markdown',
    author='Markus Loipfinger',
    author_email='m.loipfinger@hotmail.de',
    url='https://github.com/Markus2101/StaticCodeMetrics',
    version='1.0.3',
    license='GPL-3.0',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
    ],
    packages=['scm_modules', 'scm_modules.metrics', 'scm_modules.utils'],
    install_requires=['numpy', 'pandas', 'matplotlib'],
    entry_points={'console_scripts': ['staticcodemetric=scm_modules.__main__:main']}
)
