#weather.py
import json
import urllib.request
import datetime

#List of cities. This is a list of Dictionary items

def import_cities():
    cities = []
    file = open("cities.txt")
    for line in file:
        city_in = line.strip().split(':')
        city = {
            "name":city_in[0],
            "lat":city_in[1],
            "lon":city_in[2],
        }
        cities.append(city)
    file.close()
    return cities

def get_cities(cities):
    print("Select a city from the list below to get the 7 day forecast")
    print("\n")
    for i in range(len(cities)):
        print("{} -- {}".format(i+1,cities[i]["name"]))
    #Get city number as referenced from the printed list. This is one higher than index list
    while True:
        city_select = int(input("Which City(1-{})? ".format(len(cities))))
        if city_select < 1 or city_select > len(cities): # check to see if we errored out last time, otherwise skip
            print("That is not a valid entry. Try again.")
        else:
            return city_select

def forecast_call(url):
    webURL = urllib.request.urlopen(url)
    data = webURL.read()
    encoding = webURL.info().get_content_charset('utf-8')
    return json.loads(data.decode(encoding))

def heat_index(TF,TDF):
    #Formula from NOAA website
    if TF <= 75:
        HI = int(TF) #HI formula doesn't apply to low temps and is NA
    else:
        T = (5.0/9.0)*(TF-32.0)
        TD = (5.0/9.0)*(TDF-32.0)
        c = 6.11*pow(10,((7.5*T/(237.7+T)))) #Saturadted vapor pressure
        d = 6.11*pow(10,((7.5*TD/(237.7+TD)))) #actual vapor pressure
        RH = 100*(d/c)

        HI = -42.379 + 2.04901523*TF + 10.14333127*RH \
             - .22475541*TF*RH - .00683783*TF*TF - .05481717*RH*RH \
             + .00122874*TF*TF*RH + .00085282*TF*RH*RH - .00000199*TF*TF*RH*RH
    return int(HI)

def output_weather(weather,city):
    #Heading
    print('\n')
    print("City: {}".format(city))
    print("{}    {}    {}    {}".format("Day".ljust(10),
                                      "Max".rjust(3),
                                      "Heat".rjust(4),
                                      "Summary"))
    print("".ljust(50,'-'))
    #Data
    for i in range(len(weather["daily"]["data"])):
        daily = weather["daily"]["data"] #Should be list of dicts for the day

        #Get the day and convert it to today/tomorrow when needed
        ddate = datetime.datetime.fromtimestamp(
            int(daily[i]["time"])
        ).strftime('%A')
        d = datetime.datetime.now() + datetime.timedelta(days=1)
        if i == 0:
            ddate = "Today"
        elif i== 1:
            ddate = "Tommorrow"

        max_temp = int(daily[i]["temperatureMax"])
        dew_point = int(daily[i]["dewPoint"]) #used for Heat index calculation
        summary = daily[i]["summary"]

        print("{} -- {} -- {} -- {}".format(ddate.ljust(10),
                                      repr(max_temp).rjust(3),
                                      repr(heat_index(max_temp,dew_point)).rjust(3),
                                      summary))


def main():
    #Get the city
    cities = import_cities()
    city_select = get_cities(cities) - 1 #subtract one to now match the list index

    #after getting the city, find the lat and lon, then send them to the data retrival
    lat = cities[city_select]["lat"]
    lon = cities[city_select]["lon"]
    url_string = "https://api.forecast.io/forecast/40c495d946e7f24d0470be483f05d4d6/"
    urlData = url_string + lat + "," + lon

    #Get Data
    weather = forecast_call(urlData)
    #Print Data
    output_weather(weather,cities[city_select]["name"])


if __name__ == "__main__":
    main()
