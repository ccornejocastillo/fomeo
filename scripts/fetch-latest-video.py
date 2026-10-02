#!/usr/bin/env python3
"""Fetch the latest long-form video of the fomeo TV YouTube channel
and save it to data/latest-video.json."""

import json
import sys
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

# "UULF" playlist = channel uploads excluding Shorts and live streams
FEED_URL = (
    "https://www.youtube.com/feeds/videos.xml"
    "?playlist_id=UULFmOyqRg2nrLsYsxE8I6eddg"
)

OUTPUT = Path(__file__).resolve().parent.parent / "data" / "latest-video.json"

NS = {
    "atom": "http://www.w3.org/2005/Atom",
    "yt": "http://www.youtube.com/xml/schemas/2015",
}


def main():
    request = urllib.request.Request(
        FEED_URL, headers={"User-Agent": "fomeo-latest-video"}
    )

    with urllib.request.urlopen(request, timeout=30) as response:
        root = ET.fromstring(response.read())

    entry = root.find("atom:entry", NS)

    if entry is None:
        sys.exit("No entries found in feed")

    video_id = entry.findtext("yt:videoId", namespaces=NS)
    title = entry.findtext("atom:title", namespaces=NS)
    published = entry.findtext("atom:published", namespaces=NS)

    if not video_id or not title or not published:
        sys.exit("Incomplete entry in feed")

    video = {
        "videoId": video_id,
        "title": title,
        "published": published,
        "url": f"https://www.youtube.com/watch?v={video_id}",
        "thumbnail": f"https://i.ytimg.com/vi/{video_id}/hqdefault.jpg",
    }

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(
        json.dumps(video, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    print(f"Latest video: {title} ({video_id})")


if __name__ == "__main__":
    main()
