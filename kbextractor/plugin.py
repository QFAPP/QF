from yapsy.IPlugin import IPlugin


class ISourcePlugin(IPlugin):
    """
    Represents the interface for the source plugins.
    """
    def __init__(self):
        self.options_dict = {}

    def authenticate(self):
        pass

    def help(self):
        pass

    def retrieve_topics(self, page):
        pass

    def retrieve_articles(self, topic_name, page):
        pass

    def next_page(self, metadata):
        pass

    def parse_options(self, options_str):
        """
        Parses the options provided to the plugin.
        """
        option_list = options_str.split(',')
        option_list_list = [value.split('=', 1) for value in option_list if '=' in value]
        self.options_dict = dict(option_list_list)


class IDestinationPlugin(IPlugin):
    """
    Represents the interface for the destination plugins.
    """

    def store(self, topic_name, article_entry_list):
        pass
