import os
import math
import json
import csv


def normalize_values(data: dict):
    values = data.values()
    max_value = max(values)
    min_value = min(values)
    
    for key, value  in data.items():
        normalized = (value - min_value) / (max_value - min_value)
        data[key] = normalized


def build_similarity_matrix(data: dict):
    matrix = []
    
    headers = ["x"]
    for ehr_code in data:
        headers.append(ehr_code)
    matrix.append(headers)
    
    for key1, value1 in data.items():
        row = [key1]
        for key2, value2 in data.items():
            d = math.sqrt((value1 - value2) ** 2)
            row.append(d)
        matrix.append(row)
    
    return matrix


if __name__ == "__main__":
    pathname = "../EX3/data"
    circumferences = {}
    for filename in os.listdir(pathname):
        ehr_code = int(filename.replace(".ehr.json", ""))
        with open(f"{pathname}/{filename}", "r") as f:
            data = json.load(f)
            
        coordinates = data[0]["ehitis"]["ehitiseKujud"]["ruumikuju"][0]["geometry"]["coordinates"][0]
        
        circumference = 0
        for index, coord in enumerate(coordinates):
            first_coord = coord
            second_coord = coordinates[index + 1] if index + 1 != len(coordinates) else coordinates[0]
            distance = math.sqrt((second_coord[0] - first_coord[0]) ** 2 + (second_coord[1] - first_coord[1]) ** 2)
            circumference += distance
     
        circumferences[ehr_code] = circumference
    
    normalize_values(circumferences)
    similarity_matrix = build_similarity_matrix(circumferences)
    
    with open("similarity_matrix.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(similarity_matrix)
