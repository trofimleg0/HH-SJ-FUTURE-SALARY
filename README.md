# HH-and-SJ-Future-Salary #

The script receives and downloads developer vacancies for 15 popular programming languages from [HeadHunter](https://hh.ru) and [SuperJob](https://www.superjob.ru) using the API.
Analyzes and calculates the average salary for each of them

## How to install ##

Python should be already installed.

Use `pip`(or `pip3` for Python3) to install dependencies:

```commandline
pip install -r requirements.txt
```

Recommended using [virtualenv/venv](https://docs.python.org/3/library/venv.html)

## Launch ##
1) You need to get [SJ key](https://api.superjob.ru/info/)
2) Add to `.env` file:
    - `HH_AREA` Area for HeadHunter request (Example:HH_AREA=1 - Moscow)
    - `HH_PERIOD` Period of published vacancies for HeadHunter request (Example: `HH_PERIOD=7` - Last 7 days)
    - `SJ_KEY` Your generated SuperJob Key
    - `SJ_AREA` Area for SuperJob request (Example:SJ_AREA=4 - Moscow)
    - `SJ_PERIOD` Period of published vacancies for SuperJob request (Example: `SJ_PERIOD=7` - Last 7 days)
3) Run `main.py`

```commandline
python main.py
```

Example:  
HeadHunter: `Area`: Moscow, `Period`: 1 day
SuperJob: `Area`: Moscow, `Period`: 7 days

![Image alt](https://github.com/{trofimleg0}/{repository}/raw/{main}/{path}/Example.png)