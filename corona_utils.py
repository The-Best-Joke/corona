"""
Utils file which contains several useful functions for processing, organizing
and writing data related to Covid cases and deaths in Colombia and the world.

Functions
----------
cases_per_day : Dataframe
    Returns a Dataframe object of the number of cases per day in Colombia
cases_per_city : Dataframe
    Returns a Dataframe object of the total number of cases per city in Colombia
deaths_per_day : Dataframe
    Returns a Dataframe object of the number of deaths per day in Colombia
cases_per_city : Dataframe
    Returns a Dataframe object of the total number of cases per city in Colombia
cases_per_age : Dataframe
    Returns a Dataframe object of the total number of cases per age group in
    Colombia
total_cases_per_day : Dataframe
    Returns a Dataframe object of the total number of cases per day in Colombia
total_deaths_per_day : Dataframe
    Returns a Dataframe object of the total number of deaths per day in Colombia
origins_and_possible : (Series, Series)
    Returns two Series objects that list the original locations of where cases
    came from, and the possible places where some cases came from, respectively
countries_cases_progression : Dataframe
    Returns a Dataframe containing the progressions of cases of all the
    countries of interest
countries_deaths_progression : Dataframe
    Returns a Dataframe containing the progressions of deaths of all the
    countries of interest
cities_cases_per_day : None
    Writes a csv file for each Series representing the cases per day of every
    single city with a diagnosed case in Colombia
cities_cases_progression : None
    Writes a csv file for each Series representing the cumulative cases per day
    of every single city with a diagnosed case in Colombia
cities_deaths_per_day : None
    Writes a csv file for each Series representing the cases per day of every
    single city with a reported death in Colombia
cities_deaths_progression : None
    Writes a csv file for each Series representing the cumulative deaths per day
    of every single city with a reported death in Colombia
"""

from datetime import datetime, timedelta
import unidecode
import pandas as pd
import numpy as np
from variables.first_dates import spain_first_date
from variables.first_dates import italy_first_date
from variables.first_dates import brazil_first_date
from variables.first_dates import ecuador_first_date
from variables.first_dates import mexico_first_date
from variables.first_dates import peru_first_date
from variables.first_dates import venezuela_first_date
from variables.first_dates import colombia_first_date
from variables.first_dates import argentina_first_date
from variables.first_dates import chile_first_date
from variables.first_dates import spain_first_death_date
from variables.first_dates import italy_first_death_date
from variables.first_dates import brazil_first_death_date
from variables.first_dates import ecuador_first_death_date
from variables.first_dates import mexico_first_death_date
from variables.first_dates import peru_first_death_date
from variables.first_dates import venezuela_first_death_date
from variables.first_dates import colombia_first_death_date
from variables.first_dates import argentina_first_death_date
from variables.first_dates import chile_first_death_date

#dateparse = lambda x : datetime.strptime(x[:10], '%Y-%m-%d')

cases_colombia = pd.read_csv("Casos.csv",
    parse_dates = ["Fecha de diagnóstico"]).rename(
        columns = {
            "Fecha de notificación" : "date",
            "Fecha de muerte" : "date_death",
            "Nombre municipio" : "city",
            "Departamento" : "dept",
            "Atención" : "locTreatment",
            "Edad" : "age",
            "Sexo" : "sex",
            "Tipo" : "type",
            "Nombre del país" : "origin"
        }
    ).drop('ID de caso', 1)

cases_worldwide = pd.read_csv("confirmed-global.csv")
deaths_worldwide = pd.read_csv("confirmed-global-deaths.csv")

def __get_locations():
    """Get the dictionaries of the locations and possible locations of cases
    reported in Colombia.

    Returns
    ----------
    locations : Dictionary
        The dictionary containing the locations of origin and the number of
        cases
    possible_locations : Dictionary
        The dictionary containing the possible locations of origin and the
        number of cases
    """
    locations = {}
    possible_locations = {}
    for location in cases_colombia.origin.tolist():
        __resolve_locations(locations, possible_locations, location)
    return locations, possible_locations

def __resolve_locations(locations, possible_locations, location):
    """Handles the logic for determining whether the location is a Nan, multiple
    locations, or a straight-forward single location.

    Parameters
    ----------
    locations : Dictionary
        The dictionary containing the locations of origin and the number of
        cases
    possible_locations : Dictionary
        The dictionary containing the possible locations of origin and the
        number of cases
    location : String OR Nan
        A Nan, or, in the case of a string, either a list of locations or a
        single location

    Returns
    ----------
    None
    """
    if isinstance(location, float):
        __resolve_nan(possible_locations)
    elif "-" in location:
        __add_possible_locations(possible_locations, location)
    else:
        __add_location(locations, location)

def __resolve_nan(possible_locations):
    if "Nan" in possible_locations:
        possible_locations["Nan"] += 1
    else:
        possible_locations["Nan"] = 1

def __add_possible_locations(possible_locations, locations):
    """Handles the logic for dealing with locations values with more than one
    possible origin country.

    Parameters
    ----------
    possible_locations : Dictionary
        The dictionary containing the possible locations of origin and the
        number of cases.
    locations : String
        The list of possible locations of origin.

    Returns
    ----------
    None
    """
    list_possible_places = locations.split("-")
    for place in list_possible_places:
        place = unidecode.unidecode(place.strip())
        if place in possible_locations:
            possible_locations[place] += 1
        else:
            possible_locations[place] = 1

def __add_location(locations, location):
    """Adds the location to the locations dictionary.

    Parameters
    ----------
    locations : Dictionary
        The dictionary containing the locations of origin and the number of
        cases
    location : String
        The string value of the location

    Returns
    ----------
    None
    """
    location = unidecode.unidecode(location)
    if location in locations:
        locations[location] += 1
    else:
        locations[location] = 1

def __fill_blank_days(dtfrm):
    """Adds missing days to the provided dataframe.

    For all missing days, the date is filled with a corresponding 0 value.

    Parameters
    ----------
    dtfrm : Dataframe
        A Dataframe object containing a linear (though incomplete) progression
        of days

    Returns
    ----------
    dtfrm : Dataframe
        A Dataframe with a clean linear progression of days
    """
    first_date = dtfrm.iloc[0]
    last_date = dtfrm.iloc[-1]
    date_range = pd.date_range(first_date.name, last_date.name)
    return dtfrm.reindex(date_range, fill_value=0)

def cases_per_day():
    """Returns a Dataframe object `cpd` of the number of cases per day in
    Colombia.

    Returns
    ----------
    cpd : Dataframe
        A Dataframe that contains the total number of cases per day in Colombia
    """
    location = cases_worldwide["Country/Region"]
    country_index = location[location == "Colombia"].index[0]
    date_cases = {}
    past_cases = 0
    for i in range(__days_since_first_case().days + 1):
        day = colombia_first_date + timedelta(days=i)
        day = datetime.strftime(day, "%-m/%-d/%y")
        curr_cases = cases_worldwide[day].iloc[country_index].item()
        date_cases[day] = curr_cases - past_cases
        past_cases = curr_cases
    cpd = pd.DataFrame(date_cases.items(), columns=['date', 'cases'])
    return cpd

def deaths_per_day():
    """Returns a Dataframe object `dpd` of the number of deaths per day in
    Colombia.

    Returns
    ----------
    dpd : Dataframe
        A Dataframe that contains the total number of deaths per day in Colombia
    """
    location = deaths_worldwide["Country/Region"]
    country_index = location[location == "Colombia"].index[0]
    date_deaths = {}
    past_cases = 0
    for i in range(__days_since_first_death().days + 1):
        day = colombia_first_death_date + timedelta(days=i)
        day = datetime.strftime(day, "%-m/%-d/%y")
        curr_cases = deaths_worldwide[day].iloc[country_index].item()
        date_deaths[day] = curr_cases - past_cases
        past_cases = curr_cases
    dpd = pd.DataFrame(date_deaths.items(), columns=['date', 'deaths'])
    return dpd

def cases_per_city():
    """Returns a Dataframe object `cpc` of the total number of cases per city in
    Colombia.

    Returns
    ----------
    cpc : Dataframe
        A Dataframe that contains the total number of cases per city in Colombia
    """
    cpc = cases_colombia.city.value_counts().reset_index()
    cpc.columns = ["city", "cases"]
    return cpc

def cases_per_age():
    """Returns a Dataframe object `cpa` of the total number of cases per age
    group in Colombia.

    Returns
    ----------
    cpa : Dataframe
        A Dataframe that contains the total number of cases per age group in
        Colombia
    """
    cpa = pd.DataFrame(cases_colombia.age.value_counts())\
        .rename(columns={"age" : "cases"})
    cpa.index.name = "age group"
    return cpa

def origins_and_possible():
    """Returns two Series objects, `places_origin` and `possible_origin`, that
    list the original locations of where cases came from, and the possible
    places where some cases came from, respectively.

    Returns
    ----------
    places_origin : Series
        A series that lists the original locations of where cases came from
    possible_origins : Series
        A series that lists the possible places where some cases came from
    """
    places_origin, possible_origins = __get_locations()
    places_origin = pd.Series(places_origin).reset_index()
    possible_origins = pd.Series(possible_origins).reset_index()
    places_origin.columns = ["origin", "cases"]
    possible_origins.columns = ["origin", "cases"]
    return places_origin, possible_origins

def total_cases_per_day():
    """Returns a Dataframe object `tcpd` of the total number of cases per day in
    Colombia.

    Returns
    ----------
    tcpd : Dataframe
        Dataframe with the total number of cases per day in Colombia
    """
    location = cases_worldwide["Country/Region"]
    country_index = location[location == "Colombia"].index[0]
    date_cases = {}
    for i in range(__days_since_first_case().days + 1):
        day = colombia_first_date + timedelta(days=i)
        day = datetime.strftime(day, "%-m/%-d/%y")
        curr_cases = cases_worldwide[day].iloc[country_index].item()
        date_cases[day] = curr_cases
    tcpd = pd.DataFrame(date_cases.items(), columns=['date', 'cases'])
    return tcpd

def total_deaths_per_day():
    """Returns a Dataframe object `tdpd` of the total number of deaths per day
    in Colombia.

    Returns
    ----------
    tdpd : Dataframe
        Dataframe with the total number of deaths per day in Colombia
    """
    location = deaths_worldwide["Country/Region"]
    country_index = location[location == "Colombia"].index[0]
    date_deaths = {}
    for i in range(__days_since_first_death().days + 1):
        day = colombia_first_death_date + timedelta(days=i)
        day = datetime.strftime(day, "%-m/%-d/%y")
        curr_cases = deaths_worldwide[day].iloc[country_index].item()
        date_deaths[day] = curr_cases
    tdpd = pd.DataFrame(date_deaths.items(), columns=['date', 'deaths'])
    return tdpd

def __days_since_first_case():
    """Returns a Timedelta object with the number of days since the first
    reported case in Colombia.

    Returns
    ----------
    Timedelta
    """
    last_date = datetime.strptime(cases_worldwide[cases_worldwide.columns[-1]]
        .name, "%m/%d/%y")
    return last_date - colombia_first_date

def __days_since_first_death():
    """Returns a Timedelta object with the number of days since the first
    reported death in Colombia.

    Returns
    ----------
    Timedelta
    """
    last_death_date = datetime.strptime(deaths_worldwide[deaths_worldwide
        .columns[-1]].name, "%m/%d/%y")
    return last_death_date - colombia_first_death_date

def __city_cases_per_day(city):
    """Returns a Series object `ccpd` with the cases per day in the city
    provided.

    Parameters
    ----------
    city : String
        A string object value of the city whose cases per day is being returned

    Returns
    ----------
    ccpd : Series
        A Series that contains the cases per day in the city
    """
    ccpd = cases_colombia[(cases_colombia["city"] == city)
        & cases_colombia["date_death"].isnull()]
    ccpd = ccpd[["date", "city"]]
    ccpd = ccpd.date.value_counts().sort_index()
    return ccpd

def __city_cases_progression(city):
    """Returns a Series object `ccp` with the cumulative cases per day in the
    city provided.

    Parameters
    ----------
    city : String
        A string object value of the city whose progression of cases is being
        returned

    Returns
    ----------
    cccp : Series
        A Series that contains the cumulative progression of cases in the city
    """
    ccp = __city_cases_per_day(city).cumsum()
    return ccp

def __country_cases_progression(country, date):
    """Returns a list `progression_list` containing the progression of cases in
    the country provided.

    For countries that have had more days since their first reported case than
    Colombia, up to two extra weeks of the progression is also returned.

    Parameters
    ----------
    country : String
        A string object value of the country whose progression is being
        generated

    date : Datetime
        A datetime object whose value is the first date of a reported Covid case
        in the country

    Returns
    ----------
    progression_list : List
        A list containing the progressive increase in cases in the country
        provided
    """
    location = cases_worldwide["Country/Region"]
    country_index = location[location == country].index[0]
    progression_list = []
    for i in range(__days_since_first_case().days + 14):
        day = date + timedelta(days=i)
        day = datetime.strftime(day, "%-m/%-d/%y")
        if day in cases_worldwide.columns:
            progression_list.append(cases_worldwide[day]
                .iloc[country_index].item())
        else:
            break
    return progression_list

def __city_deaths_per_day(city):
    """Returns a Series object `cdpd` with the deaths per day in the city
    provided.

    Parameters
    ----------
    city : String
        A string object value of the city whose deaths of deaths is being
        returned

    Returns
    ----------
    cdpd : Series
        A Series that contains the deaths per day in the city
    """
    cdpd = cases_colombia[(cases_colombia["city"] == city)
        & cases_colombia["date_death"].notnull()]
    cdpd = cdpd[["date", "city"]]
    cdpd = cdpd.date.value_counts().sort_index()
    return cdpd

def __city_deaths_progression(city):
    """Returns a Series object `cdp` with the cumulative deaths per day in the
    city provided.

    Parameters
    ----------
    city : String
        A string object value of the city whose progression of deaths is being
        returned

    Returns
    ----------
    cccp : Series
        A Series that contains the cumulative progression of deaths in the city
    """
    cdp = __city_deaths_per_day(city).cumsum()
    return cdp

def __country_deaths_progression(country, date):
    """Returns a list `progression_list` containing the progression of deaths in
    the country provided.

    For countries that have had more days since their first reported death than
    Colombia, up to two extra weeks of the progression is also returned.

    Parameters
    ----------
    country : String
        A string object value of the country whose progression is being
        generated

    date : Datetime
        A datetime object whose value is the first date of a reported Covid
        death in the country

    Returns
    ----------
    progression_list : List
        A list containing the progressive increase in deaths in the country
        provided
    """
    location = deaths_worldwide["Country/Region"]
    country_index = location[location == country].index[0]
    progression_list = []
    for i in range(__days_since_first_death().days + 14):
        day = date + timedelta(days=i)
        day = datetime.strftime(day, "%-m/%-d/%y")
        if day in deaths_worldwide.columns:
            progression_list.append(deaths_worldwide[day]
                .iloc[country_index].item())
        else:
            break
    return progression_list

def cities_cases_per_day():
    """Writes a csv file for each Series representing the cases per day of every
    single city with a diagnosed case in Colombia.

    Returns
    ----------
    None
    """
    cities = cases_colombia.city.unique()
    for city in cities:
        city_cases = __city_cases_per_day(city)
        city_cases.index.name = "date"
        city_cases.index = pd.to_datetime(city_cases.index,
            format="%d/%m/%Y %H:%M:%S")
        city_cases = city_cases.sort_index()
        city_cases.to_csv("../covid-in-colombia/data/cities/cases/per_day/"
            + city.lower() + ".csv", header=["cases"])

def cities_cases_progression():
    """Writes a csv file for each Series representing the cumulative cases per
    day of every single city with a diagnosed case in Colombia.

    Returns
    ----------
    None
    """
    cities = cases_colombia.city.unique()
    for city in cities:
        city_cases = __city_cases_progression(city)
        city_cases.index.name = "date"
        city_cases.index = pd.to_datetime(city_cases.index,
            format="%d/%m/%Y %H:%M:%S")
        city_cases = city_cases.sort_index()
        city_cases.to_csv("../covid-in-colombia/data/cities/cases/total/"
            + city.lower() + ".csv", header=["cases"])

def cities_deaths_per_day():
    """Writes a csv file for each Series representing the cases per day of every
    single city with a reported death in Colombia.

    Returns
    ----------
    None
    """
    cities = cases_colombia.city.unique()
    for city in cities:
        city_deaths = __city_deaths_per_day(city)
        city_deaths.index.name = "date"
        city_deaths.index = pd.to_datetime(city_deaths.index,
            format="%d/%m/%Y %H:%M:%S")
        city_deaths = city_deaths.sort_index()
        city_deaths.to_csv("../covid-in-colombia/data/cities/deaths/per_day/"
            + city.lower() + ".csv", header=["deaths"])

def cities_deaths_progression():
    """Writes a csv file for each Series representing the cumulative deaths per
    day of every single city with a reported death in Colombia.

    Returns
    ----------
    None
    """
    cities = cases_colombia.city.unique()
    for city in cities:
        city_deaths = __city_deaths_progression(city)
        city_deaths.index.name = "date"
        city_deaths.index = pd.to_datetime(city_deaths.index,
            format="%d/%m/%Y %H:%M:%S")
        city_deaths = city_deaths.sort_index()
        city_deaths.to_csv("../covid-in-colombia/data/cities/deaths/total/"
            + city.lower() + ".csv", header=["deaths"])

def countries_cases_progression():
    """Returns a Dataframe `dataframe` containing the progressions of cases of
    all the countries of interest.

    Returns
    ----------
    dataframe : Dataframe
        A dataframe of the progressions of all countries from the first day of
        their outbreak up until two weeks in advance of the amount of days
        Colombia has endured.
    """
    colombia = __country_cases_progression("Colombia", colombia_first_date)
    italy = __country_cases_progression("Italy", italy_first_date)
    spain = __country_cases_progression("Spain", spain_first_date)
    peru = __country_cases_progression("Peru", peru_first_date)
    ecuador = __country_cases_progression("Ecuador", ecuador_first_date)
    argentina = __country_cases_progression("Argentina", argentina_first_date)
    chile = __country_cases_progression("Chile", chile_first_date)
    venezuela = __country_cases_progression("Venezuela", venezuela_first_date)
    brazil = __country_cases_progression("Brazil", brazil_first_date)
    mexico = __country_cases_progression("Mexico", mexico_first_date)

    data = dict(Colombia = np.array(colombia),
                Italy = np.array(italy),
                Spain = np.array(spain),
                Peru = np.array(peru),
                Ecuador = np.array(ecuador),
                Argentina = np.array(argentina),
                Chile = np.array(chile),
                Venezuela = np.array(venezuela),
                Brazil = np.array(brazil),
                Mexico = np.array(mexico))

    dataframe = pd.DataFrame({k : pd.Series(v) for k, v in data.items()})
    dataframe.index.name = "day"
    dataframe.index += 1
    return dataframe

def countries_deaths_progression():
    """Returns a Dataframe `dataframe` containing the progressions of deaths of
    all the countries of interest.

    Returns
    ----------
    dataframe : Dataframe
        A dataframe of the progressions of deaths of all countries from the
        first day of a reported death up until two weeks in advance of the
        amount of days Colombia has endured.
    """
    italy = __country_deaths_progression("Italy", italy_first_death_date)
    spain = __country_deaths_progression("Spain", spain_first_death_date)
    peru = __country_deaths_progression("Peru", peru_first_death_date)
    ecuador = __country_deaths_progression("Ecuador", ecuador_first_death_date)
    chile = __country_deaths_progression("Chile", chile_first_death_date)
    brazil = __country_deaths_progression("Brazil", brazil_first_death_date)
    mexico = __country_deaths_progression("Mexico", mexico_first_death_date)
    colombia = __country_deaths_progression("Colombia",\
        colombia_first_death_date)
    argentina = __country_deaths_progression("Argentina",\
        argentina_first_death_date)
    venezuela = __country_deaths_progression("Venezuela",\
        venezuela_first_death_date)

    data = dict(Colombia = np.array(colombia),
                Italy = np.array(italy),
                Spain = np.array(spain),
                Peru = np.array(peru),
                Ecuador = np.array(ecuador),
                Argentina = np.array(argentina),
                Chile = np.array(chile),
                Venezuela = np.array(venezuela),
                Brazil = np.array(brazil),
                Mexico = np.array(mexico))

    dataframe = pd.DataFrame({k : pd.Series(v) for k, v in data.items()})
    dataframe.index.name = "day"
    dataframe.index += 1
    return dataframe
