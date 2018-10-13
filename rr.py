import urllib
import urllib.error
import urllib.request

from flask import Flask
from bs4 import BeautifulSoup

def scrape_rr():
    year = "2019"
    base_url = "https://www.redrocksonline.com//events/calendar/%s/" % year
    count = 0
    concerts = ""
    while count < 13:
        count = count + 1

        url = base_url + str(count)
        hdr = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)',
               'Cache-Control': 'max-age=0'}

        req = urllib.request.Request(url, headers=hdr)
        response = urllib.request.urlopen(req)
        response.read()

        try:
            page = urllib.request.urlopen(req)
        except urllib.error.HTTPError as e:
            print(e)

        content = page.read()

        refined_html = str(content).replace('\\', '')
        html = BeautifulSoup(refined_html, 'lxml')
        data = html.findAll("div", {"class": 'cat-4'})

        for i in data:

            # select links (which have desc) and dates
            link = i.select("a")
            date = i.find("span", {"class": 'dt'})

            # clear tags in html
            for tag in i.find_all(True):
                tag.attrs = {}

            try:

                event = str(link).replace("<a>", '').replace("</a>", '')\
                                 .replace("</span>", '').replace("<span>", '')\
                                 .replace(", More Info, Buy Tickets", '').replace("[", '')\
                                 .replace("]", '')

                date = str(date).replace("</span>", '').replace("<span>", '')\
                                .replace(" -", '')

                concert = date + ' : ' + event
                concerts = concerts + "<br>" + concert
            except:
                pass
    return concerts


app = Flask(__name__)

@app.route('/')
def hello():
    return "Scrapping redrocksonline.com ...<meta http-equiv='refresh' content='0; url=/rr' />", 200

@app.route("/rr")
def index():
    return scrape_rr(), 200 
 
if __name__ == "__main__":
    app.run("0.0.0.0",5000)