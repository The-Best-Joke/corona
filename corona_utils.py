from datetime import datetime, date, timedelta
from variables.first_dates import *
import pandas as pd
import numpy as np
import math
import unidecode
import re


#dateparse = lambda x : datetime.strptime(x[:10], '%Y-%m-%d')

cases_colombia = pd.read_csv("Casos.csv",\
						parse_dates = ["Fecha diagnostico"],\
						#date_parser=dateparse)\
						)\
					.rename(\
		 				columns={"Fecha de notificación" : "date",\
		 						 "Fecha de muerte" : "date_death",\
		 			 			 "Ciudad de ubicación" : "city",\
		 			 			 "Departamento" : "dept",\
		 			 			 "Atención" : "locTreatment",\
		 			 			 "Edad" : "age",\
		 			 			 "Sexo" : "sex",\
		 			 			 "Tipo" : "type",\
		 			 			 "País de procedencia" : "origin"})\
					.drop('ID de caso', 1)

cases_worldwide = pd.read_csv("confirmed-global.csv")
deaths_worldwide = pd.read_csv("confirmed-global-deaths.csv")

def places():
	"""Handles the logic for determining whether the location is a Nan, multiple
	locations, or a straight-forward single location.

    Returns
    ----------
    places : Dictionary
    	The dictionary containing the countries of origin and the number of
    	cases
    possible_places : Dictionary
    	The dictionary containing the possible countries of origin and the
    	number of cases
    """
	places = {}
	possible_places = {}
	for location in cases_colombia.origin.tolist():
		resolve_places(places, possible_places, location)
	return places, possible_places

def resolve_places(places, possible_places, location):
	"""Handles the logic for determining whether the location is a Nan, multiple
	locations, or a straight-forward single location.

    Parameters
    ----------
    places : Dictionary
    	The dictionary containing the countries of origin and the number of
    	cases
    possible_places : Dictionary
    	The dictionary containing the possible countries of origin and the
    	number of cases
    locations : String OR Nan
    	A Nan, or, in the case of a string, either a list of locations or a
    	single location
    """
	if isinstance(location, float):
		resolve_nan(possible_places)
	elif "-" in location:
		add_possible_origins(possible_places, location)
	else:
		add_origin(places, location)

def resolve_nan(possible_places):
	if "Nan" in possible_places:
			possible_places["Nan"] += 1
	else:
		possible_places["Nan"] = 1

def add_possible_origins(possible_places, locations):
	"""Handles the logic for dealing with locations values with more than one
	possible origin country.

    Parameters
    ----------
    possible_places : Dictionary
    	The dictionary containing the possible countries of origin and the
    	number of cases. 
    locations : String
    	The list of possible locations of origin.
    """
	list_possible_places = locations.split("-")
	for place in list_possible_places:
		place = unidecode.unidecode(place.strip())
		if place in possible_places:
			possible_places[place] += 1
		else:
			possible_places[place] = 1

def add_origin(places, location):
	"""Adds the location to the places dictionary.

    Parameters
    ----------
    places : Dictionary
    	The dictionary containing the countries of origin and the number of
    	cases 
    location : String
    	The string value of the location
    """
	location = unidecode.unidecode(location)
	if location in places:
		places[location] += 1
	else:
		places[location] = 1

def fill_blank_days(dtfrm):
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
	s = cases_worldwide["Country/Region"]
	country_index = s[s == "Colombia"].index[0]
	date_cases = {}
	past_cases = 0
	for i in range(days_since_first_case().days + 1):
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
	s = deaths_worldwide["Country/Region"]
	country_index = s[s == "Colombia"].index[0]
	date_deaths = {}
	past_cases = 0
	for i in range(days_since_first_death().days + 1):
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
	places_origin, possible_origins = places()
	places_origin, possible_origins = pd.Series(places_origin).reset_index(),\
									  pd.Series(possible_origins).reset_index()
	places_origin.columns, possible_origins.columns = ["origin", "cases"],\
													  ["origin", "cases"]
	return places_origin, possible_origins

def total_cases_per_day():
	"""Returns a Dataframe object `tcpd` of the total number of cases per day in
	Colombia.

	Returns
    ----------
    tcpd : Dataframe
    	Dataframe with the total number of cases per day in Colombia
    """
	s = cases_worldwide["Country/Region"]
	country_index = s[s == "Colombia"].index[0]
	date_cases = {}
	for i in range(days_since_first_case().days + 1):
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
	s = deaths_worldwide["Country/Region"]
	country_index = s[s == "Colombia"].index[0]
	date_deaths = {}
	for i in range(days_since_first_death().days + 1):
		day = colombia_first_death_date + timedelta(days=i)
		day = datetime.strftime(day, "%-m/%-d/%y")
		curr_cases = deaths_worldwide[day].iloc[country_index].item()
		date_deaths[day] = curr_cases
	tdpd = pd.DataFrame(date_deaths.items(), columns=['date', 'deaths'])
	return tdpd

def days_since_first_case():
	"""Returns a Timedelta object with the number of days since the first
	reported case in Colombia.
    """
	last_date = datetime.strptime(cases_worldwide[cases_worldwide.columns[-1]]\
		.name, "%m/%d/%y")
	return last_date - colombia_first_date

def days_since_first_death():
	"""Returns a Timedelta object with the number of days since the first
	reported death in Colombia.
    """
	last_death_date = datetime.strptime(deaths_worldwide[deaths_worldwide\
		.columns[-1]].name, "%m/%d/%y")
	return last_death_date - colombia_first_death_date

def country_cases_progression(country, date):
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
	s = cases_worldwide["Country/Region"]
	country_index = s[s == country].index[0]
	progression_list = []
	for i in range(days_since_first_case().days + 14):
		day = date + timedelta(days=i)
		day = datetime.strftime(day, "%-m/%-d/%y")
		if day in cases_worldwide.columns:
			progression_list.append(cases_worldwide[day].iloc[country_index]\
							.item())
		else:
			break
	return progression_list

def country_deaths_progression(country, date):
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
	s = deaths_worldwide["Country/Region"]
	country_index = s[s == country].index[0]
	progression_list = []
	for i in range(days_since_first_death().days + 14):
		day = date + timedelta(days=i)
		day = datetime.strftime(day, "%-m/%-d/%y")
		if day in deaths_worldwide.columns:
			progression_list.append(deaths_worldwide[day].iloc[country_index]\
							.item())
		else:
			break
	return progression_list

def countries_cases_progression():
	"""Returns a Dataframe `df` containing the progressions of cases of all the
	countries of interest.

	Returns
    ----------
    df : Dataframe
    	A dataframe of the progressions of all countries from the first day of
    	their outbreak up until two weeks in advance of the amount of days
    	Colombia has endured.
    """
	colombia_array = country_cases_progression("Colombia", colombia_first_date)
	italy_array = country_cases_progression("Italy", italy_first_date)
	spain_array = country_cases_progression("Spain", spain_first_date)
	peru_array = country_cases_progression("Peru", peru_first_date)
	ecuador_array = country_cases_progression("Ecuador", ecuador_first_date)
	argentina_array = country_cases_progression("Argentina", argentina_first_date)
	chile_array = country_cases_progression("Chile", chile_first_date)
	venezuela_array = country_cases_progression("Venezuela", venezuela_first_date)
	brazil_array = country_cases_progression("Brazil", brazil_first_date)
	mexico_array = country_cases_progression("Mexico", mexico_first_date)

	data_columns = ["Colombia", "Italy", "Spain", "Peru", "Ecuador",\
					"Argentina", "Chile", "Venezuela", "Brazil", "Mexico"]

	data = dict(Colombia = np.array(colombia_array),\
				Italy = np.array(italy_array),\
				Spain = np.array(spain_array),\
				Peru = np.array(peru_array),\
				Ecuador = np.array(ecuador_array),\
				Argentina = np.array(argentina_array),\
				Chile = np.array(chile_array),\
				Venezuela = np.array(venezuela_array),\
				Brazil = np.array(brazil_array),\
				Mexico = np.array(mexico_array))

	df = pd.DataFrame(dict([ (k,pd.Series(v)) for k,v in data.items() ]))
	df.index.name = "day"
	df.index += 1
	return df

def countries_deaths_progression():
	"""Returns a Dataframe `df` containing the progressions of deaths of all the
	countries of interest.

	Returns
    ----------
    df : Dataframe
    	A dataframe of the progressions of deaths of all countries from the
    	first day of a reported death up until two weeks in advance of the
    	amount of days Colombia has endured.
    """
	colombia_array = country_deaths_progression("Colombia", colombia_first_death_date)
	italy_array = country_deaths_progression("Italy", italy_first_death_date)
	spain_array = country_deaths_progression("Spain", spain_first_death_date)
	peru_array = country_deaths_progression("Peru", peru_first_death_date)
	ecuador_array = country_deaths_progression("Ecuador", ecuador_first_death_date)
	argentina_array = country_deaths_progression("Argentina", argentina_first_death_date)
	chile_array = country_deaths_progression("Chile", chile_first_death_date)
	venezuela_array = country_deaths_progression("Venezuela", venezuela_first_death_date)
	brazil_array = country_deaths_progression("Brazil", brazil_first_death_date)
	mexico_array = country_deaths_progression("Mexico", mexico_first_death_date)

	data_columns = ["Colombia", "Italy", "Spain", "Peru", "Ecuador",\
					"Argentina", "Chile", "Venezuela", "Brazil", "Mexico"]

	data = dict(Colombia = np.array(colombia_array),\
				Italy = np.array(italy_array),\
				Spain = np.array(spain_array),\
				Peru = np.array(peru_array),\
				Ecuador = np.array(ecuador_array),\
				Argentina = np.array(argentina_array),\
				Chile = np.array(chile_array),\
				Venezuela = np.array(venezuela_array),\
				Brazil = np.array(brazil_array),\
				Mexico = np.array(mexico_array))

	df = pd.DataFrame(dict([ (k,pd.Series(v)) for k,v in data.items() ]))
	df.index.name = "day"
	df.index += 1
	return df
