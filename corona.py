"""Corona Script

Main script to be called for generating the csv files containing all of the
processed data of cases and deaths of Covid in Colombia and the world.
"""

from corona_utils import cases_per_day
from corona_utils import deaths_per_day
from corona_utils import cases_per_city
from corona_utils import cases_per_age
from corona_utils import total_cases_per_day
from corona_utils import total_deaths_per_day
from corona_utils import origins_and_possible
from corona_utils import countries_cases_progression
from corona_utils import countries_deaths_progression
from corona_utils import cities_cases_per_day
from corona_utils import cities_cases_progression
from corona_utils import cities_deaths_per_day
from corona_utils import cities_deaths_progression

# casesPerDept = data.dept.value_counts()
# casesPerLoc = data.locTreatment.value_counts()
# casesPerSex = data.sex.value_counts()
# casesPertype = data.type.value_counts()
# casesPerOrigin = data.origin.value_counts(dropna=False)

cases_per_day = cases_per_day()
deaths_per_day = deaths_per_day()
cases_per_city = cases_per_city()
cases_per_age = cases_per_age()
total_cases_per_day = total_cases_per_day()
total_deaths_per_day = total_deaths_per_day()
cases_per_origin, possible_origins_cases = origins_and_possible()
countries_cases_progression = countries_cases_progression()
countries_deaths_progression = countries_deaths_progression()
cities_cases_per_day()
cities_cases_progression()
cities_deaths_per_day()
cities_deaths_progression()

# Write CSVs
cases_per_day.to_csv("../covid-in-colombia/data/cases_per_day.csv")
deaths_per_day.to_csv("../covid-in-colombia/data/deaths_per_day.csv")
cases_per_city.to_csv("../covid-in-colombia/data/cases_per_city.csv")
cases_per_age.to_csv("../covid-in-colombia/data/cases_per_age.csv")
cases_per_origin.to_csv("../covid-in-colombia/data/cases_per_origin.csv")
possible_origins_cases.to_csv("../covid-in-colombia/data/"
	+ "possible_origins_cases.csv")
total_cases_per_day.to_csv("../covid-in-colombia/data/"
	+ "total_cases_per_day.csv")
total_deaths_per_day.to_csv("../covid-in-colombia/data/"
	+ "total_deaths_per_day.csv")
countries_cases_progression.to_csv("../covid-in-colombia/data/"
	+ "countries_progression.csv")
countries_deaths_progression.to_csv("../covid-in-colombia/data/"
	+ "countries_death_progression.csv")
###
