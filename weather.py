import bs4, requests
from tkinter import *

window = Tk()

window.title("Weather Forecast")

window.rowconfigure(0, minsize=400, weight=1)
window.columnconfigure(1, minsize=200, weight=1)

fr_buttons = Frame(window)
fr_buttons.grid(row=0, column=0, sticky="ns")

lbl = Label(fr_buttons, text="choose a city")
lbl.grid(row=0, column=0, sticky="ew", padx=5, pady=5)

txt = Entry(fr_buttons,width=20)
txt.grid(row=1, column=0, sticky="ew", padx=5, pady=5)
txt.focus()

def clicked():
    bigtxt.delete("1.0", END)
    city = txt.get()
    url = f'http://www.skaikairos.gr/main/{city}/position'

    res = requests.get(url)
    if res.status_code == 404:
        response =  'Your city of choise doesn\'t exist or you mispelled it.'
    else:
        soup = bs4.BeautifulSoup(res.text, 'html.parser')
        kairos = soup.find("div", {"id": "forecast-upper-seven"})
        data = list(kairos.stripped_strings)

        if data:
            response =  f"""\
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
            response =  f'There are no weather data for {city}'

    bigtxt.insert("1.0", response)

btn = Button(fr_buttons, text="Click Me", command=clicked)
btn.grid(row=2, column=0, sticky="ew", padx=5)

bigtxt = Text(window,width=70,height=30)
bigtxt.grid(row=0, column=1, sticky="nsew")

window.mainloop()
