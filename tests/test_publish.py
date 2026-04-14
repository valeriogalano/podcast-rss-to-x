import os
from unittest.mock import MagicMock, patch

import pytest

from publish import (
    fetch_last_episode,
    is_published,
    mark_as_published,
    publish_to_x,
)

SAMPLE_RSS = b"""<?xml version="1.0"?>
<rss version="2.0">
  <channel>
    <item>
      <title>Episodio 42</title>
      <link>https://example.com/ep42</link>
    </item>
  </channel>
</rss>"""


class TestFetchLastEpisode:
    def test_parses_title_and_link(self):
        mock_resp = MagicMock()
        mock_resp.content = SAMPLE_RSS
        with patch("publish.requests.get", return_value=mock_resp):
            episode = fetch_last_episode("https://feed.example.com/rss")
        assert episode["title"] == "Episodio 42"
        assert episode["link"] == "https://example.com/ep42"

    def test_raises_on_empty_feed(self):
        empty_rss = b"""<?xml version="1.0"?><rss><channel></channel></rss>"""
        mock_resp = MagicMock()
        mock_resp.content = empty_rss
        with patch("publish.requests.get", return_value=mock_resp):
            with pytest.raises(Exception, match="Nessun episodio"):
                fetch_last_episode("https://feed.example.com/rss")

    def test_raises_on_missing_link(self):
        rss = b"""<?xml version="1.0"?><rss><channel><item><title>Solo titolo</title></item></channel></rss>"""
        mock_resp = MagicMock()
        mock_resp.content = rss
        with patch("publish.requests.get", return_value=mock_resp):
            with pytest.raises(Exception):
                fetch_last_episode("https://feed.example.com/rss")

    def test_raises_on_http_error(self):
        mock_resp = MagicMock()
        mock_resp.raise_for_status.side_effect = Exception("500")
        with patch("publish.requests.get", return_value=mock_resp):
            with pytest.raises(Exception):
                fetch_last_episode("https://feed.example.com/rss")


class TestIsPublished:
    def test_returns_true_when_link_matches_env(self):
        with patch.dict(os.environ, {"LAST_PUBLISHED_URL": "https://example.com/ep42"}):
            assert is_published("https://example.com/ep42") is True

    def test_returns_false_when_link_differs(self):
        with patch.dict(os.environ, {"LAST_PUBLISHED_URL": "https://example.com/ep41"}):
            assert is_published("https://example.com/ep42") is False

    def test_returns_false_when_env_missing(self):
        env = {k: v for k, v in os.environ.items() if k != "LAST_PUBLISHED_URL"}
        with patch.dict(os.environ, env, clear=True):
            assert is_published("https://example.com/ep42") is False


class TestMarkAsPublished:
    def test_calls_update_github_variable(self):
        with patch("publish.update_github_variable") as mock_update:
            mark_as_published("https://example.com/ep42")
        mock_update.assert_called_once_with("LAST_PUBLISHED_URL", "https://example.com/ep42")


class TestPublishToX:
    def test_sends_correct_request(self):
        episode = {"title": "Episodio Test", "link": "https://ex.com/ep"}
        mock_resp = MagicMock()
        mock_resp.status_code = 201
        with patch("publish.requests.post", return_value=mock_resp) as mock_post:
            publish_to_x(episode, "BEARER_TOKEN")
        mock_post.assert_called_once()
        call_kwargs = mock_post.call_args
        assert "Bearer BEARER_TOKEN" in call_kwargs[1]["headers"]["Authorization"]
        assert "Episodio Test" in call_kwargs[1]["json"]["text"]
        assert "https://ex.com/ep" in call_kwargs[1]["json"]["text"]

    def test_raises_on_api_error(self):
        episode = {"title": "Test", "link": "https://ex.com/ep"}
        mock_resp = MagicMock()
        mock_resp.status_code = 403
        mock_resp.text = "Forbidden"
        with patch("publish.requests.post", return_value=mock_resp):
            with pytest.raises(Exception, match="Errore X API"):
                publish_to_x(episode, "BAD_TOKEN")
