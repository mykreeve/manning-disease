import geonamescache
import re
import unidecode
import pandas as pd
gc = geonamescache.GeonamesCache()

df = pd.DataFrame(columns=['headline','city','country'])

headlines = open('headlines.txt', 'r')
for n,line in enumerate(headlines):
	line = line.replace('\n','')
	possible_cities = []
	possible_countries = []
	for c in gc.get_cities():
		city = unidecode.unidecode(gc.get_cities()[c]['name'])
		if city in unidecode.unidecode(line):
			possible_cities.append(gc.get_cities()[c]['name'])
	for c in gc.get_countries_by_names():
		if unidecode.unidecode(c) in unidecode.unidecode(line):
			possible_countries.append(c)

	best_city = None
	length = 0

	if len(possible_cities) > 0:
		for p in possible_cities:
			if len(p) > length: 
				best_city = p
				length = len(p)
	
	if len(possible_countries) == 0 and len(possible_cities) > 0:
		city = (gc.get_cities_by_name(best_city)[0])
		key = list(city.keys())[0]
		possible_countries.append(gc.get_countries()[city[key]['countrycode']]['name'])

	# print (line, '-', best_city, '-', possible_countries[0])
	best_country = None
	if len(possible_countries) > 0:
		best_country = possible_countries[0]

	df = df.append({'headline': line, 'city': best_city, 'country': best_country}, ignore_index=True)
	print (n+1)

print (df)
