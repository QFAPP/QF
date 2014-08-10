import unittest
import unittest.mock

from unittest.mock import MagicMock
from unittest.mock import patch

from kbextractor.kbmodels import Article
from kbextractor.plugins.destinations.osd import OSDPlugin


class TestOsdPlugin(unittest.TestCase):
    def test_osd_regular(self):
        osd_plugin = OSDPlugin()
        test_article_00 = Article()
        test_article_00.subject = "Subject 01"
        test_article_00.body = "A very small body"
        test_article_00.topic = "First topic"
        test_articles = [
            test_article_00
        ]

        mock = MagicMock(return_value="")
        with patch('builtins.print', mock):
            osd_plugin.store("test", test_articles)

        assert mock.called

    def test_osd_no_articles(self):
        osd_plugin = OSDPlugin()
        test_articles = None

        mock = MagicMock(return_value="")
        with patch('builtins.print', mock):
            osd_plugin.store("Test", test_articles)

        assert mock.called

    def test_osd_no_topic(self):
        osd_plugin = OSDPlugin()
        test_articles = None

        mock = MagicMock(return_value="")
        with patch('builtins.print', mock):
            osd_plugin.store(None, test_articles)

        assert mock.called

    def test_osd_no_article_subject(self):
        osd_plugin = OSDPlugin()
        test_article_00 = Article()
        test_article_00.subject = None
        test_article_00.body = "A very small body"
        test_article_00.topic = "First topic"
        test_articles = [
            test_article_00
        ]

        mock = MagicMock(return_value="")
        with patch('builtins.print', mock):
            osd_plugin.store("Test", test_articles)

        assert mock.called