import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import numpy as np
#from scipy.stats import norm
import statistics

# use ". venv/bin/activate" to start venv

URL = "http://www-k12.atmos.washington.edu/k12/grayskies/plot_nw_wx.cgi?Measurement=Solar&station=SEA&station=UWA&station=UWUH&interval=168&timezone=8&rightlab=y&connect=lines&groupby=overlay&begmonth=1&begday=1&begyear=2015&beghour=0&endmonth=1&endday=1&endyear=2015&endhour=0"

def main():
    data_url = "http://www-k12.atmos.washington.edu/k12/grayskies/" + get_data_url(URL)
    #print(f"{data_url}")
    raw_data_rows = get_data(data_url)
    print(f"{len(raw_data_rows)}")
    sliced_data = slice_data(raw_data_rows)
    analyze_data(sliced_data)
    plot_data(sliced_data)

def get_data_url(i):
    page = requests.get(i)
    soup = BeautifulSoup(page.content, "html.parser")
    link = soup.find("a")
    link = link.get("href")
    return link

def get_data(i):
    page = requests.get(i)
    soup = BeautifulSoup(page.content, "html.parser")
    element_list = soup.find_all("pre")
    data_table = str(element_list[1])
    line_list = data_table.split("\n")
    return line_list

def slice_data(i):
    # second table data starts at line 70
    # print(f"{line_list[70:72]}")
    # how to find length of the data table? done
    dict = {}
    #print(f"{line_list[70:74][0]}")
    last = len(i) - 1
    first = last - 1080 # 1080 is last 18 hours
    print(f"{first} to {last}")
    for element in i[first:last]:
        intraline_list = element.split()
        #print(f"{innerline_list[0]}")
        time = intraline_list[1]
        #print(f"{innerline_list[12]}")
        radiation = float(intraline_list[12])
        dict.update({time: radiation})
    #print(f"{dict}")
    return dict

def plot_data(i):
    lists = i.items() # sorted by key, return a list of tuples
    x, y = zip(*lists) # unpack a list of pairs into two tuples
    plt.plot(x, y)
    plt.xlabel("Time")
    plt.xticks([1, 135, 270, 405, 540, 675, 810, 945, 1080])
    plt.margins(0.05)
    plt.subplots_adjust(bottom=0.15)
    plt.ylabel("Solar Radiation: W/m^2")
    plt.title("Solar Radiation in Seattle, past 18 hours")
    plt.savefig("solar_radiation.png")
    #plt.show()

def analyze_data(i):
    radiation_only = list(i.values())
    print(f"N = {len(radiation_only)}")
    radiation_fresh = [value for value in radiation_only if value != 0.0]
    print(f"N = {len(radiation_fresh)} without 0.0")
    mean = np.mean(radiation_fresh)
    print(f"mean = {mean}")
    max = np.max(radiation_fresh)
    print(f"max = {max}")
    stdev = np.std(radiation_fresh)
    print(f"standard deviation = {stdev}")
    joules = sum(radiation_fresh*60)
    print(f"sum = {joules/1000000:.2f} MJ/m^2")
    #plt.hist(radiation_fresh, bins = 50)
    #plt.show()


main()
