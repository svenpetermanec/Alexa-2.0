import urllib.request
import re

#search_keyword="home"

def find(search_keyword):
    query = urllib.parse.quote(search_keyword)
    html = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + query)
    video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
    return "https://www.youtube.com/watch?v=" + video_ids[0]

