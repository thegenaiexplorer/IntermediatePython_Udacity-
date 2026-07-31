"""Write a stream of close approaches to CSV or to JSON.

This module exports two functions: `write_to_csv` and `write_to_json`, each of
which accept an `results` stream of close approaches and a path to which to
write the data.

These functions are invoked by the main module with the output of the `limit`
function and the filename supplied by the user at the command line. The file's
extension determines which of these functions is used.

You'll edit this file in Part 4.
"""
import csv
import json
import helpers
import os


def write_to_csv(results, filename):
    """Write an iterable of `CloseApproach` objects to a CSV file.

    The precise output specification is in `README.md`.Roughly, each output row
    corresponds to the information ina single close approach from the `results`
    stream and its associated near-Earth object.

    :param results: An iterable of `CloseApproach` objects.
    :param filename: A Path-like object pointing to where the data
    should be saved.
    """
    fieldnames = (
        'datetime_utc', 'distance_au', 'velocity_km_s',
        'designation', 'name', 'diameter_km', 'potentially_hazardous'
    )
    list_fieldnames = list(fieldnames)
    list_approaches = [list_fieldnames]
    for approach in results:
        datetime_utc = helpers.datetime_to_str(approach.time)
        distance_au = approach.distance
        velocity_km_s = approach.velocity
        designation = approach.neo.designation
        if (approach.neo.name is None):
            name = ""
        else:
            name = approach.neo.name
        diameter_km = approach.neo.diameter
        potentially_hazardous = approach.neo.hazardous
        temp_record = [datetime_utc, distance_au, velocity_km_s,
                      designation, name, diameter_km, potentially_hazardous]
        list_approaches.append(temp_record)

    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f, lineterminator=os.linesep)
        for record in list_approaches:
            writer.writerow(record)


def write_to_json(results, filename):
    """Write an iterable of `CloseApproach` objects to a JSON file.

    The precise output specification is in `README.md`.Roughly, the output is a
    list containing dictionaries, each mapping `CloseApproach` attributes to
    their values and the 'neo' key mapping to a dictionary of the associated
    NEO's attributes.

    :param results: An iterable of `CloseApproach` objects.
    :param filename: A Path-like object pointing to where the data
    should be saved.
    """
    list_master = []
    for approach in results:
        datetime_utc = helpers.datetime_to_str(approach.time)
        distance_au = float(approach.distance)
        velocity_km_s = float(approach.velocity)
        designation = str(approach.neo.designation)
        if (approach.neo.name is None):
            name = ""
        else:
            name = str(approach.neo.name)
        diameter_km = float(approach.neo.diameter)
        potentially_hazardous = approach.neo.hazardous
        temp_dict = {
                      "datetime_utc": datetime_utc,
                      "distance_au": distance_au,
                      "velocity_km_s": velocity_km_s,
                      "neo": {
                          "designation": designation,
                          "name": name,
                          "diameter_km": diameter_km,
                          "potentially_hazardous": potentially_hazardous
                          }
                      }
        list_master.append(temp_dict)

    with open(filename, 'w') as f:
        json.dump(list_master, f, indent=2)
