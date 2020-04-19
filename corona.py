from corona_utils import *
from variables.first_dates import *
import numpy as np

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

progression_colombia = resolve_progression_dicts("Colombia", colombia_first_date)
progression_italy = resolve_progression_dicts("Italy", italy_first_date)
progression_spain = resolve_progression_dicts("Spain", spain_first_date)
progression_peru = resolve_progression_dicts("Peru", peru_first_date)
progression_ecuador = resolve_progression_dicts("Ecuador", ecuador_first_date)
progression_venezuela = resolve_progression_dicts("Venezuela", venezuela_first_date)
progression_brazil = resolve_progression_dicts("Brazil", brazil_first_date)
progression_mexico = resolve_progression_dicts("Mexico", mexico_first_date)

# Write CSVs
cases_per_day.to_csv("../covid-project/public/data/cases_per_day.csv")
cases_per_city.to_csv("../covid-project/public/data/cases_per_city.csv")
cases_per_age.to_csv("../covid-project/public/data/cases_per_age.csv")
cases_per_origin.to_csv("../covid-project/public/data/cases_per_origin.csv")
possible_origins_cases.to_csv("../covid-project/public/data/possible_origins_cases.csv")
total_cases_per_day.to_csv("../covid-project/public/data/total_cases_per_day.csv")
###

# Write progression arrays
np.savetxt('../covid-project/public/data/progression_colombia.txt', progression_colombia, fmt='%i', delimiter=',')
np.savetxt('../covid-project/public/data/progression_italy.txt', progression_italy, fmt='%i', delimiter=',')
np.savetxt('../covid-project/public/data/progression_spain.txt', progression_spain, fmt='%i', delimiter=',')
np.savetxt('../covid-project/public/data/progression_peru.txt', progression_peru, fmt='%i', delimiter=',')
np.savetxt('../covid-project/public/data/progression_ecuador.txt', progression_ecuador, fmt='%i', delimiter=',')
np.savetxt('../covid-project/public/data/progression_venezuela.txt', progression_venezuela, fmt='%i', delimiter=',')
np.savetxt('../covid-project/public/data/progression_brazil.txt', progression_brazil, fmt='%i', delimiter=',')
np.savetxt('../covid-project/public/data/progression_mexico.txt', progression_mexico, fmt='%i', delimiter=',')
###