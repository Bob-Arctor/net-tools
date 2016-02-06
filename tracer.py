import requests
from scapy.all import traceroute
import sys
from geopy.geocoders import Nominatim
import webbrowser

if len(sys.argv) != 2:
    sys.exit('Usage: traceroute.py <remote host>')

FREEGEOPIP_URL = 'http://freegeoip.net/json/'
MY_IP_URL = 'http://ip.42.pl/raw'
GOOGLE_API_KEY = 'AIzaSyAsg1SGMa85Aa8Ai0gb2VzLdRWMiNj76ms'
GOOGLE_START_URL = 'https://maps.googleapis.com/maps/api/staticmap?'

def get_lat_lon(ip):
    url = '{}/{}'.format(FREEGEOPIP_URL, ip)
    response = requests.get(url)
    response.raise_for_status()
    lat = str(response.json()["latitude"])
    lon = str(response.json()["longitude"])
    return lat, lon


def get_geolocation_for_ip(ip):
    lat, lon = get_lat_lon(ip)
    if not (float(lat)) and not (float(lon)):
        my_ip = requests.get(MY_IP_URL).content.decode("UTF-8")
        lat, lon = get_lat_lon(my_ip)

    geolocator = Nominatim()
    location = geolocator.reverse("%s, %s" % (lat, lon))

    return location.address

def make_google_marker(i, ip, check=False):
    lat, lon = get_lat_lon(ip)
    if check and not (float(lat)) and not (float(lon)):
        my_ip = requests.get(MY_IP_URL).content.decode("UTF-8")
        lat, lon = get_lat_lon(my_ip)
    #returns markers and paths
    return "&markers=color:blue%%7Clabel:%d%%7C%.6f,%.6f" % (i, float(lat), float(lon)), \
           "%%7C%.6f,%.6f" % (float(lat), float(lon))


def main():
    host = sys.argv[1]

    print("-"*50)
    print("Tracing %s" % host)
    print("-"*50)

    r1, unans = traceroute(host, maxttl=20, verbose=0)
    hops = list(r1.get_trace().values())[0]

    params = "size=1000x1000&scale=2&maptype=terrain"
    markers = ""
    paths = "&path=weight:5%%7Ccolor:0x0000ff"

    for k in hops.keys():
        print("%d -> %s (%s)" % (k, get_geolocation_for_ip(hops[k][0]), hops[k][0]))
        m, p = make_google_marker(k, hops[k][0], True)
        markers += m
        paths += p

    print("-"*50)
    print("Click the link below to see the trace:")
    print("%s%s%s%s&key=%s" % (GOOGLE_START_URL, params, markers, paths, GOOGLE_API_KEY))

    #commented out due to error in OS
    #webbrowser.open_new_tab("%s%s%s&key=%s" % (GOOGLE_START_URL, params, markers, GOOGLE_API_KEY))

if __name__ == "__main__":
    main()
