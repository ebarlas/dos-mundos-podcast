# Dos Mundos Podcast

This code repository contains utilities for converting Dos Mundos Spanish textbook
audio activities into a podcast feed.

* `labs.json` - JSON array of audio lab parts and chapters
* `audiolab.py` - Module for parsing audio lab HTML pages and extracting audio lab activities
* `download.py` - Module for downloading audio lab MP3s, updating ID3 tags, and arranging files in a local directory tree
* `podcast.py` - Module for creating podcast feed RSS files for each audio lab chapter