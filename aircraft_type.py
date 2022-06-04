import pandas as pd
from icao_nnumber_converter_us import n_to_icao, icao_to_n

df = pd.read_csv(r"C:\Users\Admin\Documents\UFO\Opensky\ReleasableAircraft2021\MASTER.txt")

n_number = icao_to_n("abfc71")

n_number = n_number[1:]

search_result_row = df[df["N-NUMBER"].str.contains(n_number)]
search_result = search_result_row.iloc[0]["TYPE AIRCRAFT"]

def aircraft_type_search(icao):
    df = pd.read_csv(r"C:\Users\Admin\Documents\UFO\Opensky\ReleasableAircraft2021\MASTER.txt")
    n_number = icao_to_n(icao)

    n_number = n_number[1:]

    search_result_row = df[df["N-NUMBER"].str.contains(n_number)]
    type_aircraft = search_result_row.iloc[0]["TYPE AIRCRAFT"]

    return type_aircraft
