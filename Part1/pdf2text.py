import re
from pathlib import Path

import pandas as pd
import pdfplumber
import pytesseract
from icecream import ic
from pdf2image import convert_from_path

# well_info = {
#     "well name and number":"well_names",
#     "county":"well_county",
#     "state": "state_info",
#     "api #":"well_api",
#     "operator":"operator_of_well",
#     "well operator":"operator_of_well"
# }

well_features = {
    "Stimulated(?! Formation)" : "stimulation_date",
    "Stimulated Formation" : "stimulated_formation",
    "Top \(Ft\)" : "top_ft",
    "Bottom \(Ft\)": "bottom_ft",
    "Stimulation Stages": "stimulation_stages",
    "Volume(?! Units)":"volume",
    "Volume Units": "volume_units",
    "Type Treatment":"type_treatment",
    "Acid%":"acid",
    "Lbs Proppant":"lbs_prop",
    "Maximum Treatment Pressure \(PSI\)": "max_psi",
    "Maximum Treatment Rate \(BBLS/Min\)": "bbls_min"
}

well_example_dict = {
    "stimulation_date": None,
    "stimulated_formation": None,
    "top_ft": None,
    "bottom_ft": None,
    "stimulation_stages": None,
    "volume": None,
    "volume_units": None,
    "type_treatment": None,
    "acid": None,
    "lbs_prop": None,
    "max_psi": None,
    "bbls_min": None
}


dict_ls = []
for file in Path("DSCI560_Lab5_pdfs").glob("*.pdf"):
    ic(file.name)

    iter_dict = well_example_dict.copy()
    iter_dict["file_num"] = re.findall(r'\d+', file.name)[0]

    with pdfplumber.open(file, laparams={}) as pdf:
        for i, page in enumerate(pdf.pages, start=1):
            ocr_page = False

            if not page.extract_text():
                page = convert_from_path(file,  dpi=400, single_file=True, first_page=i, last_page=i)
                page = page[0]
                ocr_page = pytesseract.image_to_pdf_or_hocr(page, extension='pdf')
                with open('ocr_page.pdf', 'w+b') as f:
                    f.write(ocr_page)

                page = pdfplumber.open("ocr_page.pdf", laparams={}).pages[0]
                ocr_page = True

            if page.search("Stimulated Formation Top"):
                for key, value in well_features.items():
                    x0_adj = 0
                    x1_adj = 0
                    bottom_adj = 11
                    if res := page.search(key):
                        if ocr_page:
                            if key == "Stimulated(?! Formation)":
                                x0_adj = 90
                            elif key == "Volume(?! Units)":
                                x1_adj = 160
                            bottom_adj = 70
                        elif key == "Stimulated(?! Formation)":
                            x0_adj = 20
                        elif key == "Volume(?! Units)":
                            x1_adj = 30

                        # ic(ocr_page,x0_adj, x1_adj, bottom_adj)
                        res[0]["x0"] = res[0]["x0"] - x0_adj
                        res[0]["x1"] = res[0]["x1"] + x1_adj
                        res[0]["bottom"] = res[0]["bottom"] + bottom_adj

                        if len(text_ls := page.crop((res[0]["x0"], res[0]["top"], res[0]["x1"], res[0]["bottom"]))
                               .extract_text().splitlines()) > 1:
                            iter_dict[value] = text_ls[1].strip()

                dict_ls.append(iter_dict)
                # ic(iter_dict)
                break

well_features_df = pd.DataFrame(dict_ls)
well_features_df.to_csv("well_features.csv", index=False)

















# for i, block in enumerate(blocks):
#     print("%r"%block[4])
#     print(block[4].lower())
#     if block[4].rstrip().lower() in  "well name and number \nbasic game & fish 34-3 \n":
#         print("value:", blocks[i+1][4].strip())




# pdf_file = fitz.open("DSCI560_Lab5_pdfs/W22099.pdf")
# page = pdf_file[4]
# well_example_dict["well_no"] = "22099"

# blocks = page.get_text("blocks", sort=True, flags=fitz.TEXT_INHIBIT_SPACES)

# print(blocks)
# lines = [] # an empty list to store lines
# for block in blocks: # iterate over blocks
#     text = block[4] # get the text of the block
#     lines.extend(text.strip().lower().split("\n")) # split by new-line character and add to lines list

# print(lines)
# for i,line in enumerate(lines): # print all lines on page
#     line = line.strip()
#     # print(line)
#     # print([val for key, val in well_features.items() if key in line])
#     if line in well_info and well_example_dict.get(well_info[line]) is None:
#         well_example_dict[well_info[line]] = lines[i+1]
#     elif line in well_features and well_example_dict.get(well_features[line]) is None:
#         if line == "type treatment":
#             well_example_dict[well_features[line]] = lines[i+5]
#         else:
#             well_example_dict[well_features[line]] = lines[i+8]
#     # elif len([val for key, val in well_features.items() if key+ " :" in line])>=1:
#     #     # print(line)
#     #     line_spl = line.split(":")
#     #     well_example_dict[well_features[line_spl[0].strip()]] = line_spl[1].strip()
#     # elif "#"+well_example_dict["well_no"] in line:
#     #     print(line)
#     #     line_split = line.split(" ")
#     #     for i, word in enumerate(line_split):
#     #         if word == "api":
#     #             well_example_dict["well_api"] = line_split[i+1]


#     if None not in well_example_dict.values():
#             break


# # # # if isinstance(well_example_dict["well_api"], str):
# # # #     well_example_dict["well_api"] = well_example_dict["well_api"].replace(" ","").replace("-","")
# # # # if len(well_example_dict["well_api"]) > 10:
# # # #     well_example_dict["well_api"] = well_example_dict["well_api"].replace("0", "", 1)

# print(well_example_dict)