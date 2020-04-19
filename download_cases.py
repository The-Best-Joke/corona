import requests

global_cases_link = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv"
colombia_cases_link = "https://www.datos.gov.co/api/views/gt2j-8ykr/rows.csv?accessType=DOWNLOAD"
global_cases = requests.get(global_cases_link, allow_redirects=True)
colombia_cases = requests.get(colombia_cases_link, allow_redirects=True)
open("confirmed-global.csv", "wb").write(global_cases.content)
open("Casos.csv", "wb").write(colombia_cases.content)