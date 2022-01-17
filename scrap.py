from selenium import webdriver
import pandas as pd
import time
import re

try:
    raw_data = {'name': ['name'],
                'company': ['company'],
                'com1': ['com1'],
                'com1_con': ['com1_con'],
                'com2': ['com2'],
                'com2_con': ['com2_con'],
                'com3': ['com3'],
                'com3_con': ['com3_con'],
                'com4': ['com4'],
                'com4_con': ['com4_con'],
                'com5': ['com5'],
                'com5_con': ['com5_con'],
                'ph': ['ph'],
                'dosage': ['dosage']
                }
    print('--', raw_data)
    df = pd.DataFrame(raw_data,
                      columns=['name', 'company', 'com1', 'com1_con',
                               'com2', 'com2_con', 'com3', 'com3_con', 'com4', 'com4_con', 'com5',
                               'com5_con', 'ph', 'dosage'])
    df.to_csv('Result.csv', mode='a', header=False, index=False)

except Exception as ex:
    print(ex)
    
def getdata(txt, reg):
    com1 = ''
    com1_con = ''
    com2 = ''
    com2_con = ''
    matchs = re.findall(reg, txt)
    if matchs:
        if 'oil' in reg:
            com1_con = matchs[0].replace('oil ', '')
            ss = txt.split(matchs[0])
            ss = ss[0].strip().split(' ')
            com1 = ss[-1] + ' oil'
        elif 'benz' in reg:
            com1_con = matchs[0].split('(')[1]
            com1 = matchs[0].split('(')[0]
            if len(matchs) > 1:
                com2_con = matchs[1].split('(')[1]
                com2 = matchs[1].split('(')[0]
        else:
            com1_con = matchs[0].split('(')[1]
            com1 = matchs[0].split('(')[0]
        com1_con = com1_con.replace('(', '').replace(')', '')
        com2_con = com2_con.replace('(', '').replace(')', '')

    if 'benz' in reg:
        return com1, com2, com1_con, com2_con
    return com1, com1_con


oil_reg = 'oil \(.*?\)'
gly_reg = 'glycer\w+ \(.*?\)'
egg_reg = 'egg \w+ \(.*?\)'
benz_reg = 'benz\w+ \w+ \(.*?\)|\w+ benz\w+ \(.*?\)'

url = 'https://dailymed.nlm.nih.gov/dailymed/search.cfm?labeltype=all&query=propofol&pagesize=200&page=1'
browser = webdriver.Chrome(executable_path='chromedriver')
browser.get(url)
browser.implicitly_wait(10)
articles = browser.find_elements_by_xpath("//div[@class='results']/article")

urls = []
for article in articles:
    url = article.find_element_by_class_name('drug-info-link').get_attribute('href')
    urls.append(url)

for url in urls:
    try:
        browser.get(url)
        browser.implicitly_wait(10)
        name = ''
        name = browser.find_element_by_id('drug-label').text
        company = ''
        company = browser.find_element_by_xpath("//ul[@class='drug-information'][1]/li[2]").text.replace('Packager: ', '')
        
        browser.find_element_by_id('anch_dj_109').click()
        time.sleep(1)
        
        li_tags = browser.find_elements_by_xpath("//div[@id='drug-information']/div["
                                                 "@class='drug-label-sections']/ul/li")
        dosage = ''
        com1 = ''
        com1_con = ''
        com2 = ''
        com2_con = ''
        com3 = ''
        com3_con = ''
        com4 = ''
        com4_con = ''
        com5 = ''
        com5_con = ''
        ph = ''
        for li_tag in li_tags:
            txt = li_tag.text
            if 'DESCRIPTION' in txt:
                com1, com1_con = getdata(txt, oil_reg)
                com2, com2_con = getdata(txt, gly_reg)
                com3, com3_con = getdata(txt, egg_reg)
                com4, com5, com4_con, com5_con = getdata(txt, benz_reg)
                ph = txt.split('a pH of ')[-1]
                break
        for li_tag in li_tags:
            txt = li_tag.text
            if 'SUMMARY OF DOSAGE GUIDELINES' in txt:
                tables = li_tag.find_elements_by_tag_name('table')
                for table in tables:
                    trs = table.find_elements_by_tag_name('tr')
                    for tr in trs:
                        if 'Induction of General Anesthesia' in tr.text:
                            tds = tr.find_elements_by_tag_name('td')
                            td1_txt = tds[0].text
                            td2_txt = tds[1].text
                            if 'Induction of General Anesthesia' in td1_txt:
                                dosage = td2_txt
                                break
        try:
            raw_data = {'name': [name],
                        'company': [company],
                        'com1': [com1],
                        'com1_con': [com1_con],
                        'com2': [com2],
                        'com2_con': [com2_con],
                        'com3': [com3],
                        'com3_con': [com3_con],
                        'com4': [com4],
                        'com4_con': [com4_con],
                        'com5': [com5],
                        'com5_con': [com5_con],
                        'ph': [ph],
                        'dosage': [dosage]
                            }
            print('--', raw_data)
            df = pd.DataFrame(raw_data,
                              columns=['name', 'company', 'com1', 'com1_con',
                                       'com2', 'com2_con', 'com3', 'com3_con', 'com4', 'com4_con', 'com5',
                                       'com5_con', 'ph', 'dosage'])
            df.to_csv('Result.csv', mode='a', header=False, index=False)

        except Exception as ex:
            print(ex)
    except Exception as ex:
        print(ex)

browser.quit()