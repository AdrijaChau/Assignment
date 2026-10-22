import pandas as pd
df=pd.read_csv("urban_mobility.csv")
print(df.head())

df["Energy_Per_Km"]=df["Energy_Used_kWh"]/df["Distance_Km"]
print(df[["Trip_ID","Energy_Per_Km"]])

result=df[
    (df["Vehicle_Type"]=="Electric Van")&
    (df["Maintenance_Flag"]=="Yes")
]
print(result)

result=df.groupby("Vehicle_Type").agg(
    Average_Distance_km=("Distance_Km","mean"),
    Total_Trips=("Trips_Count","sum")
)
print(result)

import numpy as np
energy=df["Energy_Used_kWh"].tonumpy()
print("Menu:",np.mean(energy))
print("Maximum:",np.max(energy))
print("Minimum:",np.min(energy))

import matplotlib.pyplot as plt
avg_energy=df.groupby("Vehicle_Type")["Enery.Used_kWh"].mean()
avg_energy.plot(kind="bar")
plt.xlabel("Vehicle Type")
plt.ylabel("Average Energy Used(kWh)")
plt.title("Average Energy Usage by Vehicle Type")
plt.tight_layout()
plt.show()

import json
with open("equipment.events.json","r") as file:
    data=json.load(file)
for event in data:
    print("Event ID:",event["event_id"])
    print("Asset Type:",event["asset"]["type"])
    print("Site:",event["asset"]["site"])
    print("Severity:",event["severity"])
    print("--------------")

import json
with open("equipment.events.json","r") as file:
    data=json.load(file)
for event in data:
    if event["temperature"]>70:
        print("Event_ID:",event["event_id"])
        print("Temperature:",event["temperature"])
        print("Actions:",event.get("actions","No actions recorded"))
        print("--------------")

with open("coastal_monitoring_log.txt","r") as file:
    text=file.read()
words=text.split()
print("Total Words:",len(words))
print("Occurrences of inspection:",text.lower().count("inspection"))

with open("coastal_monitoring_log.txt","r") as file:
    for line in file:
        if any(word in line.lower()
            for word in ["boardwalk","maintenance","wind"]):
            print(line.strip())







