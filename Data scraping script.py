#This script is by Dan Boguslavsky
#https://github.com/danbogu

from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import pyodbc
db_connection = pyodbc.connect( 'Driver={SQL Server};'
                                'Server=DESKTOP-2CTBPCN\SQLEXPRESS;'
                                'Database=test;'
                                'Trusted_Connection=yes;')
cursor = db_connection.cursor()

driver = webdriver.Chrome("C:\\Users\\user\\AppData\\Local\\Programs\\Python\\Python38\\chromedriver.exe")

driver.get("https://www.yad2.co.il/vehicles/private-cars?page=1")
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time

driver.get("https://www.yad2.co.il/vehicles/private-cars?page=1")

#extract all 'endings' of site URL:

URLs = []
i = 1
while True:
    not_successful = True
    soup = []
    try_num = 1
    while not_successful:
        page_url = "https://www.yad2.co.il/vehicles/private-cars?page=" + str(i)
        driver.get(page_url)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        if len(soup) != 0:
            not_successful = False
        try_num += 1
        if try_num >= 3:
            break
    i += 1
    car_num = 0
    if len(soup) != 0:
        while True:
            feed_num = 'feed_item_' + str(car_num)
            car = soup.find_all('div', {'id': feed_num})
            if len(car) == 0:
                break
            url_path = str(car)
            start = url_path.find("item-id")
            end = url_path.find(">", start)
            start = url_path.find("=", start)
            url_path = url_path[start + 2:end - 1]
            URLs.append(url_path)
            car_num += 1
        #break



for car_num in range (35):
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    feed_num = 'feed_item_' + str(car_num)
    car = soup.find_all('div', {'id':feed_num})
    url_path = str(car)
    start = url_path.find("item-id")
    end = url_path.find(">",start)
    start = url_path.find("=",start)
    url_path = url_path[start+2:end-1]
    URLs.append(url_path)

#list of all items full URLs

items_url_list = []
for item in URLs:
    items_url_list.append("https://www.yad2.co.il/item/" + item)

#tets print:

print(items_url_list)

#open each item in a different tab:
cars_db = []
i=0
for url in items_url_list:
    i += 1
    driver.get(url) #open site
    #wait for page to load fully:
    delay = 3  # seconds
    try:
        myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, 'IdOfMyElement')))
        print("Page is ready! " + "item " + str(url))
    except TimeoutException:
        pass
        #print("Loading took too much time! " + "item " + str(url))
        #continue


        #driver = webdriver.Chrome("C:\\Users\\user\\AppData\\Local\\Programs\\Python\\Python38\\chromedriver.exe")

            #for i in range (1,6):
    print("car number " + str(i) + " start.")
    #path = "C:\\Users\\user\\Desktop\\tests\\test" + str(i) + ".html"

    #driver.get(path)

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    main_title = soup.find('span', class_='main_title')
    second_title = soup.find('span', class_='second_title')
    price = soup.find('strong',class_= "price")
    top_categories = soup.find_all('dd', {'class': 'value'})
    top_categories_details = soup.find_all('dt', {'class': 'label'})
    summary = soup.find('p', {'class': 'details_text'})
    kilometers = soup.find('dd', {'id': 'more_details_kilometers'})
    engineType = soup.find('dd', {'id': 'more_details_engineType'})
    gearBox = soup.find('dd', {'id': 'more_details_gearBox'})
    color = soup.find('dd', {'id': 'more_details_color'})
    onRoadFrom = soup.find('dd', {'id': 'more_details_month'})
    testDate = soup.find('dd', {'id': 'more_details_testDate'})
    ownerID = soup.find('dd', {'id': 'more_details_ownerID'})
    tradeIn = soup.find('dd', {'id': 'more_details_tradeIn'})
    disabledFriendly = soup.find('dd', {'id': 'more_details_disabledFriendly'})

    car = []
    year = None
    hand = None
    engineSize = None
    top_categories_details = [year, hand, engineSize]
    top_categories_details_names = ["year","hand","engineSize"]


    if main_title is not None:
        print(main_title.text.strip())
        main_title = main_title.text.strip()
        car.append(main_title)
    else:
        car.append(None)

    if second_title is not None:
        print(second_title.text.strip())
        second_title = second_title.text.strip()
        car.append(second_title)
    else:
        car.append(None)

    if price is not None:
        print(price.text.strip())
        price = price.text.strip()
        car.append(price)
    else:
        car.append(None)

    if top_categories is not None:
        if len(top_categories) != 0:
            for index in range(len(top_categories_details_names)):
                print(top_categories_details_names[index] + " : " + top_categories[index].text.strip())
                top_categories_details[index] = top_categories[index].text.strip()
                if top_categories_details[index] is not None:
                    car.append(top_categories_details[index])
                else:
                    car.append(None)

    if summary is not None:
        print(summary.text.strip())
        summary = summary.text.strip()
        car.append(summary)
    else:
        car.append(None)

    if kilometers is not None:
        print(kilometers.text.strip())
        kilometers = kilometers.text.strip()
        car.append(kilometers)
    else:
        car.append(None)

    if engineType is not None:
        print(engineType.text.strip())
        engineType = engineType.text.strip()
        car.append(engineType)
    else:
        car.append(None)

    if gearBox is not None:
        print(gearBox.text.strip())
        gearBox = gearBox.text.strip()
        car.append(gearBox)
    else:
        car.append(None)

    if color is not None:
        print(color.text.strip())
        color = color.text.strip()
        car.append(color)
    else:
        car.append(None)

    if onRoadFrom is not None:
        print(onRoadFrom.text.strip())
        onRoadFrom = onRoadFrom.text.strip()
        car.append(onRoadFrom)
    else:
        car.append(None)

    if testDate is not None:
        print(testDate.text.strip())
        testDate = testDate.text.strip()
        car.append(testDate)
    else:
        car.append(None)

    if ownerID is not None:
        print(ownerID.text.strip())
        ownerID = ownerID.text.strip()
        car.append(ownerID)
    else:
        car.append(None)

    if tradeIn is not None:
        print(tradeIn.text.strip())
        tradeIn = tradeIn.text.strip()
        car.append(tradeIn)
    else:
        car.append(None)

    if disabledFriendly is not None:
        print(disabledFriendly.text.strip())
        disabledFriendly = disabledFriendly.text.strip()
        car.append(disabledFriendly)
    else:
        car.append(None)

    ##SQL insert:

    attributes_list = [main_title, second_title, price,
                       top_categories_details[0], #year
                       top_categories_details[1], #hand
                       top_categories_details[2], #engineSize
                       # year, hand, engineSize,
                        summary, kilometers, engineType,
                       gearBox, color, onRoadFrom, testDate, ownerID,
                       tradeIn, disabledFriendly,url]


    statment = 'INSERT INTO test.dbo.CARS VALUES ('
    for attribute in attributes_list:
        if attribute is not None:
            if "'" in attribute:
                attribute = attribute.replace("'","")
        statment += "'" + str(attribute) + "'" + ","
    statment = statment[:-1]
    statment += ")"


    cursor.execute(statment)
    db_connection.commit()



    cars_db.append(car)
    print("car number " + str(i) + " end.")


cursor.close()
del cursor
driver.close()


#All the project is for self learning purpose only.