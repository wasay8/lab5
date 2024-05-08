# Import the requests module
import pandas as pd
from icecream import ic

OUTPUT_FILENAME = "lab5_pt2/output.csv"
LIST_OF_COLS = ["API #","Well Name","Operator Name","County","State",  "Latitude", "Longitude"]

def get_lat_long(api_no):

    URL = f"https://www.shalexp.com/search/wells?a1=on&f1=api_no&c1=contains&v1={api_no}&dc=wells.0-1-3-4-5-12-13"

    shalexp_list = pd.read_html(URL)
    return shalexp_list[0][LIST_OF_COLS]


drilling_df = pd.read_csv("lab5_pt1/res_2b.csv", usecols=["API #"])

lat_long_s = drilling_df["API #"].apply(get_lat_long)

# test_s = drilling_df["API #"][:2].apply(get_lat_long)

final_df = pd.concat(lat_long_s.to_list(), ignore_index=True)
ic(final_df)
final_df.to_csv(OUTPUT_FILENAME, index=False)


# print(drilling_df["API #"][:2].apply(get_lat_long))
