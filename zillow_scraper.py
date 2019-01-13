from bs4 import BeautifulSoup
from requests import get
import time, random 
import re
import pandas as pd
import itertools
import matplotlib.pyplot as plt
import seaborn as sns
#scrape house information from main page
n_page=1
sum_house=0
house_ids = []
total = 1000
i = 0

#scrape information from specific house page
prices = []
beds = []
baths = []
sqfts = []
ele_schs = []
mid_schs = []
high_schs = []

headers = ({'User-Agent':
                    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3607.0 Safari/537.36'})

def get_house_summary(html_soup):
    summary = html_soup.find('div', class_="home-details-summary-and-price")
    summary = summary.find_all('span')
    l = len(summary)
    house_infos = []

    for i in range(l):
         info = summary[i].text
         house_infos.append(info)
    return house_infos

def get_detail(house_infos, param):
    res = ""
    for i in house_infos:
        if param in i:
            res = i
            break
    return res

def get_school_rates(html_soup):
    schools = html_soup.find('div', class_="hdp-nearby-schools")
    sch_summary = schools.find_all('span')
    l = len(sch_summary)
    sch_rates = []

    for i in range(l-1):
        info = sch_summary[i].text
        if info.isdigit():
            sch_rates.append(info)
    return sch_rates

def get_elementary_sch(sch_rates):   
    return sch_rates[0]

def get_middle_sch(sch_rates):
    return sch_rates[1]

def get_high_sch(sch_rates):
    return sch_rates[2]

def get_house_soup(url, headers):
    response = get(url, headers = headers)
    html_soup = BeautifulSoup(response.text, 'html.parser')
    return html_soup

def get_house_containers(html_soup):
    house_containers = html_soup.find_all('div', class_="zsg-photo-card-content zsg-aspect-ratio-content")
    return house_containers

def get_num_houses_per_page(house_containers):
    num_house_page = len(house_containers)
    print("page has " + str(num_house_page) + " house(s)")
    return num_house_page

def get_total_houses(html_soup):
    facts = html_soup.find('div', class_='zsg-separator')
    pattern = 'for Sale:[0-9]+'
    line = re.search(pattern, facts.text).group()
    ind = line.index(':')
    total = int(line[ind+1:])
    return total

def get_individial_house(house_containers):
    for i in range(len(house_containers)):        
        for instance in house_containers[i].find_all('a'):
            house_id = instance.get('href')
            if not house_id.startswith('/myzillow') and "AuthRequired.htm" not in house_id:
                house_id = 'https://www.zillow.com' + house_id
                house_ids.append(house_id)
                house_info_file.write(house_id) 
                house_info_file.write("\n")   

house_info_file = open("house_info.txt", "w")
indidual_house_info = open("individual_houses.txt", "w")

while sum_house < total:
    url = "https://www.zillow.com/homes/for_sale/27560_rb/" + str(n_page+i) + "_p"
    soup = get_house_soup(url, headers)
    house_containers = get_house_containers(soup)
    sum_house = sum_house + get_num_houses_per_page(house_containers)
    total = get_total_houses(soup)
    #print(total)
    get_individial_house(house_containers)
    i = i + 1
    time.sleep(2)
print("=> total number of houses scraped is " + str(sum_house))
house_info_file.close()
i = 0

for house_id in house_ids:
    i = i + 1
    print("house number " + str(i))
    soup = get_house_soup(house_id, headers)
    time.sleep(5)
    print(house_id)

    #get summary of house_info
    house_infos = get_house_summary(soup)

    price = get_detail(house_infos, "$")
    if(price != ""):
        prices.append(price)

    bed = get_detail(house_infos, "bed")
    if(bed != ""):
        beds.append(bed)

    bath = get_detail(house_infos, "bath")
    if(bath != ""):
        baths.append(bath)

    sqft = get_detail(house_infos, "sqft")
    if(sqft != ""):
        sqfts.append(sqft)

    #get school ratings
    sch_rates = get_school_rates(soup)

    ele_sch = get_elementary_sch(sch_rates)
    ele_schs.append(ele_sch)

    mid_sch = get_middle_sch(sch_rates)
    mid_schs.append(mid_sch)

    high_sch = get_high_sch(sch_rates)
    high_schs.append(high_sch)

    msg = price +' | ' + bed + ' | ' + bath + ' | ' + sqft+ ' | ' + ele_sch+ ' | ' + mid_sch + ' | ' + high_sch
    print(msg)
    indidual_house_info.write(msg + "\n")
 