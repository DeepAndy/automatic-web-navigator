## Summary
This software is designed to automate reptitive web tasks such as clicking
the same button across a large portion of websites.

This software is not yet complete and should not be used for any important tasks.
Since the software is incomplete, it can cause a large amount of damage if not
used with proper care. Use at your own risk.

## Required Software
* [Python 2](https://www.python.org/downloads)

* [Python 2 pip](https://www.makeusof.com/tag/install-pip-for-python/)

* Python 2 selenium module

    * `pip install selenium`

    * `pip install bs4`

* Web Driver

    * [Chrome Driver](https://sites.google.com/a/chromium.org/chromedriver/downloads)

    * [Firefox Driver](https://github.com/mozilla/geckodriver/releases)

## How to use
Using a terminal, type this command

`python navigator.py`

Note that some operating systems will require you to run Python as `python2`

The above command will present the user with a menu to manage website and action
queues.

## Notes
The chromedriver executable path is set to my personal directory for now.
You will have to change the path in *config.ini* to get it to work.

## License
This software is licensed under the MIT license.
