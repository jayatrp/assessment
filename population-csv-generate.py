import requests
import json
import csv
from collections import defaultdict
from typing import List

def prime_factors(n:int)->List[int]:
    factors = []
    while n % 2 == 0:
        factors.append(2)
        n = n // 2
    for i in range(3,int(n**(1/2))+1,2):
        while n % i== 0:
            factors.append(i)
            n = n // i
    if n > 2:
        factors.append(n)
    return factors

def population_change(prev_population:int, cur_population:int)->str:
    change = cur_population - prev_population
    percent = (change/prev_population)*100
    return f"{change} ({percent:.2f}%)"

# Send a GET request to the API and store the response
response = requests.get("https://datausa.io/api/data?drilldowns=State&measures=Population")

# Parse the JSON data from the response
responseData = json.loads(response.text)

# Create a default dictionary to store the data
population_data = defaultdict(lambda : defaultdict(int))

# Iterate through the data and store it in the dictionary
for item in responseData["data"]:
    state = item["State"]
    year = item["Year"]
    population = item["Population"]
    population_data[state][year] = population

# Open a CSV file for writing
with open("population_data.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)

    # Write the header row
    writer.writerow(["State Name", "2013", "2014", "2015", "2016", "2017", "2018", "2019", "2019 Factors"])

    # Write the data rows
    for state, years_data in population_data.items():
        population_change_list = []
        for year, population in years_data.items():
            if year == '2019 Factors':
                factors = prime_factors(population)
                factors = ';'.join(str(x) for x in factors)
                years_data[year] = f"{population} ({factors})"
            elif year != '2013':
                prev_population = population_data[state][str(int(year)-1)]
                population_change_list.append(population_change(prev_population,population))
                years_data[year] = f"{population} {population_change_list[-1]}"
        row = [state]
        row.extend([years_data[year] for year in ['2013', '2014', '2015', '2016', '2017', '2018', '2019']])
        writer.writerow(row)
