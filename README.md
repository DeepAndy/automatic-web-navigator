## Summary
This software is designed to automate reptitive web tasks such as clicking
the same button across a large portion of websites.

This software must be used with care.

## Required Software
* [Python 3](https://www.python.org/downloads)

* Python 3 pip (Should be installed with Python 3)

* Python 3 selenium module

    * `pip3 install selenium`

    * `pip3 install bs4`

* Web Driver

    * [Chrome Driver](https://sites.google.com/a/chromium.org/chromedriver/downloads)

    * [Firefox Driver](https://github.com/mozilla/geckodriver/releases)

## How to use
Using a terminal, type this command

`python3 navigator.py`

The above command will present the user with a menu to manage website and action
queues.

## Special Mac setup
On MacOS, you will need to install the proper certificates for Python to connect
to pages. You will need to run the following code in a terminal:

`sudo /Applications/Python\ 3.7/Install\ Certificates.command`

## Trello
This project now keeps track of tasks on Trello.
The link can be found [here.](https://trello.com/b/NrBC6CaV/automatic-web-navigator)

## Notes
The chromedriver and geckodriver executable path is set to my personal directory for now.
You will have to change the path in *config.ini* to get it to work.

Also, many of the scripts here are for my work at the Office of Information Technology (OIT)
at Ohio University. Most of these one time companion scripts are stored in the legacy-companion
and legacy-main directories.

## License
This software is licensed under the MIT license.
