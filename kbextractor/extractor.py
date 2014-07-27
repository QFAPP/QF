class KbExtractor:
    """Perform the data extraction task.

    """

    def __init__(self, source_plugin, destination_plugin):
        self.source_plugin = source_plugin
        self.destination_plugin = destination_plugin

    def extract(self):
        # Authenticate
        self.source_plugin.authenticate()

        # Retrieve the topics
        retrieved_topics = self.source_plugin.retrieve_items("topics")

        while True:
            # We can leave if there are no more topics
            if not retrieved_topics:
                break

            # Set the entries and the meta
            topic_entries = retrieved_topics[0]
            topic_meta = retrieved_topics[1]

            # Go through the topic list
            for topic_entry in topic_entries:
                topic_entry_name = topic_entry.name

                # Retrieve the articles associated to this entry
                retrieved_articles = self.source_plugin.retrieve_articles(
                    topic_entry)
                while True:
                    # We can leave if there are no more articles
                    if not retrieved_articles:
                        break

                    # Set the entries and the meta
                    articles_entries = retrieved_articles[0]
                    articles_meta = retrieved_articles[1]

                    # Store the results
                    self.destination_plugin.store(topic_entry_name,
                                                  articles_entries)

                    # Retrieve the next page
                    articles_next_page_url = self.source_plugin.next_page(
                        articles_meta)

                    # If there is no next page, we're done for this topic
                    if not articles_next_page_url:
                        break

                    # Retrieve the next page of articles
                    retrieved_articles = self.source_plugin.retrieve_items(
                        articles_next_page_url)

            # Check whether there are more topics
            topics_next_page_url = self.source_plugin.next_page(topic_meta)
            if not topics_next_page_url:
                break

            # Retrieve the next page of topics
            retrieved_topics = self.source_plugin.retrieve_items(
                topics_next_page_url)