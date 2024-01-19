# Vaccine

Vaccine is a program designed to test the vulnerability of an endpoint to SQL injection attacks. It supports both boolean and union-based injection methods for MySQL and Postgres databases.

## Table of Contents
- [Usage](#usage)
- [Options](#options)
- [Output](#output)
- [Dependencies](#dependencies)
- [Contributing](#contributing)
- [License](#license)

## Usage

```bash
python vaccine.py URL [-o OUTPUT] [-X METHODS]
```

- `URL`: The target URL to test for SQL injection vulnerabilities.
- `-o, --output`: Specify the output file for the results. (Optional)
- `-X, --methods`: Specify the HTTP method (GET or POST). (Optional)

## Options

- `-o, --output`: Specify the output file for the results. Default is "output".
- `-X, --methods`: Specify the HTTP method (GET or POST). Default is "GET".

## Output

The results of the SQL injection tests will be stored in the specified output file in the "output" directory. The output file will be in zip format.

## Contributing

If you'd like to contribute to the project, please follow the [contributing guidelines](CONTRIBUTING.md).