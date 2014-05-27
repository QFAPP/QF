from kbextractor.plugin import IDestinationPlugin


class OnDiskPlugin(IDestinationPlugin):
    """
    This is the On Screen Display plugin.

    It will display the topics and their articles as followed:
    [Topic 1]
        Article A
        Article B
        Article C
    [Topic 2]
        Article D
        Article E
    """

    def __init__(self):
        self.current_topic = ""

    def store(self, topic_name, article_entry_list):
        """
        Displays the content of the article_entry_list on the screen

        :param topic_name The name of the topic
        :param article_entry_list The list of entries of this topic
        """

        # Display the topic if necessary
        if self.current_topic != topic_name:
            self.current_topic = topic_name
            print ("[{0}]".format(self.current_topic))

        # Display the subject of the articles
        [print("   {0}".format(article_entry.subject)) for article_entry in article_entry_list]