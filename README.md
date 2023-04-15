# Python Mono-Repo Template
This is a template for creating a Python mono-repository that allows storing multiple separate services and packages
that can be dependencies of these services. The template serves as a skeleton that allows easy creation of new services
and packages, and takes care of different aspects such as code linting, unit testing, and building Docker images.

### Features:
* 🐍 [Monorepo](https://en.wikipedia.org/wiki/Monorepo)-ready: multiple separate services and packages in a single repository
* 📦 [Poetry](https://github.com/python-poetry/poetry) for dependency management
* 📝 Easy creation of new services and packages with a Makefile and templates
* 🖋️ Python code formatting using [Black](https://github.com/psf/black) (The uncompromising Python code formatter)
* ⚡ Code linting using [Ruff](https://github.com/charliermarsh/ruff) (An extremely fast Python linter, written in Rust.)
* 🐳 Preconfigured Dockerfiles for services
* 🪝 [Pre-commit](https://github.com/pre-commit/pre-commit) hooks for linting and formatting
* 🚀 GitHub Actions for linting and testing

---

## Features
#### 🐍 Templates for Python packages and services:
This template provides a set of templates for creating new Python
packages and services. These templates include boilerplate code and configuration files that make it easy to get started
and ensure consistency across all the components in your repository.


#### 📦 Dependency management with Poetry:
This repository uses Poetry as the preferred way to track dependencies for
Python packages and services. Poetry provides a simple and reliable way to manage dependencies, and is recommended over
the old setup.py files and requirements.txt files. With Poetry, you can easily add and remove dependencies, generate
lockfiles for reproducible builds, and manage virtual environments for different projects.


#### 🖋️ Python code formatting using Black:
This project uses Black, a Python code formatter, to ensure that code is consistently formatted and adheres to
PEP 8 guidelines. Black takes care of automatic code formatting, saving you time and energy that would be spent on
manual formatting.


#### ⚡️Code linting using Ruff:
This project uses Ruff, a new super fast Python linter written in Rust, to check code for syntax errors, style
violations, and potential bugs. Ruff is designed to be extremely fast, making it a good choice for large codebases.


#### 🐳 Preconfigured Dockerfiles:
This template includes a basic Dockerfile that can be used to build and run services in containers.
This makes it easy to deploy your services to different environments and helps ensure that your code runs consistently
across different machines.*


#### 🪝 Pre-commit hooks for linting and formatting:
This template comes with pre-commit hooks that automatically check
your code for formatting errors, style issues, and other problems before you commit changes to Git. This helps ensure
that your code is consistent and adheres to the project's standards.


#### 🚀 GitHub Actions for linting and testing:
This template includes GitHub Actions that automatically run linting and
testing scripts whenever you push changes to your repository. This helps catch errors and issues early on, before they
can cause problems in production.


#### 🛠️ Makefile for running common commands:
This template includes a Makefile that provides a set of common commands for
working with the repository, such as running tests, building Docker images, and cleaning up temporary files.

---

## Getting Started
To use this template, simply clone the repository and start creating new services and packages based on the provided
templates. You can customize the pre-commit hooks, GitHub Actions, and other configuration files to meet your specific needs.


### File Structure
```
├── doc                    # Project-level documentation folder
├── packages               # Packages root folder
├── scripts                # Project-level scripts folder
├── services               # Services root folder
├── templates              # Template folder for new packages and services
│   ├── package            # Package template folder
│   │   ├── doc            # Package documentation folder
│   │   ├── scripts        # Package scripts folder
│   │   ├── src            # Package source code folder
│   │   ├── tests          # Package test folder
│   │   ├── Makefile       # Package Makefile for running common commands
│   │   ├── README.md      # Package README file
│   │   ├── poetry.lock    # Poetry lock file for package dependencies
│   │   └── pyproject.toml # Poetry configuration file for the package
│   └── service            # Service template folder
│       ├── doc            # Service documentation folder
│       ├── scripts        # Service scripts folder
│       ├── src            # Service source code folder
│       ├── tests          # Service test folder
│       ├── Dockerfile     # Dockerfile for building the service
│       ├── Makefile       # Service Makefile for running common commands
│       ├── README.md      # Service README file
│       ├── poetry.lock    # Poetry lock file for service dependencies
│       └── pyproject.toml # Poetry configuration file for the service
├── LICENSE                # License file
├── Makefile               # Project-level Makefile for running common commands for the entire repo
├── README.md              # README file for the entire repo
└── pyproject.toml         # Poetry configuration file for the entire repo
```

### Creating New Services and Packages
This repository includes a Makefile that provides convenient targets for creating new services and packages.
These targets are implemented using shell scripts located in the scripts directory, and provide boilerplate code and
configuration files to help get started with new projects.

To create a new service, run the new-service target from the command line and provide a name for your service:

```shell
make new-service name=<service-name>
```

This will create a new service directory in the services directory with the provided name.
The directory will contain a Dockerfile for building the service, a pyproject.toml file for listing dependencies,
and a basic project structure.

To create a new package, run the new-package target from the command line and provide a name for your package:

```shell
make new-package name=<package-name>
```

This will create a new Python package in the packages directory with the provided name.
The directory will contain a basic project structure with a pyproject.toml file for listing dependencies.

These targets are designed to help you get started quickly and provide a consistent project structure across all your
services and packages. You can modify the shell scripts to suit your own needs or create your own targets in the
Makefile as needed.

---

## Using the Makefile

This repository includes a Makefile with targets that automate common tasks for Python services.
These targets are implemented using shell scripts located in the scripts directory and can be invoked from the command
line using the make command.

Here are the available targets:

### Installation
This target installs the service and its dependencies into a virtual environment.
It uses Poetry to manage dependencies and installs them according to the configuration in the pyproject.toml file.

To use this target, run the following command from the root directory of your service:
```shell
make install
```

### Code formatting
This target formats the code using Black, a Python code formatter. It applies a consistent coding style to your
codebase and ensures that it follows the PEP 8 guidelines.

To use this target, run the following command from the root directory of your service:

```shell
make format
```

### Linting
This target lints the code using Ruff, a fast Python linter written in Rust. It checks your codebase for syntax errors,
style violations, and potential bugs, and provides a report of any issues found.

To use this target, run the following command from the root directory of your service:
```shell
make lint
```

### Unit testing
This target runs the unit tests for your service using Pytest, a Python testing framework. It discovers and runs all
tests in the tests directory and provides a report of the test results.

To use this target, run the following command from the root directory of your service:
```shell
make test
```

## Contributing
If you find any issues with this template or have suggestions for improvements, please feel free to contribute to the
project. You can open issues, submit pull requests, or contact the project maintainers directly.

## License
This project is licensed under the MIT License - see the LICENSE file for details.
