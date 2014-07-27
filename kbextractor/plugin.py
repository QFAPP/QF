from yapsy.IPlugin import IPlugin

class ISourcePlugin(IPlugin):
    """Represents the interface for the source plugins."""

    def __init__(self):
        super().__init__()
        self.options_dict = {}

    def authenticate(self):
        pass

    def help(self):
        pass

    def retrieve_topics(self, page):
        pass

    def retrieve_articles(self, topic_name):
        pass

    def next_page(self, metadata):
        pass

    def parse_options(self, options_str):
        """Parses the options provided to the plugin."""
        self.options_dict = PluginCommon.parse_options(options_str)


class IDestinationPlugin(IPlugin):
    """Represents the interface for the destination plugins."""

    def __init__(self):
        super().__init__()
        self.options_dict = {}

    def store(self, topic_name, article_entry_list):
        pass

    def parse_options(self, options_str):
        """Parses the options provided to the plugin."""
        self.options_dict = PluginCommon.parse_options(options_str)


class PluginCommon:
    """Common functions for the plugins.

    Contains all the functions that are common between the source and
    destination plugins.
    """

    @staticmethod
    def parse_options(options_str):
        """Parses the options provided to the plugin."""
        # If  no options were provided, simply return an empty dictionary
        if not options_str:
            return {}

        option_list = options_str.split(',')
        option_list_list = [value.split('=', 1) for value in option_list if
                            '=' in value]
        return dict(option_list_list)