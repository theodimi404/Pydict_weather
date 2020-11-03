from tkinter import *
from tkinter.ttk import *
from dotenv import load_dotenv
from tabulate import tabulate
import bs4
import os
import requests


def extract_data_from_table(index, table):
    row = table[index]
    day = row.find('th').text

    more_info = row.find_all('td')
    weather = more_info[2].text
    temperature = more_info[1].text
    feels_like = more_info[3].text
    wind = more_info[4].text
    humidity = more_info[6].text
    uv = more_info[9].text

    return [day, weather, temperature, feels_like, wind, humidity, uv]


def parsing_data(url):
    res = requests.get(url)
    if res.status_code == 404:
        response = 'Your city of choise doesn\'t exist or you mispelled it.'
    else:
        soup = bs4.BeautifulSoup(res.text, 'html.parser')
        table = soup.find('table', {'id': 'wt-ext'})
        body = table.find('tbody')
        body_info = body.find_all('tr')

        headers = ['Day', 'Weather', 'Temperature', 'Feels like', 'Wind', 'Humidity', 'UV']
        response = tabulate(
            [
                extract_data_from_table(0, body_info),
                extract_data_from_table(1, body_info),
                extract_data_from_table(2, body_info),
                extract_data_from_table(3, body_info),
            ],
            headers=headers
        )

    bigtxt.insert("1.0", response)


load_dotenv()
API_KEY = os.getenv("API_KEY")

window = Tk()

window.title("Weather Forecast")

window.rowconfigure(0, minsize=400, weight=1)
window.columnconfigure(1, minsize=200, weight=1)

fr_buttons = Frame(window)
fr_buttons.grid(row=0, column=0, sticky="ns")

lbl_country = Label(fr_buttons, text="choose a country")
lbl_country.grid(row=0, column=0, sticky="ew", padx=5, pady=5)

dropdown_menu = Combobox(fr_buttons, values=["Greece", "Great Britain"])
dropdown_menu.grid(row=1, column=0, sticky="ew", padx=5, pady=5)
dropdown_menu.set('Greece')

lbl = Label(fr_buttons, text="choose a city")
lbl.grid(row=2, column=0, sticky="ew", padx=5, pady=5)

txt = Entry(fr_buttons, width=20)
txt.grid(row=3, column=0, sticky="ew", padx=5, pady=5)
txt.focus()


def clicked():
    bigtxt.delete("1.0", END)
    if dropdown_menu.get() == 'Greece':
        city = txt.get()
        url = f'http://www.skaikairos.gr/main/{city}/position'

        res = requests.get(url)
        if res.status_code == 404:
            response = 'Your city of choise doesn\'t exist or you mispelled it.'
        else:
            soup = bs4.BeautifulSoup(res.text, 'html.parser')
            kairos = soup.find("div", {"id": "forecast-upper-seven"})
            data = list(kairos.stripped_strings)

            if data:
                response = f"""\
                    Η πρόγνωση του καιρού για {city} είναι:
                    {data[2]}
                    {data[3]}{data[4]}
                    {data[5]} {data[6]} Μποφόρ
                    ------
                    {data[7]}
                    {data[8]}
                    {data[9]}{data[10]}
                    {data[11]} {data[12]} Μποφόρ
                    ------
                    {data[13]}
                    {data[14]}
                    {data[15]}{data[16]}
                    {data[17]} {data[18]} Μποφόρ
                    ------
                    {data[19]}
                    {data[20]}
                    {data[21]}{data[22]}
                    {data[23]} {data[24]} Μποφόρ
                    (Data from skaikairos.gr)"""
            else:
                response = f'There are no weather data for {city}'

        bigtxt.insert("1.0", response)

    else:
        city = txt.get()
        url = f'https://www.timeanddate.com/weather/uk/{city}/ext'
        parsing_data(url)


btn = Button(fr_buttons, text="Click Me", command=clicked)
btn.grid(row=4, column=0, sticky="ew", padx=5)

bigtxt = Text(window, width=110, height=20)
bigtxt.grid(row=0, column=1, sticky="nsew")

window.mainloop()
