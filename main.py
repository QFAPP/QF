import argparse

from kbextractor.kb_plugin_manager import KbExtractorPluginManager
from kbextractor.extractor import KbExtractor


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Export you knowledge base.")
    parser.add_argument("--source", dest="source", action="store",
                        help="Where you want to extract the data from")
    parser.add_argument("--destination", dest="destination", action="store",
                        help="Where you want to store the data")
    parser.add_argument("-sopt", "--source-options", dest="source_options", action="store",
                        nargs="?", const="", default="",
                        help="The options for the source plugin")
    parser.add_argument("-dopt", "--destination-options", dest="destination_options", action="store",
                        nargs="?", const="", default="",
                        help="The options for the destination plugin")
    parser.add_argument("--list", action="store_true",
                        help="list available plugins")

    # Parse the arguments
    args = parser.parse_args()

    # Prepare the plugin manager
    kbManager = KbExtractorPluginManager()

    # Load the plugins
    kbManager.load_plugins()

    # Display the available plugins if requested
    if args.list:
        kbManager.show_all()
        exit()

    # Set the source plugin
    sourcePluginInfo = kbManager.manager.getPluginByName("PyDesk", "Source")
    sourcePlugin = sourcePluginInfo.plugin_object
    sourcePlugin.parse_options(args.source_options)

    # Set the destination plugin
    destinationPluginInfo = kbManager.manager.getPluginByName("OSD", "Destination")
    destinationPlugin = destinationPluginInfo.plugin_object
    destinationPlugin.options_dict = {}

    # Start the extraction
    extractor = KbExtractor(sourcePlugin, destinationPlugin)
    extractor.extract()
