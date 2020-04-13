# StaticCodeMetrics
This repository provides helper-functions to compute static code metrics like, for instance, instability and abstractness of files and components. 
The development of these algorithms was inspired by the book **Clean Architecture** written by **Robert C. Martin** (https://www.amazon.com/dp/0134494164).

- Calculation of instability I: I = fan_out / (fan_in + fan_out), where fan_out denotes the number of outgoing dependencies from a file / component and fan_in the number of incoming dependencies to a file / component.

- Calculation of abstractness A: A = N_a / N_c, where N_a denotes the number of interfaces or abstract classes inside a file / component and N_c the number of classes inside a file / component.

## Development status
Currently, the instability and abstractness metric can be computed on C++ files only.

## Future development
In future, the metrics should be expanded to handle whole components (consisting of one or more files). Other programming languages will be tackled, too.
