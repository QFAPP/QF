import argparse

from kbextractor.kb_plugin_manager import KbExtractorPluginManager


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Export you knowledge base.")
    parser.add_argument("--subdomain", dest="subdomain", action="store",
                        help="Your subdomain")
    parser.add_argument("--username", dest="username", action="store",
                        help="Your username")
    parser.add_argument("--password", dest="password", action="store",
                        help="Your password")
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

    # Set the destination plugin
    destinationPluginInfo = kbManager.manager.getPluginByName("OSD", "Destination")
    destinationPlugin = destinationPluginInfo.plugin_object

    # Authenticate
    sourcePlugin.authenticate(args.subdomain, args.username, args.password)

    # Retrieve the topics
    retrieved_topics = sourcePlugin.retrieve_items("topics")

    while True:
        # We can leave if there are no more topics
        if not retrieved_topics:
            break

        # Set the entries and the meta
        topic_entries = retrieved_topics[0]
        topic_meta = retrieved_topics[1]

        # Go through the topic list
        for topic_entry in topic_entries:
            topic_entry_name = topic_entry.get("name")

            # Retrieve the articles associated to this entry
            retrieved_articles = sourcePlugin.retrieve_articles(topic_entry)
            while True:
                # We can leave if there are no more articles
                if not retrieved_articles:
                    break

                # Set the entries and the meta
                articles_entries = retrieved_articles[0]
                articles_meta = retrieved_articles[1]

                # Store the results
                destinationPlugin.store(topic_entry_name, articles_entries)

                # Retrieve the next page
                articles_next_page_url = sourcePlugin.next_page(articles_meta)

                # If there is no next page, we're done for this topic
                if not articles_next_page_url:
                    break

                # Retrieve the next page of articles
                retrieved_articles = sourcePlugin.retrieve_items(articles_next_page_url)

        # Check whether there are more topics
        topics_next_page_url = sourcePlugin.next_page(topic_meta)
        if not topics_next_page_url:
            break

        # Retrieve the next page of topics
        retrieved_topics = sourcePlugin.retrieve_items(topics_next_page_url)
