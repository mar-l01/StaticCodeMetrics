# StaticCodeMetrics

![Python application](https://github.com/Markus2101/StaticCodeMetrics/workflows/Python%20application/badge.svg?branch=master)

This repository provides helper-functions to compute static code metrics like, for instance, instability and abstractness of files and components. 
The development of these algorithms was inspired by the book **Clean Architecture** written by **Robert C. Martin** (https://www.amazon.com/dp/0134494164).

- Calculation of instability I: I = fan_out / (fan_in + fan_out), where fan_out denotes the number of outgoing dependencies from a file / component and fan_in the number of incoming dependencies to a file / component.

- Calculation of abstractness A: A = N_a / N_c, where N_a denotes the number of interfaces or abstract classes inside a file / component and N_c the number of classes inside a file / component.

- Distance D: D = |A + I - 1|, where a value of 0 indicates the file / component lies on the _Main Sequence_ and a value of 1 denotes a file being far away of it.

- Main Sequence: A linear line going from point _(0,1)_ to _(1,0)_, where the coordinates _(a,i)_ describe the value of Abstractness and the value of Instability, respectively. Both points given describe the most desireable points for a file / component: either maximal stable & abstract or maximal unstable & concrete. For all files / components given it is desireable to be on or close to the Main Sequence.

## Usage
The static code checker can be started using the command line:
`python ./static_code_check.py -df <directory-path> (-di | -ms)`

`-df <directory-path>`: Path to the directory which contains the code-files to check. This directory will be processed recursively.  
`-di`: Plot distance metric  
`-ms`: Plot Main Sequence  

## Development status
Currently, the instability and abstractness metric can be computed on C++ files only.

## Future development
In future, the metrics should be expanded to handle whole components (consisting of one or more files). Other programming languages will be tackled, too.
