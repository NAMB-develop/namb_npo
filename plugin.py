import urllib2 as U
import json as J

def json_request(url):
    request = U.urlopen(url)
    response=request.read()
    return J.loads(response)

def search(term):
    return json_request("http://apps-api.uitzendinggemist.nl/episodes/search/%s.json" % (term))

def tips():
    return json_request("http://apps-api.uitzendinggemist.nl/tips.json")

def recent():
    return json_request("http://apps-api.uitzendinggemist.nl/broadcasts/recent.json")

def recent_date(year, month, day):
    return json_request("http://apps-api.uitzendinggemist.nl/broadcasts/%s-%s-%s.json" % (year, month, day))

def popular():
    return json_request("http://apps-api.uitzendinggemist.nl/episodes/popular.json")

def series():
    return json_request("http://apps-api.uitzendinggemist.nl/series.json")

def latest(series_code):
    return json_request("http://apps-api.uitzendinggemist.nl/episodes/series/%s/latest.json" % (series_code))

def episodes(series_code):
    return json_request("http://apps-api.uitzendinggemist.nl/series/%s.json" % (series_code))

def broadcaster(broadcaster): # FIXME: Unknown workings
    return json_request("http://apps-api.uitzendinggemist.nl/episodes/broadcaster/%s.json" % (broadcaster))

def genre(genre):
    return json_request("http://apps-api.uitzendinggemist.nl/episodes/genre/%s.json" % (genre))

def episode(episode_code):
    return json_request("http://apps-api.uitzendinggemist.nl/episodes/%s.json" % (episode_code))

def load_recent():
    global RECENT
    RECENT=recent()

#Unknown
#"http://apps-api.uitzendinggemist.nl/episodes/%s/view.json"


        
