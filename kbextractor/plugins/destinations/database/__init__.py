from kbextractor.plugin import IDestinationPlugin
from .models import Article, Topic


class DatabasePlugin(IDestinationPlugin):
    """
    Plugin storing the articles in a database.
    """

    def store(self, topic_name, article_entry_list):
        """
        Stores the article entries in the database.

        :param topic_name The name of the topic
        :param article_entry_list The list of entries of this topic
        """

        try:
            # Try to retrieve the topic to see if it exists already
            topic = Topic.get(Topic.name == topic_name)
        except Topic.DoesNotExist:
            # If not, create it
            topic = Topic.create(name=topic_name)

        # Go through all the articles in this topic
        for article_entry in article_entry_list:
            article_name = article_entry.get("subject", "")

            # If there is no subject, it means the article is corrupted
            # therefore we skip it
            if not article_name:
                continue

            # Create the files with the content
            # Overwrite existing files
            try:
                article = Article.create(topic=topic,
                                         subject=article_name,
                                         body=article_entry.get("body", ""))
            except Article.DoesNotExist:
                pass