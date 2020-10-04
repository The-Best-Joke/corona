"""Downloader and Writer of Cases and Deaths

This script downloads – using the `requests` module – the global and Colombian
cases and deaths found in specific urls from the World Health Organization and
the Instituto Nacional de Salud, and writes that data to csv files within the
same directory.
"""

import requests

GLOBAL_CASES_URL = "https://raw.githubusercontent.com/CSSEGISandData/"\
                 + "COVID-19/master/csse_covid_19_data/"\
                 + "csse_covid_19_time_series/"\
                 + "time_series_covid19_confirmed_global.csv"
GLOBAL_DEATHS_URL = "https://raw.githubusercontent.com/CSSEGISandData/"\
                  + "COVID-19/master/csse_covid_19_data/"\
                  + "csse_covid_19_time_series/"\
                  + "time_series_covid19_deaths_global.csv"
COLOMBIA_CASES_URL = "https://www.datos.gov.co/api/views/gt2j-8ykr/"\
                   + "rows.csv?accessType=DOWNLOAD"

global_cases = requests.get(GLOBAL_CASES_URL, allow_redirects=True)
global_deaths = requests.get(GLOBAL_DEATHS_URL, allow_redirects=True)
colombia_cases = requests.get(COLOMBIA_CASES_URL, allow_redirects=True)

open("confirmed-global.csv", "wb").write(global_cases.content)
open("confirmed-global-deaths.csv", "wb").write(global_deaths.content)
open("Casos.csv", "wb").write(colombia_cases.content)
