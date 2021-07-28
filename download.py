import urllib.request
import eyed3
import audiolab
from pathlib import Path


def download_file(url, file_path):
    with urllib.request.urlopen(url) as u:
        with open(file_path, 'wb') as f:
            f.write(u.read())
            print(f'transferred {url} to {file_path}')


def update_mp3_tag(file_path, lab, lab_ref):
    mp3 = eyed3.load(file_path)
    mp3.tag.artist = 'Dos Mundos'
    mp3.tag.album = lab['title'] + ' - ' + lab['subtitle']
    mp3.tag.album_artist = 'Dos Mundos'
    mp3.tag.title = lab_ref['label']
    mp3.tag.track_num = 1
    mp3.tag.save()


def make_dir(dir):
    Path(dir).mkdir(parents=True, exist_ok=True)


def download_lab(lab, lab_refs, should_download):
    path = f'dos_mundos/{lab["label"]}/'
    make_dir(path)
    for lab_ref in lab_refs:
        url = lab_ref['url']
        file_path = path + url.rpartition('/')[2]
        if should_download:
            download_file(url, file_path)
        update_mp3_tag(file_path, lab, lab_ref)


def main():
    should_download = True
    for lab in audiolab.load_audio_labs():
        lab_refs = audiolab.get_audio_lab_refs(lab['label'])
        download_lab(lab, lab_refs, should_download)


if __name__ == '__main__':
    main()
