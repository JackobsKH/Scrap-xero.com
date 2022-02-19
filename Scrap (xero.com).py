import requests
import json
from bs4 import BeautifulSoup
import re


def parse(url):

	# Заголовки - чтобы сайты не думали, что ходит бот
	headers = {
		"Accept": "*/*",
		"User-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36"
	}
	# Получение текста с указанного URL
	req = requests.get(url, headers=headers)
	src = req.text
	# print(src)


	# # Запись первой страницы на диск
	# with open ("index.html", "w", encoding="utf-8") as file:
	# 	file.write(src)

	# # Чтение файла с диска. Работаем уже не онлайн
	# with open ("index.html", encoding="utf-8") as file:
	# 	src = file.read()


	# Создаем объект BeautifulSoup, где ищем все ссылки класса mzr-tc-group-item-href
	soup = BeautifulSoup(src, "lxml")
	all_advisor_names = soup.find_all("div", class_ = "advisors-result-card")

	advisor_urls=[]


	for adv_card in all_advisor_names:
		advisor_url = adv_card.find("a").get("href")
		advisor_urls.append(advisor_url)


	# for adv_url in advisor_urls:
	# 	req = requests.get(adv_url, headers)
	# 	a = str(adv_url).split("/") 
	# 	advisor_name = str(a[-2])[:-13]

	# 	with open(f"data/{advisor_name}.html", "w", encoding="utf-8") as file:
	# 		file.write(req.text)

	advisors_full_data = []
	for adv_url in advisor_urls:
		# a = str(adv_url).split("/") 
		# adv_name = str(a[-2])[:-13]	
		
		req = requests.get(adv_url, headers)
		# with open(f"data/{adv_name}.html") as file:
		src = req.text

		soup = BeautifulSoup(src, "lxml")
		adv_data = soup.find("div", class_="advisors-profile")


		try:
			adv_logo = adv_data.find(class_="actual-logo").get("src")
		except Exception:
			adv_logo = "No Logo"

		try:
			adv_name = adv_data.find(class_="advisors-profile-hero-detailed-info-title title-2").text
		except Exception:
			adv_name = "Advisor has No Name"

		try:
			adv_ind = adv_data.find(class_="advisors-profile-hero-detailed-info-sub national").text
			adv_ind_list=adv_ind.split("·")
			adv_industry = adv_ind_list[0].strip().lstrip()
			
		except Exception:
			adv_industry = "None"
			
		try:	
			adv_www = adv_data.find(class_="advisors-profile-hero-detailed-contact-website").get("href")
		except Exception:
			adv_www = "No Website"

		try:
			adv_tel = adv_data.find(class_="advisors-profile-hero-detailed-contact-phone").get("data-phone").strip("'\n")
		except Exception:
			adv_tel = "No Phone number"

		try:
			adv_address = adv_data.find(class_="advisors-profile-locations-list-item-address").text
		except Exception:
			adv_address = "No Address"

		try:
			adv_about = adv_data.find(class_="advisor-profile-practice-desc").text.strip("'\n")
		except Exception:
			adv_about = "No Description"

		try:
			adv_contact_name = adv_data.find(class_="advisors-profile-team-name").text.strip("'\n")
			adv_contact_name = adv_contact_name.strip(" ")
		except Exception:
			adv_contact_name="No name"

		try:

			adv_status_list = [i.find('h6', class_=re.compile('^Tag__TagHeading')).text
				for i in list(filter(
					lambda j: j.find('p', class_=re.compile('^CardHeader__CardPreTitle')).text == 'Partner status',
					adv_data.find_all("div", class_=re.compile('^Tag__TagWrapper'))
					))]

			adv_status=adv_status_list[0].strip(" ")
		except Exception:
			adv_status = "No data"



			
		adv_country = "Australia"




		advisors_full_data.append(
			{
				"Advisor Name": adv_name,
				"Logo url": adv_logo,
				"Website": adv_www,
				"Contact Person": adv_contact_name.strip("'\n"),
				"Partnership Status": adv_status,
				"Phone": adv_tel,
				"Industry": adv_industry,
				"Address": adv_address,
				"Country": adv_country,
				"Description": adv_about
			}

		)

	with open("data/advisors_full_data.json", "a", encoding="utf-8") as file:
		json.dump(advisors_full_data, file, indent=4, ensure_ascii = False)





def main():
	url = 'https://www.xero.com/au/advisors/find-advisors/australia/?type=advisors&orderBy=ADVISOR_RELEVANCE&sort=ASC&pageNumber=1'

	url = url[:-1]

	for i in range (1,5):
		url+=str(i)
		print(url)
		parse(url)
		url = url[:-1]
		# print(url)
		print(f"Passed page number: {i}")

	print("Well Done!")


if __name__=="__main__":
	main()