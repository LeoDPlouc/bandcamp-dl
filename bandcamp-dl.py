import urllib.request as req
import requests
import sys
import re

def find_root(url):
    pattern = re.compile("https://.*?com")
    root = re.findall(pattern, url)[0]

    return root

def find_track_list(url):
    response =  req.urlopen(url)

    html = response.read().decode("utf-8")
    html = html.strip()

    pattern = re.compile("<a.*?a>", flags=re.DOTALL)
    match = re.findall(pattern,html)
    match = [e for e in match if "/track/" in e]

    pattern = re.compile("<a href=\".*?\"")
    match = "\n".join(e for e in match)
    match = re.findall(pattern, match)
    match = [e for e in match if "?" not in e]
    
    pattern = re.compile("\".*?\"")
    match = "\n".join(e for e in match)
    match = re.findall(pattern, match)
    match = [e[1:-1] for e in match]

    return match

def find_track_url(url):
    response =  req.urlopen(url)

    html = response.read().decode("utf-8")
    html = html.strip()

    pattern = re.compile("{\"mp3-128\":.*?}")
    match = re.findall(pattern, html)
    match = "\n".join(e for e in match)

    pattern = re.compile("\"https.*?\"")
    track_url = re.findall(pattern, match)[0]
    track_url = track_url[1:-1]

    return track_url

def find_title(url):
    return url.split("/")[-1]

def download_track(url):
    data = requests.get(url)

    with open(title + ".mp3", "wb") as f:
        f.write(data.content)

if __name__ == "__main__":

    url = sys.argv[1]

    print("URL : " + url)

    root = find_root(url)

    print ("Root : " + root)

    tracks = list()

    if "album" in url :
        print("Album detected")

        print("Fetching track's urls")

        tracks = find_track_list(url)
        tracks = [root + e for e in tracks]
    else: 
        print("Single track detected")
        
        tracks.append(url)
    
    for t in tracks:
        title = find_title(t)

        print("Working on track : " + title)

        print("Finding mp3's url")
        track_url = find_track_url(t)

        print("Downloading track")
        download_track(track_url)
        print("Download completed")