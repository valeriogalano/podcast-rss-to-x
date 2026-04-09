import logging
import os
import sys
import xml.etree.ElementTree as ET

import requests

from github_state import update_github_variable

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("twitter")


def fetch_last_episode(feed_url: str) -> dict:
    response = requests.get(feed_url)
    response.raise_for_status()

    root = ET.fromstring(response.content)
    item = root.find('./channel/item')

    if item is None:
        raise Exception("Nessun episodio trovato nel feed")

    title = item.findtext('title', '').strip()
    link = item.findtext('link', '').strip()

    if not title or not link:
        raise Exception(f"Titolo o link mancante: {title=} {link=}")

    return {'title': title, 'link': link}


def is_published(link: str) -> bool:
    return link == os.environ.get('LAST_PUBLISHED_URL', '')


def mark_as_published(link: str) -> None:
    logger.info(f"Aggiornamento stato: {link}")
    update_github_variable('LAST_PUBLISHED_URL', link)


def publish_to_x(episode: dict, token: str) -> None:
    content = f"🎙️ Nuovo episodio:\n{episode['title']}\n{episode['link']}"

    logger.info(f"Pubblicazione su X: {content[:80]}...")

    response = requests.post(
        'https://api.twitter.com/2/tweets',
        headers={
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json',
        },
        json={'text': content}
    )

    if response.status_code not in (200, 201):
        raise Exception(f"Errore X API {response.status_code}: {response.text}")

    logger.info("Post pubblicato con successo!")


if __name__ == "__main__":
    feed_url = os.environ.get('PODCAST_RSS_URL', 'https://pensieriincodice.it/podcast/index.xml')
    token = os.environ['X_TOKEN']

    episode = fetch_last_episode(feed_url)
    logger.info(f"Ultimo episodio: {episode['link']}")

    if is_published(episode['link']):
        logger.info("Episodio già pubblicato, niente da fare.")
        sys.exit(0)

    publish_to_x(episode, token)
    mark_as_published(episode['link'])
