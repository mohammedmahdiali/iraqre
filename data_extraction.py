import requests
import time
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver

CONST_MAIN = "https://iraqre.com"
CONST_PAGES = ["https://iraqre.com/en/sell", "https://iraqre.com/en/rent"]
CONST_NEXT_PAGE = "?page="

CONST_SUB_PAGES = []

def get_links(n_pages):

	driver = webdriver.Chrome('chromedriver.exe')
	for page in CONST_PAGES:
		for sub_page in range(1, page_num):

			driver.get(page+CONST_NEXT_PAGE+str(sub_page))
			time.sleep(30)

			last_height = driver.execute_script("return document.body.scrollHeight")
			driver.execute_script(f"window.scrollTo(0, {last_height / 2});")
			time.sleep(20)

			source = driver.page_source
			if f"sell{CONST_NEXT_PAGE}{sub_page}" or f"rent{CONST_NEXT_PAGE}{sub_page}" in source:
				soup = BeautifulSoup(source, 'html.parser')
				divs = soup.find_all("div", {"class":"listbox-cont-2"})
				for div in divs:
					a = div.find("a").get('href')
					CONST_SUB_PAGES.append(CONST_MAIN+str(a))
			else:break

    with open("iraqre.csv", "a+") as f:
        for i in CONST_SUB_PAGES:
            f.write(f"{i},")

def get_data_from_links(file_path):

	final_data = []

	with open(file_path, "r") as file:
		file = file.read().split(",")
		for link in file:
			if "https://" in link:
				data_dic = {}
				response = requests.get(link)
				source = response.content
				soup = BeautifulSoup(source, 'html.parser')

				title = soup.find("h2", {"class":"h2-desshow"})
				data_dic["title"] = title.text
				divs = soup.find_all("li", {"class":"over-child"})

				for div in divs:
					spans = div.find_all("span")
					data_dic[spans[0].text] = spans[1].text

				final_data.append(data_dic)
			else:continue

	df = pd.DataFrame(final_data)
	df.to_excel("data.xlsx")