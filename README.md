# StaticCodeMetrics [![version](https://img.shields.io/badge/Version-1.0.2-orange)](https://github.com/Markus2101/StaticCodeMetrics/releases) [![pypi](https://img.shields.io/badge/PyPi-1.0.2-informational)](https://pypi.org/project/staticcodemetric-scm-pkg/) ![Python application](https://github.com/Markus2101/StaticCodeMetrics/workflows/Python%20application/badge.svg?branch=master)

This repository provides helper-functions to compute static code metrics like, for instance, instability and abstractness of files and components. 
The development of these algorithms was inspired by the book **Clean Architecture** written by **Robert C. Martin** (https://www.amazon.com/dp/0134494164).

- Calculation of instability I: I = fan_out / (fan_in + fan_out), where fan_out denotes the number of outgoing dependencies from a file / component and fan_in the number of incoming dependencies to a file / component.

- Calculation of abstractness A: A = N_a / N_c, where N_a denotes the number of interfaces or abstract classes inside a file / component and N_c the number of classes inside a file / component.

- Distance D: D = |A + I - 1|, where a value of 0 indicates the file / component lies on the _Main Sequence_ and a value of 1 denotes a file being far away of it.

- Main Sequence: A linear line going from point _(0,1)_ to _(1,0)_, where the coordinates _(a,i)_ describe the value of Abstractness and the value of Instability, respectively. Both points given describe the most desireable points for a file / component: either maximal stable & abstract or maximal unstable & concrete. For all files / components given it is desireable to be on or close to the Main Sequence.

## Installation
This application can either be installed via [PyPi](https://pypi.org/) or by cloning this repository.

### Requirements
Following packages are required for this application to be executed successfully:
- [Python](https://www.python.org/downloads/) (>=3.7)
- [numpy](https://numpy.org/install/) (>=1.18.3)
- [pandas](https://pandas.pydata.org/pandas-docs/stable/getting_started/install.html) (>=1.0.3)
- [matplotlib](https://matplotlib.org/3.2.1/users/installing.html) (>=3.2.1)

### Simply via PyPi
Installing via PyPi is easy and straight forward. Executing following command will install this application for you:  
```sh
$ pip install staticcodemetric-scm-pkg
```  

Now the application can be started from the command line directly by running, for example,  
```sh
$ staticcodemetric -h
```  

### Call Python-script directly
After cloning this repository, run \__main__.py using Python from the root-directory, e.g.   
```sh
$ python .\scm_modules\__main__.py -h
```  

## Usage
The static code checker can be started directly from the command line:  
```sh
$ staticcodemetric -df <directory-path> -pl <programming-language> (-di | -ms) [-s] [-sp <save-path>]
```  

Following options are available (required or optional):  
`-df <directory-path>`: Path to the directory which contains the code-files to check. This directory will be processed recursively.  
`-pl <programming-language>`: Programming language used in the files to check  
`-di`: Plot distance metric  
`-ms`: Plot Main Sequence  
`-s`: Save computed metrics (either instability and abstractness or distance in default directory)  
`-sp <save-path>`: Computed metrics are saved within provided path (but only if it exists)

## Testing
Tests are written using Python's unittest library and can be locally executed using following command from the root-directory:  
```sh
$ python .\tests\run_all_tests.py
```  

## Development status
Currently, the metrics defined above can only be computed for C++ files.

## Future development
In future, the metrics should be expanded to handle whole components (consisting of one or more files). Other programming languages will be tackled, too.
