import csv
import re
import math

def read_csv(filename: str):
    lines = []
    with open(filename, mode ='r') as file:
        csvFile = csv.reader(file)
        for line in csvFile:
            lines.append(line)
    return list(zip(*lines))[1:]

def normailze_data(data: list):
    max_value = max(data)
    min_value = min(data)

    new_data = []
    for item in data:
        normalized = (item - min_value) / (max_value - min_value)
        new_data.append(normalized)
    return new_data


if __name__ == '__main__':
    data = read_csv("MARKETING_SEGMENTATION_SIMPLE.CSV")
    normalized_data = {}

    for group in data:
        numbers = []
        for item in group[1:]:
            parsed_item = re.sub(r"[^\d\.]+", "", item)
            numbers.append(float(parsed_item))

        normalized_data[group[0]] = normailze_data(numbers)

    matrix = []

    for i in range(4):
        row = []
        for j in range(4):
            dif = 0
            for key in normalized_data.keys():
                dif += (normalized_data[key][i] - normalized_data[key][j]) ** 2
            d = math.sqrt(dif)
            row.append(round(d, 2))
        matrix.append(row)

    for row in matrix:
        print(row)

