import urllib
import urllib.error
import urllib.request

from flask import Flask
from bs4 import BeautifulSoup


def parse(link, date, concerts):
    event = str(link).replace("<a>", '').replace("</a>", "")\
                     .replace("</span>", '').replace("<span>", "")\
                     .replace(", More Info, Buy Tickets", "")\
                     .replace("[", '').replace("]", '')

    stripped = str(event).split(' - ', 1)
    show = str(stripped[0])
    time = str(stripped[1])

    print(stripped)

    date = str(date).replace("</span>", '').replace("<span>", '')\
                    .replace(" -", '')

    concert = "<tr> <td style='width:120'>" + date + "</td><td style='width:80'>" \
               + time + "</td><td style='width:220'>" + show + "</td></tr>"
    concerts = concerts + concert
    return concerts

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

            	concerts = parse(link, date, concerts)

            except:
                pass

    return "<body style='background-color:#F7F1E6'><center><h2>Calendar " + year + "</h2><table>" + concerts \
            + "</table></center></body>"


app = Flask(__name__)

@app.route('/')
def hello():
    return "Scraping redrocksonline.com ...<meta http-equiv='refresh' content='0; url=/rr' />", 200

@app.route("/rr")
def index():
    return scrape_rr(), 200

if __name__ == "__main__":
    app.run("0.0.0.0", 5000)