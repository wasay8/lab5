import requests
from bs4 import BeautifulSoup
import collections
import duckdb
import pandas as pd

def get_other_information(api,well_name):
	# Preprocessing of well_name and api
	
	well_name = str(well_name)
	well_name = well_name.replace(" ","+")
	
	# URL_setting by entering searching query
	url = f"https://www.drillingedge.com/search?type=wells&operator_name=&well_name={well_name}&api_no={api}&lease_key=&state=&county=&section=&township=&range=&min_boe=&max_boe=&permit_start=&permit_end=&min_depth=&max_depth=&field_formation="


	# Headers to mimic a browser visit
	headers = {'User-Agent': 'Mozilla/5.0'}

	# Returns a requests.models.Response object
	page = requests.get(url, headers=headers)

	soup = BeautifulSoup(page.text, 'html.parser')

	# Return a target table
	res_table = soup.find("table", class_="table wide-table interest_table")

	# Finding columns
	columns_raw = res_table.find_all("th",class_="search_table_column")
	columns=[]
	for column in columns_raw:
		columns.append(column.text.strip())

	# Finding contents
	contents_raw = res_table.find_all("td")
	contents=[]
	aurl = ""	
	
	
	
	
	for (i,content) in enumerate(contents_raw):
		contents.append(content.text.strip())
		if i==1:
			aurl=content.find("a",href=True)["href"]	
	if aurl == "":
		return {'API #': '', 'Well Name': '', 'Lease Name': '', 'Location': '', 'Operator': '', 'Status': '',
		"Producetion_information":"","Well_Type":"","Closest_City":""}
	
	well_page = requests.get(aurl)
	
	soup = BeautifulSoup(well_page.text, 'html.parser')
	dropcap = soup.find_all("p",class_="block_stat")
	Producetion_information = ""
	for para in dropcap:
		Producetion_information += para.text
		Producetion_information += '\n'
	
	
	# Well_Type and Closest_City
	# print(soup.find("div",class_="table_wrapper"))
	table = soup.find("table",class_="skinny")
	if table is None:
		table = soup.find("table",class_="wide-table")
	table_tr = table.find_all("tr")
	Well_Type = table_tr[2].find_all("td")[1].text
	Closest_City = table_tr[4].find_all("td")[1].text
	
	
	
	
	
	
	
	
	
	# Combine them togther into a dict
	n = min(len(contents),len(columns))
	res = {columns[i]:contents[i] for i in range(n)}
	res["Producetion_information"] = Producetion_information
	res["Well_Type"] = Well_Type
	res["Closest_City"] = Closest_City
	return res


if __name__ == "__main__":
	# print(get_other_information("33-105-90258","Atlanta #1 SWD"))
	# print(get_other_information("33-053-06057","Kline Federal 5300 31-18 6B"))
	
	db_name = "test.db" # Please input db_name you want
	con = duckdb.connect(db_name)
	table_name = "basic_informaion" # Please input table name
	input_data = pd.read_csv("test.csv")
	con.sql(f"Drop table if exists {table_name}")
	con.sql(f"CREATE TABLE {table_name} AS SELECT * FROM input_data")
	init_data = con.sql(f"SELECT * FROM {table_name}").df()
	print(init_data.head(5))
	res = collections.defaultdict(list)
	for index,row in init_data.iterrows():
		api_name = row['well_api'].replace(" ","")
		company_name = row['well_name']
		print(api_name,company_name)
		tres = get_other_information(api_name,company_name)
		tres['API #'] = api_name
		tres['Well Name'] = company_name
		for tres_key in tres.keys():
			res[tres_key].append(tres[tres_key])
		print(tres)
	
	
	
	
	
	
	# To dataframe
	res_df = pd.DataFrame()
	res_df["API #"]=res["API #"]
	res_df['Well Name']=res['Well Name']
	res_df['Lease Name']=res['Lease Name']
	res_df['Location']=res['Location']
	res_df['Operator']=res['Operator']
	res_df['Status']=res['Status']
	res_df["Producetion_information"] = res["Producetion_information"]
	res_df["Well_Type"] = res["Well_Type"]
	res_df["Closest_City"] = res["Closest_City"]
	
	# To csv
	res_df.to_csv("res_2b.csv",index=False)
	
	
