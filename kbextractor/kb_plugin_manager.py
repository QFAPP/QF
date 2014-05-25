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

        # Sort the plugins by category
        plugins = {}

        # Go through all the plugins
        for plugin in self.manager.getAllPlugins():
            # Retrieve the plugin category
            category = plugins.get(plugin.category)

            # Create the category in the dictionary if it does not exist
            if not category:
                plugins[plugin.category] = []

            # Add the plugin to the right category
            plugins[plugin.category].append(plugin)

        # Go through all the categories
        for category in plugins:
            # Print the name of the category
            print("[{0}]".format(category))

            # Print the plugin information
            for plugin_info in plugins[category]:
                print("   {0}: {1}".format(plugin_info.name, plugin_info.description))