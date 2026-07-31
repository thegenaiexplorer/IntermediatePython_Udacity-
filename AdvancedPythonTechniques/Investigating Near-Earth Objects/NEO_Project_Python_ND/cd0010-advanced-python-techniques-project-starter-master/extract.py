"""Extract data on near-Earth objects and close approaches from files.

Files used are CSV and JSON files.

The `load_neos` function extracts NEO data from a CSV file, formatted as
described in the project instructions, into a collection of `NearEarthObject`s.

The `load_approaches` function extracts close approach data from a JSON file,
formatted as described in the project instructions, into a collection of
`CloseApproach` objects.

The main module calls these functions with the arguments provided at the
command line, and uses the resulting collections to build an `NEODatabase`.

You'll edit this file in Task 2.
"""
import csv
import json

from models import NearEarthObject, CloseApproach


def load_neos(neo_csv_path):
    """Read near-Earth object information from a CSV file.

    :param neo_csv_path: A path to a CSV file containing data
    about near-Earth objects.
    :return: A collection of `NearEarthObject`s.
    """
    neos_list = []
    with open(neo_csv_path, 'r') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            designation = row[3]
            name = row[4]
            diameter = row[15]
            pha = row[7]
            if (pha == "Y"):
                hazardous = True
            else:
                hazardous = False
            neo_obj = NearEarthObject(designation, name, diameter, hazardous)
            neos_list.append(neo_obj)
    return neos_list


def load_approaches(cad_json_path):
    """Read close approach data from a JSON file.

    :param cad_json_path: A path to a JSON file containing data
    about close approaches.
    :return: A collection of `CloseApproach`es.
    """
    ca_list = []
    with open(cad_json_path, 'r') as f:
        contents = json.load(f)

    for data in contents['data']:
        designation = data[0]
        time = data[3]
        distance = data[4]
        velocity = data[7]
        ca_obj = CloseApproach(designation, time, distance, velocity)
        ca_list.append(ca_obj)

    print(f'Number of datapoints loaded are {len(ca_list)}')
    return ca_list
