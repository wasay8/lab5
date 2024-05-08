from PIL import Image
import re
import fitz
import pytesseract
import os
import collections
import pandas as pd
"""
notice install tesseract-ocr by run "apt get tesseract-ocr"
"""


folder_name = 'DSCI560_Lab5_pdfs'
thesum,iii = 0,0
n = len(os.listdir(folder_name))
res_dict = collections.defaultdict(list)
for tpath in os.listdir(folder_name):
	pdf_path = os.path.join(folder_name,tpath)  
	pdfDoc = fitz.open(pdf_path)
	count = 0
	
	# The process to filename and get api
	api_relist = ["\d{2}\s*-\s*\d{3}\s*-\s*\d{5}",
		"\d{3}-\d{5}",
		"\d{2}-\d{5}",
		"\d{10}",
		"\d{7}"]
	for re_ in api_relist:
		for (i,page) in enumerate(pdfDoc):	
			#OCR method(temp useless)
			"""
			#mat = fitz.Matrix(3,3)
			#rect = page.rect
			#clip = fitz.Rect(rect.width*0.75,0.05*rect.height,
					#rect.width*0.9,0.08*rect.height)
			#pix = page.get_pixmap(matrix=mat,alpha=False,clip=clip)
			#page8img = Image.frombytes("RGB",[pix.width,pix.height],pix.samples)


			clip = fitz.Rect(rect.width*0.813,0.098*rect.height,
						rect.width*0.95,0.111*rect.height)
			pix = page.get_pixmap(matrix=mat,alpha=False,clip=clip)
			apiimg = Image.frombytes("RGB",[pix.width,pix.height],pix.samples)

			clip = fitz.Rect(rect.width*0.044,0.198*rect.height,
						rect.width*0.28,0.2138*rect.height)
			pix = page.get_pixmap(matrix=mat,alpha=False,clip=clip)
			wellnameimg = Image.frombytes("RGB",[pix.width,pix.height],pix.samples)
			
			#page8 = pytesseract.image_to_string(page8img,lang='eng')
			
			# api = pytesseract.image_to_string(apiimg,lang='eng', config='--psm 7 --oem 3 -c tessedit_char_whitelist=0123456789')
			# wellname = pytesseract.image_to_string(wellnameimg,lang='eng')
			"""
			
			page_text = page.get_text("word")
			if re.search(re_,page_text):
				count=1
				print(re.search(re_,page_text).group(),i,tpath)
				res_dict["API #"].append(re.search(re_,page_text).group())
				res_dict["Filename"].append(tpath)
				break
		if count==1:
			break	
		# print(page8)
	iii+=1
	print(f"{iii}/{n}",tpath)
	thesum+=count
print(len(os.listdir(folder_name)),thesum)
df = pd.DataFrame()
df['well_api'] = res_dict["API #"]
df['Filename'] = res_dict['Filename']



thesum,iii = 0,0
for tpath in os.listdir(folder_name):
	pdf_path = os.path.join(folder_name,tpath)  
	pdfDoc = fitz.open(pdf_path)
	count = 0
	for (i,page) in enumerate(pdfDoc):
		page_text = page.get_text("word").split("\n")
		for (j,text) in enumerate(page_text):
			if text.strip() == "Well Name and Number" or text.strip() == "Well or Facility Name":
				p_text = page_text[j+1]
				if not re.search("24-HOUR PRODUCTION",p_text) and p_text[0]!="0" and p_text.strip()!='D':
					count=1
					print(page_text[j+1],i,tpath)
					res_dict["Well_name"].append(page_text[j+1])
					break
				
			
		if count==1:
			break
	if count == 0:
		res_dict["Well_name"].append("")
	iii+=1			
	print(f"{iii}/{n}",tpath)
	thesum+=count
print(len(os.listdir(folder_name)),thesum)
df['well_name'] = res_dict["Well_name"]
df.to_csv("test.csv",index = False)

