import sys, pyperclip, bs4, requests

def get_weather(city):
    url = f'http://www.skaikairos.gr/main/{city}/position'

    res = requests.get(url)
    if res.status_code != requests.codes.ok:
        return 'Your city of choise doesn\'t exist or you mispelled it.'

    soup = bs4.BeautifulSoup(res.text, 'html.parser')
    kairos = soup.find("div", {"id": "forecast-upper-seven"})
    data = list(kairos.stripped_strings)

    if data:
        return f"""\
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
        return f'There are no weather data for {city}'

if len(sys.argv) > 1:
    # Get city from command line.
    city = ' '.join(sys.argv[1:])
    response = get_weather(city)
    print(response)
    input('Press ENTER to exit')
else:
    # Get city from clipboard.
    city = pyperclip.paste()
    response = get_weather(city)
    print(response)
    input('Press ENTER to exit')
