import os
import math
import csv
import json
from collections import defaultdict
from datetime import date


def int_of_float(string):
    f = float(string)
    i = int(f)
    return i if i == f else f


def find_fields_in_json(json_data, target_fields, code):
    results = defaultdict(list)
    results["ehrKood"].append(code)
    
    def search_recursive(data):
        if isinstance(data, dict):
            for field in target_fields:
                if field in data:
                    if data[field] is None:
                        if field == "esmaneKasutus":
                            results[field].append(float(date.today().year))
                    else:
                        results[field].append(int_of_float(data[field]))
                    
            for value in data.values():
                search_recursive(value)
                
        elif isinstance(data, list):
            for item in data:
                search_recursive(item)
    
    search_recursive(json_data)
    return dict(results)


def extract_wanted_data_from_files(fields):
    data = []
    
    for filename in os.listdir("data"):
        with open(f"data/{filename}", "r") as f:
            json_data = json.load(f)
            
            file_data = find_fields_in_json(json_data, fields, int(filename.replace(".ehr.json", "")))
            for field in fields:
                if field not in file_data:
                    file_data[field] = 0
                else:
                    file_data[field] = max(file_data[field])
            file_data["ehrKood"] = file_data["ehrKood"][0]
            
            data.append(file_data)
    
    return data


def write_data_to_csv(data, filename, fields=[]):
    with open(filename, "w", newline='') as f:
        if isinstance(data[0], dict):
            writer = csv.DictWriter(f, fieldnames=fields)
            writer.writeheader()
        else:
            writer = csv.writer(f)
        writer.writerows(data)


def normalize_values(fields, data):
    for field in fields:
        values = []
        for file_data in data:
            values.append(file_data[field])
        
        max_value = max(values)
        min_value = min(values)

        new_values= []
        for item in values:
            normalized = (item - min_value) / (max_value - min_value)
            new_values.append(normalized)
        
        for index, value in enumerate(new_values):
            data[index][field] = value


def build_similarity_matrix(fields, data):
    matrix = []
    
    headers = ["x"]
    for file_data in data:
        headers.append(file_data["ehrKood"])
    matrix.append(headers)
    
    for file_data1 in data:
        row = [file_data1["ehrKood"]]
        for file_data2 in data:
            dif = 0
            for field in fields:
                dif += (file_data1[field] - file_data2[field]) ** 2
            d = math.sqrt(dif)
            row.append(d)
        matrix.append(row)
    
    return matrix


if __name__ == "__main__":
    fields = [
        "mahtBruto",
        "maxKorrusteArv",
        "ehitisalunePind",
        "yldkasut_pind",
        "esmaneKasutus",
        "lift",
        "tubadeArv"
    ]
    
    data = extract_wanted_data_from_files(fields)
    
    dataset_fields = fields.copy()
    dataset_fields.insert(0, "ehrKood")
    write_data_to_csv(data, "dataset.csv", fields=dataset_fields)
    
    normalize_values(fields, data)
   
    similarity_matrix = build_similarity_matrix(fields, data)
    #write_data_to_csv(similarity_matrix, "similarity_matrix.csv")