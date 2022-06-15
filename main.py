from bs4 import BeautifulSoup
import requests
import csv
from datetime import date

"""
Class Description:
Represents a scraper bot using the BeautifulSoup and requests libraries to gather recent racing results.

@author: Farhan Abdulla
@version: 2022.05.31
"""
class Scraper():
    def __init__(self):
        self.scrape()

    def scrape(self):
        """
        Completes the scraping by the calling nested functions. The racing link is passed
        into get_race_result(), which then scrapes through the website and writes the csv file.
        """
        self.get_race_result(self.get_race())

    def get_race_result(self, link):
        """
        Creates a csv file and fills it up with the scraped information from the F1 website.
        @param link String containing the URL with the racing results
        """
        file = open(f'{self.circuit}{date.today().year}.csv', 'x')
        writer = csv.writer(file)
        writer.writerow(['Name', 'Car', 'Laps', 'Time', 'Points'])
        results = requests.get(link).text
        soup = BeautifulSoup(results, 'lxml')
        drivers = soup.find('table', class_='resultsarchive-table').tbody.find_all('tr')
        for driver in drivers:
            firstname = driver.find('span', class_='hide-for-tablet').text
            lastname = driver.find('span', class_='hide-for-mobile').text
            car = driver.find('td', class_='semi-bold uppercase hide-for-tablet').text
            laps = driver.find('td', class_='bold hide-for-mobile').text
            time = driver.find_all('td', class_='dark bold')[1].text
            points = driver.find_all('td', class_="bold")[3].text
            writer.writerow([f'{firstname} {lastname}', car, laps, time, points])

    def get_race(self):
        """
        Finds the URL with racing results and the most recent race.
        @return String representing the URL with the racing results
        """
        races = requests.get('https://www.formula1.com/en/results.html').text
        soup = BeautifulSoup(races, 'lxml')
        self.circuit = soup.find('table', class_='resultsarchive-table').tbody.find_all('tr')[-1].find('a', class_="dark bold ArchiveLink").text.strip()
        return 'https://www.formula1.com/' + soup.find('table', class_='resultsarchive-table').tbody.find_all('tr')[-1].a.get('href')


Scraper()