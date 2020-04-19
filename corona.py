from corona_utils import *
from variables.first_dates import *

# casesPerDept = data.dept.value_counts()
# casesPerLoc = data.locTreatment.value_counts()
# casesPerSex = data.sex.value_counts()
# casesPertype = data.type.value_counts()
# casesPerOrigin = data.origin.value_counts(dropna=False)

cases_per_day = cases_per_day()
cases_per_city = cases_per_city()
cases_per_age = cases_per_age()
total_cases_per_day = total_cases_per_day()
cases_per_origin, possible_origins_cases = origins_and_possible()
progression_countries = countries_progression()

# Write CSVs
cases_per_day.to_csv("../covid-project/public/data/cases_per_day.csv")
cases_per_city.to_csv("../covid-project/public/data/cases_per_city.csv")
cases_per_age.to_csv("../covid-project/public/data/cases_per_age.csv")
cases_per_origin.to_csv("../covid-project/public/data/cases_per_origin.csv")
possible_origins_cases.to_csv("../covid-project/public/data/possible_origins_cases.csv")
total_cases_per_day.to_csv("../covid-project/public/data/total_cases_per_day.csv")
progression_countries.to_csv("../covid-project/public/data/countries_progression.csv")
###