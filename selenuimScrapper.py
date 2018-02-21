 -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
import pandas as pd
# pandas sert à stocker les données
import time
import re
start_time = time.time()

data = pd.read_csv("search_test.csv",encoding = "iso-8859-1",sep=";")
# ouvrir le navigateur
browser = webdriver.Firefox()
print(data)
# les réseaux sociaux à récupérer
list = ["facebook","linkedin" ,"twitter","instagram",
    "viadeo" ,"copainsdavant","societe","tripadvisor",
        "wikipedia"]
# les données à récupérer de Linkedin
linkedin_elements =["","nom et prénom","","job","études","région","nb de relations"]
pattern = []
# création des regex
for item in list:
    pattern.append(re.compile(item))
    data[item] = ""
# création des columns
data["titre"]=""
data["job"]=""
data["études"]=""
data["région"]=""
data["relations"]=""
data["présentation"]=""
data["photo"]=""
# ouvrir la page d'acceuil de linkedin
browser.get("https://fr.linkedin.com/")
time.sleep(5)
# s'identifier
email = browser.find_element_by_id("login-email")
email.send_keys("alain.peddah@outlook.fr")
pwd = browser.find_element_by_id("login-password")
pwd.send_keys("AuCourantDeTout")
pwd.submit()
time.sleep(10)
browser.get('https://www.google.fr')
for index, row in data.iterrows():
    start_loop_time = time.time()
    actions = ActionChains(browser)
    actions.release().reset_actions()
    # récuperer l'objet contenant le champ de recherche
    element = browser.find_element_by_name("q")
    element.clear()
    # envoyer le text de la recherche
    element.send_keys(row.iloc[0]+" "+row.iloc[1])
    element.submit()
    print("-----------------------------", index, "---------------------------------------")
    time.sleep(5)
    # trouver les résultats
    results = browser.find_elements_by_class_name("g")
    not_found = [True,True,True,True,True,True,True,True,True]
    # récupérer le premier lien qui contient le réseau social
    for i,result in enumerate(results):
        try :
            result_str = results[i].find_element_by_tag_name("cite").text
            print(result_str)
            for j in range(8):
                if (re.search(pattern[j], result_str) and not_found[j]):
                    not_found[j] = False
                    data.set_value(index, list[j], result_str)
                    # ouvrir dans un nouvel onglet
                    actions.key_down(Keys.CONTROL).click(result.find_elements_by_tag_name("a")[0]).perform()
                    actions = ActionChains(browser)
                    print(list[j])
                    print(result.text)
                    print("link",result_str)
        except Exception as e:
            print(e)
        # scroller
        browser.execute_script("scrollBy(0, 120);")
        print("-----------------------------------------------------------------------")
        time.sleep(1)
    # parcourir les onglets et récupérer les infos
    windows = browser.window_handles
    for window_index in range(1,len(windows)):
        browser.switch_to_window(windows[window_index])
        current_url = browser.current_url
        try:
            if re.search(pattern[1], current_url):
                data.set_value(index, "titre",browser.find_element_by_css_selector("[class*=pv-top-card-section__headline]").text)
                data.set_value(index, "job", browser.find_element_by_css_selector("[class*=pv-top-card-section__company]").text)
                data.set_value(index, "études",browser.find_element_by_css_selector("[class*=pv-top-card-section__school]").text)
                data.set_value(index, "région",browser.find_element_by_css_selector("[class*=pv-top-card-section__location]").text)
                data.set_value(index, "relations",browser.find_element_by_css_selector("[class*=pv-top-card-section__connections]").text)
                data.set_value(index, "présentation",browser.find_element_by_css_selector("[class*=pv-top-card-section__summary]").text)
                data.set_value(index, "photo",browser.find_element_by_css_selector("[class*=pv-top-card-section__photo]").screenshot_as_base64)
            if re.search(pattern[6], current_url):
                data.set_value(index, "societe présentation", browser.find_element_by_css_selector("[id*=identitetext]").text)
                data.set_value(index, "societe synthèse",browser.find_element_by_css_selector("[id*=synthese]").text)
        except  Exception as e:
            print("Oops!  ", e.message)
            with open(str(index)+'_Failed_'+row.iloc[0]+'_'+row.iloc[1]+str(list[j])+'.html', 'w') as file:
                file.write(e.message.encode("utf-8"))
                file.write(browser.page_source.encode("utf-8"))
        time.sleep(4)
        browser.close()
    # revenir au premier onglet
    browser.switch_to_window(windows[0])
    print("--- temps par profile ---" , (time.time() - start_loop_time))
print("--- temps total ---" , (time.time() - start_time))



