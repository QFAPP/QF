import os

from kbextractor.plugin import IDestinationPlugin


class OnDiskPlugin(IDestinationPlugin):
    """
    This plugin will store the information on disk.

    A folder with the name of the topic will be created if necessary and the
    articles will be placed inside as plain text files.
    """

    def store(self, topic_name, article_entry_list):
        """
        Stores a list of articles into a folder having the name of the topic
        containing them.

        :param topic_name The name of the topic
        :param article_entry_list The list of entries of this topic
        """

        # Create the folder if it does not exist
        if not os.path.exists(topic_name):
            os.makedirs(topic_name)

        # Go through all the articles in this topic
        for article_entry in article_entry_list:
            article_name = article_entry.get("subject")

            # If there is no subject, it means the article is corrupted
            # therefore we skip it
            if not article_name:
                continue

            # Create the files with the content
            # Overwrite existing files
            file_name = topic_name + '/' + article_name
            with open(file_name, mode='w', encoding='utf-8') as article_file:
                article_file.write(article_entry.get("body", ""))
