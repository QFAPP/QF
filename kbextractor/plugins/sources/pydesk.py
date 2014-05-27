import requests

from kbextractor.plugin import ISourcePlugin
from kbextractor.kbmodels import Article, Topic


class PyDesk(ISourcePlugin):
    """
    Plugin retrieving the data from desk.com
    """

    def __init__(self):
        self.subdomain = ""
        self.user = ""
        self.password = ""
        self.base_url = ""
        self.topic = ""

    def authenticate(self, subdomain, username, password):
        """
        Prepares the data that wil be used to authenticate.
        """
        self.subdomain = subdomain
        self.user = username
        self.password = password
        self.base_url = "https://" + self.subdomain + ".desk.com"

    def next_page(self, metadata):
        """
        Retrieves the URL of the next page from the meta data.

        :param metadata The meta data to parse to find the next page URL
        :return The URL of the next page if available
        """
        # If there is no meta data there is nothing to do
        if not metadata:
            return

        # Retrieve the next page information
        next_page = metadata.get("next")
        if not next_page:
            return

        # Retrieve the next page URL
        return next_page.get("href")

    def retrieve_topics(self, topic_page):
        """
        Retrieves the topics.
        """
        if not topic_page:
            item_to_retrieve = "topics"
        else:
            item_to_retrieve = topic_page
        return self.retrieve_items(item_to_retrieve)

    def retrieve_articles(self, topic_entry):
        """
        Saves a topic entry and its content on disk.

        :param topic_entry: the topic entry to save on disk
        """
        # If there is no data there is nothing to do
        if not topic_entry:
            return

        # The name of the topic will be the name of the folder to create
        topic_name = topic_entry.name

        # The name of the topic is mandatory
        if not topic_name:
            print('Corrupted entry. The name is missing.')
            return
        self.topic = topic_name

        # Retrieve the link pointing to to all articles in this topic
        href = topic_entry.meta.get("articles", {}).get("href")

        # Leave if there is no link pointing to the articles
        if not href:
            print('There is no URL to retrieve the articles.')
            return

        # Retrieve all the articles of a topic
        return self.retrieve_items(href)

    def retrieve_items(self, item):
        """
        Queries the API to retrieve the items.

        :param item The name of an item type or its URL (the part after the base
         URL)
        :return Returns a tuple whose first member is the list of entries of the
         requested item type, and the second one is the metadata.
        """
        # Build a dictionary of pre-defined types
        type_dict = {"topics": "/api/v2/topics.json",
                     "articles": "/api/v2/articles.json"}
        href = type_dict.get(item, item)

        # Build the url.
        url = self.base_url + href

        # Query the API.
        response = requests.get(url, auth=(self.user, self.password))

        # Check for HTTP codes other than 200.
        if response.status_code != 200:
            print('Status:',
                  response.status_code,
                  'Problem with the request. Exiting.')
            raise Exception

        # Decode the response
        items_data = response.json()

        # Return a tuple containing the list of items and the metadata
        embedded_items = items_data.get("_embedded", {})
        item_entries = embedded_items.get("entries", {})
        converted_item_entries = self.convert_to_kbmodel(item, item_entries)
        return converted_item_entries, items_data.get("_links", {})

    def convert_to_kbmodel(self, item_type, item_entries):
        """
        Converts the Desk.com items to KbExtractor items.

        :param item_type: The type of the item to convert.
        :param item_entries: All the entries to convert.
        """
        # Prepare the result list containing the converted entries
        converted_item_list = []

        # We need to have items to convert to perform some work
        if not item_entries:
            return converted_item_list

        # We need an item type to be able to convert the items
        if not item_type:
            return converted_item_list

        # If the item type contains a "/" (i.e.: /api/v2/topics/633385/articles)
        # it means we have to retrieve the last part to determine the item type
        if item_type.__contains__("/"):
            item_type = item_type.split("/")[-1]

        # Go through all the entries and convert them to the appropriate type
        if item_type == "topics":
            for topic_entry in item_entries:
                # Skip entries that are not in the support center
                if not topic_entry.get("in_support_center"):
                    continue

                # Add the topic to the result list
                topic = Topic()
                topic.name = topic_entry.get("name", "")
                topic.meta = topic_entry.get("_links", {})
                converted_item_list.append(topic)

        if item_type == "articles":
            for article_entry in item_entries:
                article = Article()
                article.topic = self.topic
                article.subject = article_entry.get("subject", "")
                article.body = article_entry.get("body", "")
                converted_item_list.append(article)

        # Return the result. It will be an emtpy list if the item type is invalid.
        return converted_item_list