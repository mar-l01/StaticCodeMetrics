[![version 1.0.1](https://img.shields.io/badge/version-1.0.1-informational)](https://github.com/Markus2101/StaticCodeMetrics/releases) ![Python application](https://github.com/Markus2101/StaticCodeMetrics/workflows/Python%20application/badge.svg?branch=master)

## Requirements
Following packages are required for this application to be executed successfully:
- [Python](https://www.python.org/downloads/) (>=3.7)
- [numpy](https://numpy.org/install/) (>=1.18.3)
- [pandas](https://pandas.pydata.org/pandas-docs/stable/getting_started/install.html) (>=1.0.3)
- [matplotlib](https://matplotlib.org/3.2.1/users/installing.html) (>=3.2.1)

## Usage
The static code checker can be started directly from the command line:  
`staticcodemetric -df <directory-path> -pl <programming-language> (-di | -ms) [-s] [-sp <save-path>]`

Following options are available (required or optional):  
`-df <directory-path>`: Path to the directory which contains the code-files to check. This directory will be processed recursively.  
`-pl <programming-language>`: Programming language used in the files to check  
`-di`: Plot distance metric  
`-ms`: Plot Main Sequence  
`-s`: Save computed metrics (either instability and abstractness or distance in default directory)  
`-sp <save-path>`: Computed metrics are saved within provided path (but only if it exists)

## Development status
Currently, the metrics defined above can only be computed for C++ files.

## Further information
For further information and details see .https://github.com/Markus2101/StaticCodeMetrics.