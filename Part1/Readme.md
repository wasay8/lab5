# PDF EXTRACTION

>package requirment: pandas 2.0.3 pyMupdf 1.23.4

Please be sure to be inside lab5_pt1 folder before running the script.

# PDF EXTRACTION for 2A

please run the script by the following command:

```
python pdf_extract.py
```

that should produce a file called well_and_features.csv in the same folder.

# PDF EXTRACTION for 2B

For api and well_name: Currently it's come from pdf_extract.py, the output of the script is test.csv.
Please set the pdf_folder correctly, you will see some information like the screenshot below.

![image](https://github.com/thoughtfuldata/DSCI560-project/assets/55038803/ac965299-f3f9-4a3d-b9ef-bc314cb49aed)

It can work just directly run it.

# WEB SCRAPING

>package requirement: pandas 2.0.3 pyMupdf 1.23.4 duckdb 0.8.1 beautifulsoup4 4.12.2

The script would catch other information on website by api and well_name. And the output is res_2b.csv
The screenshot would show the content in each row

![image](https://github.com/thoughtfuldata/DSCI560-project/assets/55038803/f4f18ea3-aea8-4e27-93f4-f3b9efed197b)


The rationale of the script is keep querying database online by url.

The final result in csv file are showed below.

![image](https://github.com/thoughtfuldata/DSCI560-project/assets/55038803/e58f301b-516a-426a-be1d-81739bc85072)


It can work just directly run it.

# DATA PREPROCESSING
execute data_preprocessing_5.py to implement the functions below.


### Libraries:  

Pandas : 1.5.3  

Numpy : 1.23.5  

Duckdb : 0.8.1  


### 1. Modifying API # 
Converting API number in its form for understanding, some values have 00-000 in it which signify that its missing values as extraction got null values.
Preprocessed API number to get state and county codes for comparision

### 2. Location
Divinding the location into county and state for better analysis.

### 3. Merging Dataset to finalize one
Merging 3 datasets using Well File Numbers and API numbers. 
Extracted Well file Number from text. 

### 4. Cleaning and Type casting 
Cleaning and removing irrelevant data from the features.


<img width="785" alt="Screenshot 2023-10-07 at 7 13 43 PM" src="https://github.com/thoughtfuldata/DSCI560-project/assets/48021329/f0a470d4-7d6b-4d37-adc1-de9ed3c9d8e1">


### 5. Storing into the Database

<img width="1443" alt="Screenshot 2023-10-07 at 7 39 39 PM" src="https://github.com/thoughtfuldata/DSCI560-project/assets/48021329/25cce5b7-ecde-48eb-9db4-419e06a1fbe1">

