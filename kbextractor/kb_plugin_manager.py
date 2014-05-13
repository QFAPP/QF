import os

from yapsy.PluginManager import PluginManager
from kbextractor.plugin import IDestinationPlugin, ISourcePlugin


class KbExtractorPluginManager(object):
    """
    Plugin manager for the KB Extractor.
    """

    def __init__(self):
        self.manager = PluginManager()

    def load_plugins(self):
        """
        Loads the plugins from the plugin directories.
        """
        #  Locate the current directory
        current_directory = os.path.abspath(os.path.dirname(__file__))

        # Create the list of folders containing the plugins
        plugin_directories = [
            "plugins",
            "plugins/sources",
            "plugins/destinations"]

        # Create the full path out of it
        places = []
        [places.append(os.path.join(current_directory, directory)) for directory in plugin_directories]

        # Set the plugin locations
        self.manager.setPluginPlaces(places)

        # Set the categories
        self.manager.setCategoriesFilter({
            "Destination": IDestinationPlugin,
            "Source": ISourcePlugin})
        self.manager.collectPlugins()

    def show_all(self):
        """
        Displays the name and the description of each plugin.
        """
        # Loop round the plugins and print their names.
        for plugin in self.manager.getAllPlugins():
            print("{0}: {1}".format(plugin.name, plugin.description))