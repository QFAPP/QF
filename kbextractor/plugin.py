from yapsy.IPlugin import IPlugin


class ISourcePlugin(IPlugin):
    """
    Represents the interface for the source plugins.
    """

    def authenticate(self, subdomain, username, password):
        pass

    def retrieve_topics(self, page):
        pass

    def retrieve_articles(self, topic_name, page):
        pass

    def next_page(self, metadata):
        pass


class IDestinationPlugin(IPlugin):
    """
    Represents the interface for the destination plugins.
    """

    def store(self, topic_name, article_entry_list):
        pass