import csv
import requests
from bs4 import BeautifulSoup
from time import sleep
from random import choice, uniform
import re

useragents = open('useragents.txt').read().split('\n')
proxies_http = open('proxiesHTTP.txt').read().split('\n')
proxies_https = open('proxiesHTTPS.txt').read().split('\n')
alinks = []
instalink = []

pageurl = 'https://lovehairstyles.com/' #here we type the name of the site
pagenum = 22 #here we enter a number of pages in search
    

def get_html(url, useragent, proxy):
    url = pageurl+'page/'+ str(i+1)+'?s='
    
    sleep(uniform(0.1, 1))
    print(url)
    proxy = {
        'http': 'http://' + choice(proxies_http),
        'https': 'https://' + choice(proxies_https)
    }
    useragent = {
        'User-Agent': choice(useragents)
    }

    r = requests.get(url)
    print(r)
    return r.text

def get_content(html,alinks):
    soup = BeautifulSoup(html, 'lxml')
    all_links = soup.find("div", { "class" : "site-content" }).find_all('h2')
    for link in all_links:
           ahref = link.a.attrs['href']
           alinks.append(ahref)

def get_insta(html,instalink):
    soup = BeautifulSoup(html, 'lxml')
    elems = soup.find_all("span", {"class": "imgsource"})
    for elem in elems:
        name = elem.text
        data = {
             'name': name
            }
        instalink.append(data)

def write_csv(i, data):
    with open('myhrefs.csv', 'a') as f:
        writer = csv.writer(f)
        writer.writerow((data['name']))
        print(i, data['name'], 'parsed')
 
def main():
    #STEP 1 - LOOP THROUGH SEARCH PAGE
    for i in range(2):
        url = pageurl+'page/'+ str(i+1)+'?s='
        sleep(uniform(0.1, 1))
        print(url)
        proxy = {
            'http': 'http://' + choice(proxies_http),
            'https': 'https://' + choice(proxies_https)
        }
        useragent = {
            'User-Agent': choice(useragents)
        }
        try:
            html = get_html(url, useragent, proxy)
        except:
            print(proxy['https'] + "did'n work")
            continue
        get_content(html,alinks)
    print(alinks)

    #STEP 2 - LOOP THROUGH POSTS
    for link in alinks:
        sleep(uniform(0.1, 1))
        proxy = {
            'http': 'http://' + choice(proxies_http),
            'https': 'https://' + choice(proxies_https)
        }
        useragent = {
            'User-Agent': choice(useragents)
        }
        try:
            html = get_html(link, useragent, proxy)
        except:
            print(proxy['https'] + "did'n work")
        get_insta(html, instalink)

    #STEP 2 - WRITE SCV
    for i, data in enumerate(instalink):
        write_csv(i, data)
        
    
 
if __name__ == '__main__':
    main()