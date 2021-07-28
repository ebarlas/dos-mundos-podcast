from html.parser import HTMLParser
import urllib.request
import json

url_base = 'http://highered.mheducation.com'
url_fmt = url_base + '/sites/0073385212/student_view0/{}/laboratory_audio_program.html'


def load_audio_labs():
    with open('labs.json', 'r') as f:
        return json.load(f)


def download_page(part):
    with urllib.request.urlopen(url_fmt.format(part)) as f:
        return f.read().decode('utf-8')


def find_href(attrs):
    for attr in attrs:
        if attr[0] == 'href':
            return attr[1]


class AudioLabHtmlParser(HTMLParser):
    def __init__(self, *, convert_charrefs=True):
        super().__init__(convert_charrefs=convert_charrefs)
        self.anchor_open = None
        self.activities_seen = False
        self.pronunciation_seen = False
        self.mp3s = []

    def handle_starttag(self, tag, attrs):
        if self.activities_seen and not self.pronunciation_seen:
            if tag == 'a':
                href = find_href(attrs)
                if href and href.endswith('.mp3'):
                    self.anchor_open = tag
                    self.mp3s.append({'url': url_base + href})

    def handle_endtag(self, tag):
        if tag == self.anchor_open:
            self.anchor_open = None

    def handle_data(self, data):
        if data == 'ACTIVIDADES AUDITIVAS':
            self.activities_seen = True
        if data == 'PRONUNCIACIÓN Y ORTOGRAFÍA':
            self.pronunciation_seen = True
        if self.anchor_open:
            self.mp3s[-1]['label'] = data.rpartition(' ')[0]


def parse_audio_lab_html(html):
    parser = AudioLabHtmlParser()
    parser.feed(html)
    return parser.mp3s


def get_audio_lab_refs(part):
    return parse_audio_lab_html(download_page(part))


if __name__ == '__main__':
    labs = load_audio_labs()
    lab = get_audio_lab_refs(labs[0]['label'])
    for entry in lab:
        print(entry)
