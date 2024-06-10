# MMORS - massively manage online resource searches OR Manage Many Online Resource Searches

[<img alt="Linting status of master" src="https://img.shields.io/github/actions/workflow/status/rwarnking/mmors/linter.yml?label=Linter&style=for-the-badge" height="23">](https://github.com/marketplace/actions/super-linter)
[<img alt="Version" src="https://img.shields.io/github/v/release/rwarnking/mmors?style=for-the-badge" height="23">](https://github.com/rwarnking/mmors/releases/latest)
[<img alt="Licence" src="https://img.shields.io/github/license/rwarnking/mmors?style=for-the-badge" height="23">](https://github.com/rwarnking/mmors/blob/main/LICENSE)

## Description
This is a small python application to crawl search results of different websites.

## Table of Contents
- [MMORS](#mmors)
  - [Table of Contents](#table-of-contents)
  - [List of Features](#list-of-features)
  - [Installation](#installation)
    - [Dependencies](#dependencies)
  - [Usage](#usage)
    - [GUI](#gui)
  - [Contributing](#contributing)
  - [Credits](#credits)
  - [License](#license)

## List of Features

- Process list of search sites
  - supports get request
  - supports get request with auth
  - supports post request
  - supports json response
  - supports html response
  - supports google json response
- Process list of search terms
  - allow terms with spaces
  - allow terms with / : ( or )
- Export results to HTML
- Export results to CSV

## Installation

Download this repository or install directly from GitHub
```bash
pip install git+https://github.com/rwarnking/mmors.git
```

### Dependencies

This project uses python. One of the tested versions is python 3.9.

Use either
```bash
pip install -r requirements.txt
```
to install all dependencies.

Or use Anaconda for your python environment and create a new environment with
```bash
conda env create --file mmors.yml
```
afterwards activate the environment (`conda activate mmors`) and start the application.

The main dependency is tkinter:
* [tkinter](https://docs.python.org/3/library/tkinter.html) for the interface/GUI
* [tkcalendar](https://pypi.org/project/tkcalendar/) for the date selection
* [BeautifulSoup](https://docs.python.org/3/library/pathlib.html)

Further dependencies that should be present anyway are:
* [calendar](https://docs.python.org/3/library/calendar.html)
* [requests](https://docs.python.org/3/library/requests.html)
* [re (regex)](https://docs.python.org/3/library/re.html) for parsing file names
* [datetime](https://docs.python.org/3/library/datetime.html) for all time data objects
* [logging](https://docs.python.org/3/library/logging.html)
* [pathlib](https://docs.python.org/3/library/pathlib.html)
* [locale](https://docs.python.org/3/library/locale.html)
* [base64](https://docs.python.org/3/library/base64.html)
* [json](https://docs.python.org/3/library/json.html) for event loading and saving
* [csv](https://docs.python.org/3/library/csv.html)
* [os](https://docs.python.org/3/library/os.html)

## Usage

Run the program using your usual Python IDE (like Visual Code) or via the console `python src\application.py`

### GUI

TODO

## Contributing

I encourage you to contribute to this project, in form of bug reports, feature requests
or code additions. Although it is likely that your contribution will not be implemented.

Please check out the [contribution](docs/CONTRIBUTING.md) guide for guidelines about how to proceed
as well as a styleguide.

## Credits
Up until now there are no further contributors other than the repository creator.

## License
This project is licensed under the [MIT License](LICENSE).
