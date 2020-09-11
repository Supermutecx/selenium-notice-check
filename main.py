from selenium import webdriver
from selenium.webdriver.common.by import By
import csv

def main():
    option = webdriver.ChromeOptions()
    option.add_argument('--headless')
    browser = webdriver.Chrome(executable_path='./chromedriver', options=option)
    browser.get('https://www.atlanticarea.uscg.mil/Our-Organization/District-8/District-Units/Sector-Houston-Galveston/Units/VTS-Port-Arthur/Marine-Safety-Information-Bulletins/')
    tableData = browser.find_element_by_xpath("//div[@class='Normal']//table[2]")
    diffData = checkNotification(tableData)
    if len(diffData) > 0:
        for diff in diffData:
            tr = tableData.find_element_by_xpath("//div[@class='Normal']//table[2]//tr[{}]".format(diff))
            link = tr.find_elements_by_tag_name("a")[0].get_attribute('href')
            title = tr.text
            print(link)
            print(title)
        saveHistory(tableData)
    
def checkNotification(tableData):
    ret = []
    originalData = []
    countWeb = 0
    with open('history.csv', 'r') as file:
        reader = csv.reader(file)
        trCount = len(tableData.find_elements_by_tag_name('tr'))
        for row in reader:
            originalData.append(row)
        for tr in tableData.find_elements_by_tag_name('tr'):
            countWeb = countWeb + 1
            temp = []
            for td in tr.find_elements_by_tag_name("td"):
                temp.append(td.text)
            if temp not in originalData:
                ret.append(countWeb)
    return ret

def saveHistory(tableData):
    with open('history.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        for tr in tableData.find_elements_by_tag_name("tr"):
            temp = []
            for td in tr.find_elements_by_tag_name("td"):
                temp.append(td.text)
            writer.writerow(temp)

if __name__ == "__main__":
    main()
