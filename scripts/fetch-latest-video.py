#!/usr/bin/env python3
"""Fetch the latest long-form video or live stream of the fomeo TV
YouTube channel and save it to data/latest-video.json."""

import json
import sys
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

FEED_URL = "https://www.youtube.com/feeds/videos.xml?playlist_id={}"

# Channel playlists: "UULF" = long-form videos, "UULV" = live streams
PLAYLISTS = [
    "UULFmOyqRg2nrLsYsxE8I6eddg",
    "UULVmOyqRg2nrLsYsxE8I6eddg",
]

OUTPUT = Path(__file__).resolve().parent.parent / "data" / "latest-video.json"

NS = {
    "atom": "http://www.w3.org/2005/Atom",
    "yt": "http://www.youtube.com/xml/schemas/2015",
    "media": "http://search.yahoo.com/mrss/",
}


def fetch_entries(playlist_id):
    request = urllib.request.Request(
        FEED_URL.format(playlist_id),
        headers={"User-Agent": "fomeo-latest-video"},
    )

    with urllib.request.urlopen(request, timeout=30) as response:
        root = ET.fromstring(response.read())

    return root.findall("atom:entry", NS)


def has_views(entry):
    # Scheduled streams that haven't aired yet show up with 0 views
    stats = entry.find("media:group/media:community/media:statistics", NS)
    return stats is None or stats.get("views") != "0"


def thumbnail_url(video_id):
    # maxresdefault (1280x720) isn't generated for every video
    url = f"https://i.ytimg.com/vi/{video_id}/maxresdefault.jpg"
    request = urllib.request.Request(url, method="HEAD")

    try:
        with urllib.request.urlopen(request, timeout=30):
            return url
    except urllib.error.HTTPError:
        return f"https://i.ytimg.com/vi/{video_id}/hqdefault.jpg"


def main():
    entries = [
        entry
        for playlist_id in PLAYLISTS
        for entry in fetch_entries(playlist_id)
        if has_views(entry)
    ]

    if not entries:
        sys.exit("No entries found in feeds")

    entry = max(
        entries, key=lambda e: e.findtext("atom:published", "", NS)
    )

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
        "thumbnail": thumbnail_url(video_id),
    }

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(
        json.dumps(video, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    print(f"Latest video: {title} ({video_id})")


if __name__ == "__main__":
    main()
