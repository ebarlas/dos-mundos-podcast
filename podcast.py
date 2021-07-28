import sys

from feedgen.feed import FeedGenerator
import audiolab


def make_podcast_feed(part, mp3s, feed_url, mp3_url_prefix):
    fg = FeedGenerator()
    fg.title(part['title'])
    fg.subtitle(part['subtitle'])
    fg.author({'name': 'McGraw-Hill', 'email': 'mhhe_create@mheducation.com'})
    fg.logo('http://highered.mheducation.com/sites/dl/free/0073385212/cover/Terrell7e10pt_nm2.jpg')
    fg.link(href=feed_url.format(part['label']), rel='self')
    fg.language('en')
    fg.load_extension('podcast')
    fg.podcast.itunes_category('Education', 'Spanish')
    for mp3 in mp3s:
        mp3_url = mp3_url_prefix + mp3['url'].rpartition('/')[2]
        fe = fg.add_entry()
        fe.id(mp3_url)
        fe.title(mp3['label'])
        fe.description(mp3['label'])
        fe.enclosure(mp3_url, 0, 'audio/mpeg')
    fg.rss_str(pretty=True)
    fg.rss_file(f'podcast/{part["label"]}.xml')


def make_podcast_feeds(url_prefix):
    for p in audiolab.load_audio_labs():
        mp3s = audiolab.get_audio_lab_refs(p['label'])
        feed_url = f'{url_prefix}/podcast/{{}}.xml'
        mp3_url_prefix = f'{url_prefix}/dos_mundos/{p["label"]}/'
        make_podcast_feed(p, mp3s, feed_url, mp3_url_prefix)


if __name__ == '__main__':
    if len(sys.argv) == 2:
        make_podcast_feeds(sys.argv[1])