import os
import copy
import requests
import itertools
from terminaltables import AsciiTable
from dotenv import load_dotenv


def predict_rub_salary(salary_from, salary_to):
    if salary_from and salary_to:
        return (salary_from + salary_to) / 2
    elif salary_from:
        return salary_from * 1.2
    else:
        return salary_to * 0.8


def get_hh_statistic(prog_language, area, period):
    url = 'https://api.hh.ru/vacancies'

    vacancy_tittle = f'{prog_language} developer'
    count_per_page = 100
    salaries = []

    for page in itertools.count(0):
        params = {
            'text': vacancy_tittle,
            'page': page,
            'per_page': count_per_page,
            'area': area,
            'period': period
        }

        response = requests.get(url, params=params)
        response.raise_for_status()

        for vacancy in response.json()['items']:
            try:
                salary_from = vacancy['salary']['from']
                salary_to = vacancy['salary']['to']
                currency = vacancy['salary']['currency']
                if currency == 'RUR' and (salary_from or salary_to):
                    salaries.append(predict_rub_salary(salary_from, salary_to))
            except TypeError:
                continue

        if page >= response.json()['pages']:
            break

    try:
        average_salary = int(sum(salaries) / len(salaries))
    except ZeroDivisionError:
        average_salary = 'Not specified'

    return [
        prog_language,
        response.json()['found'],
        len(salaries), average_salary
    ]


def get_sj_statistic(prog_language, sj_key, area, period):
    url = 'https://api.superjob.ru/2.0/vacancies'

    developer_catalog_id = 48
    count_per_page = 100
    salaries = []

    for page in itertools.count(0):
        headers = {'X-Api-App-Id': sj_key}
        params = {
            'keyword': prog_language,
            'catalogues': developer_catalog_id,
            'period': period,
            'page': page,
            'count': count_per_page,
            't': area
        }

        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()

        for vacancy in response.json()['objects']:
            try:
                salary_from = vacancy['payment_from']
                salary_to = vacancy['payment_to']
                if vacancy['currency'] == 'rub' and (salary_from or salary_to):
                    salaries.append(predict_rub_salary(salary_from, salary_to))
            except TypeError:
                continue

        if page >= response.json()['total'] / count_per_page:
            break

    try:
        average_salary = int(sum(salaries) / len(salaries))
    except ZeroDivisionError:
        average_salary = 'Not specified'

    return [
        prog_language,
        response.json()['total'],
        len(salaries), average_salary
    ]


if __name__ == '__main__':
    load_dotenv()

    hh_area = os.environ['HH_AREA']
    hh_period = os.environ['HH_PERIOD']

    sj_key = os.environ['SJ_KEY']
    sj_area = os.environ['SJ_AREA']
    sj_period = os.environ['SJ_PERIOD']

    prog_languages = [
        'JavaScript', 'Java', 'Python', 'Ruby', 'PHP', 'C++', 'C#', 'C', 'GO',
        'Swift', 'TypeScript', 'Kotlin', 'Objective-C', 'Scala', 'Rust'
    ]

    hh_table_columns = [[
        'Programming language', 'Vacancies_found', 'Vacancies_processed',
        'Average_salary'
    ]]

    sj_table_columns = copy.deepcopy(hh_table_columns)

    for prog_language in prog_languages:
        hh_table_columns.append(
            get_hh_statistic(prog_language, hh_area, hh_period))
        sj_table_columns.append(
            get_sj_statistic(prog_language, sj_key, sj_area, sj_period))

    print(AsciiTable(hh_table_columns, 'HeadHunter').table)
    print(AsciiTable(sj_table_columns, 'SuperJob').table)
