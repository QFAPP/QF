"""
Module performing operations on desk.com.
"""

import os
import os.path
import requests

from .models import Article, Topic

class Pydesk(object):
    """
    Provides operations to retrieve and save data from desk.com.
    """

    def __init__(self, subdomain, user, password):
        self.subdomain = subdomain
        self.user = user
        self.password = password
        self.base_url = "https://" + self.subdomain + ".desk.com"

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
        url = self.base_url + href + "?per_page=1"

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
        return embedded_items.get("entries"), items_data.get("_links")

    @staticmethod
    def next_page_url(metadata):
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

    def save_topics(self):
        """
        Saves all the topics entries.
        """
        retrieved_topics = self.retrieve_items("topics")
        topic_entries = retrieved_topics[0]
        topic_meta = retrieved_topics[1]
        self.save_all_topic_entries(topic_entries, topic_meta)

    def save_all_topic_entries(self, topic_entries, topic_meta):
        """
        Saves all topics and their entries on disk.

        :param topic_entries The topic entries to parse
        :param topic_meta The topic meta data, used to find the next page if any
        """
        # If there is no data, there is nothing to do
        if not topic_entries:
            return

        # Save the current list
        for topic_entry in topic_entries:
            self.save_topics_to_db(topic_entry)

        # Check whether there are more entries within this topic
        next_page_url = self.next_page_url(topic_meta)
        if not next_page_url:
            return

        # Retrieve the data of the next page
        next_topic_list, next_topic_meta = self.retrieve_items(next_page_url)
        self.save_all_topic_entries(next_topic_list, next_topic_meta)

    def save_topic_articles_to_file(self, topic_entry):
        """
        Saves a topic entry and its content on disk.

        :param topic_entry: the topic entry to save on disk
        """
        # If there is no data there is nothing to do
        if not topic_entry:
            return

        # Skip entries that are not in the support center
        if not topic_entry.get("in_support_center"):
            return

        # The name of the topic will be the name of the folder to create
        topic_name = topic_entry.get("name")

        # The name of the topic is mandatory
        if not topic_name:
            print('Corrupted entry.')
            return

        # Create the folder if it does not exist
        if not os.path.exists(topic_name):
            os.mkdir(topic_name)

        # Retrieve the link pointing to to all articles in this topic
        href = topic_entry.get("_links", {}).get("articles", {}).get("href")

        # Leave if there is no link pointing to the articles
        if not href:
            print('There is no URL to retrieve the articles.')
            return

        # Retrieve all the articles of a topic
        articles_list = self.retrieve_items(href)

        # Go through all the articles in this topic
        Pydesk.save_articles(topic_name, articles_list)

    def save_topics_to_db(self, topic_entry):
        """
        Saves a topic entry and its content on disk.

        :param topic_entry: the topic entry to save on disk
        """
        # If there is no data there is nothing to do
        if not topic_entry:
            return

        # Skip entries that are not in the support center
        if not topic_entry.get("in_support_center"):
            return

        # The name of the topic will be the name of the folder to create
        topic_name = topic_entry.get("name")

        # The name of the topic is mandatory
        if not topic_name:
            print('Corrupted entry. The name is missing.')
            return

        # Retrieve the link pointing to to all articles in this topic
        href = topic_entry.get("_links", {}).get("articles", {}).get("href")

        # Leave if there is no link pointing to the articles
        if not href:
            print('There is no URL to retrieve the articles.')
            return

        # Retrieve all the articles of a topic
        article_list = self.retrieve_items(href)

        while True:
            # Create the articles
            Pydesk.create_articles(topic_name, article_list[0])

            # Retrieve the items of the next page if any
            next_page = self.next_page_url(article_list[1])
            if not next_page:
                break
            article_list = self.retrieve_items(next_page)

    @staticmethod
    def create_articles(topic_name, article_entry_list):
        """
        Creates the article entries in the database.

        :param topic_name The name of the topic
        :param article_entry_list The list of entries of this topic
        """

        try:
            # Try to retrieve the topic to see if it exists already
            topic = Topic.get(Topic.name == topic_name)
        except Topic.DoesNotExist:
            # Create the topic if it does not exist
            topic = Topic.create(name=topic_name)

        # Go through all the articles in this topic
        for article_entry in article_entry_list:
            article_name = article_entry.get("subject")

            # Print the name (for debugging purpose)
            print(article_name)

            # Create the files with the content
            # Overwrite existing files
            try:
                article = Article.create(topic=topic,
                                         subject=article_name,
                                         body=article_entry.get("body"))
            except Article.DoesNotExist:
                pass

    @staticmethod
    def save_articles(topic_name, article_entry_list):
        """
        Saves a list of articles into a folder having the name of the topic
        where they come from.

        :param topic_name The name of the topic
        :param article_entry_list The articles to save
        """
        # Create the topic in the db if it does not exist
        topic_db = Topic.create(name=topic_name)

         # Go through all the articles in this topic
        for article_entry in article_entry_list:
            article_name = article_entry.get("subject")
            print(article_name)

            # Create the files with the content
            # Overwrite existing files
            file_name = topic_name + '/' + article_name
            with open(file_name, mode='w', encoding='utf-8') as article_file:
                article_file.write(article_entry("body"))
