# roskilde
Scraping data fra Roskilde Festival homepage

## Prerequisites

Ensure that you have Python 3 installed. You can download Python 3 from the official website: [python.org](https://www.python.org/downloads/).

## Installing Dependencies

To run the script handle_data.py, you need to install the required dependencies. The dependencies for this script are listed below:

- `os` (part of Python standard library, no need to install)
- `json` (part of Python standard library, no need to install)
- `bs4` (BeautifulSoup)
- `datetime` (part of Python standard library, no need to install)
- `csv` (part of Python standard library, no need to install)

### Using `pip`

The easiest way to install the required dependencies is by using `pip`, the Python package installer. You can install the dependencies using the following command:

```sh
pip install beautifulsoup4
```
# running the code
go to the map 24, the first run getBands.sh:
```sh
./getBands.sh
```
This scrapes the roskilde homepage and creates a json file for each band.

Then run handle_data.py:
```sh
./handle_data.py
```
This creates a csv-file that can be used in a spreadsheet
