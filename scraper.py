import bs4
from bs4 import BeautifulSoup
import urllib2
import json

def get_asns_for_country(countryUrl):
    req = urllib2.Request(countryUrl, headers={ 'User-Agent': 'Mozilla/5.0' })
    html = urllib2.urlopen(req).read()
    soup = bs4.BeautifulSoup(html,  "html.parser")
    resolve_asn_info(soup, countryUrl.split('/')[-1])

def resolve_asn_info(soup, country):
    for tr in soup.find_all('tr'):
        asnRoutes = []
        asnInfo = []
        for td in tr.find_all('td'):
            for td in tr.find_all('td', class_="alignright"):
                asnRoutes.append(td.text)
                if asnRoutes:
                    if len (asnRoutes) == 4:
                        build_json(tr.find_all('td')[0].text, country, tr.find_all('td')[1].text, [asnRoutes[1],asnRoutes[3]])

def get_list_countries(url):
    list_countries = []
    req = urllib2.Request(url, headers={ 'User-Agent': 'Mozilla/5.0' })
    html = urllib2.urlopen(req).read()
    soup = bs4.BeautifulSoup(html,  "html.parser")
    for country in soup.find_all('td', class_="centeralign"):
        if isinstance(country.string, unicode):
            list_countries.append("".join(['http://bgp.he.net/country/', "".join(country.string.split())]))
    return list_countries

def build_json(AsnId, CountryID, Name, Routes):
    data = {}
    data2 = {}
    data2['Country'] = CountryID
    data2['Name'] = Name
    data2['Routes v6'] = Routes[0]
    data2['Routes v4'] = Routes[1]
    data[int(AsnId[2:])] = data2
    json_data = json.dumps(data, indent=4)
    with open('data.json', 'ab') as f:
             json.dump(data, f)
    print json_data

def do_scrap():
    countries = get_list_countries('http://bgp.he.net/report/world')
    for country in countries:
        print country 
        get_asns_for_country(country)

do_scrap()
