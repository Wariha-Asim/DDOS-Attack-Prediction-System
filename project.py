import random
import csv

countries = ["India", "Pakistan", "China", "Japan", "Bangladesh"]  

data = []
attack_types = ["UDP Flood", "SYN Flood", "ICMP Flood", "HTTP Flood", "DNS Amplification"]

for i in range(4000):
    year = random.choice([2019, 2020, 2021, 2022, 2023,2024])
    country = random.choice(countries)
    attacks = random.randint(10, 100)
    attack_type = random.choice(attack_types)

    data.append([year, country, attacks, attack_type])

with open("fake_ddos_data.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Year", "Country", "Attacks", "Attack_Type"])  
    writer.writerows(data)

print("Dataset generated successfully!")
