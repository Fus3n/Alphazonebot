from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import csv
import itertools
import json


class BOT:
    def __init__(self,name):
        self.name = name
        self.Search = input("Enter what to search: ")
        self.numberOfTimes = int(input('How Many pages to scrape: '))
        self.newfileData = input("Add new Page data into New Csv File? answer With y/n: ")
        self.DRIVER_PATH = ''
        with open('config.json') as file:
            config = json.load(file)
            self.DRIVER_PATH = config["DRIVER_PATH"]
        driver = webdriver.Chrome(executable_path=self.DRIVER_PATH)
        self.bot = driver

    def start(self):
        if (self.newfileData == 'y'):
            newfilestructure = True
        elif (self.newfileData == 'n'):
            newfilestructure = False
        else:
            print("Invalid Option")
        bot = self.bot
        bot.get('https://www.amazon.com/')
        print("Getting Link..")
        search = bot.find_element_by_id('twotabsearchtextbox')
        search.send_keys(self.Search)
        search.send_keys(Keys.RETURN)
        pageN = 1
        if len(str(self.numberOfTimes)) != 0:
            int(self.numberOfTimes)
            print("Scraping data..")
            time.sleep(0.5)
            print("Saving data")
            for repeat in itertools.repeat(None, self.numberOfTimes):
                title = bot.find_elements_by_class_name('a-size-medium')
                price = bot.find_elements_by_class_name('a-price-whole')
                link = bot.find_elements_by_class_name('s-no-outline')
                pages = bot.find_elements_by_class_name('a-last')
                a = 1
                if newfilestructure == True:
                    with open('pageResult' + str(pageN) + '.csv', 'a', encoding='utf-8', newline='') as csvfile:
                        feildnamess = ['ProductName', 'Price', 'Link']
                        thewriter = csv.DictWriter(csvfile, fieldnames=feildnamess)
                        thewriter.writeheader()

                        for i, f, g in zip(title, price, link):
                            links = g.get_attribute('href')
                            thewriter.writerow({'ProductName': i.text, 'Price': f.text + '$', 'Link': links})

                    if self.numberOfTimes == pageN:
                        bot.close()
                    else:
                        pages[0].find_element_by_tag_name('a').click()
                        print("PAGE SCRAPED " + str(pageN))
                        pageN += 1
                        time.sleep(2)
                elif newfilestructure == False:
                    a = 1
                    with open('pageResult.csv', 'a', encoding='utf-8', newline='') as csvfile:

                        feildnamess = ['ProductName', 'Price', 'Link']
                        thewriter = csv.DictWriter(csvfile, fieldnames=feildnamess)
                        thewriter.writeheader()

                        for i, f, g in zip(title, price, link):
                            links = g.get_attribute('href')
                            thewriter.writerow({'ProductName': i.text, 'Price': f.text + '$', 'Link': links})

                    if self.numberOfTimes == pageN:
                        bot.close()
                    else:
                        pages[0].find_element_by_tag_name('a').click()
                        pageN += 1
                        time.sleep(2)
                else:
                    pass
            print('Done! exiting in 5 seconds')
            time.sleep(5)
            bot.quit()
            exit()
        else:
            print("PLease enter an amount")
            s = BOT()
            s.start()

app = BOT("man")
app.start()
