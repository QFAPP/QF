import argparse
import json

from kbextractor.pydesk import Pydesk


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Export you knowledge base.")
    parser.add_argument("--subdomain", dest="subdomain", action="store",
                        help="Your subdomain")
    parser.add_argument("--username", dest="username", action="store",
                        help="Your username")
    parser.add_argument("--password", dest="password", action="store",
                        help="Your password")

    args = parser.parse_args()
    print(args.subdomain)
    print(args.username)
    print(args.password)

    desk = Pydesk(args.subdomain,args.username,args.password)
    desk.save_topics()
    #topic_entries = retrieved_topics[0]
    #topic_meta = retrieved_topics[1]
    #desk.save_all_topic_entries(topic_entries, topic_meta)
    #desk.save_topics_to_db()

    # Loads the articles from a file
    # article_file = open('articles.json', encoding='utf-8')
    # article_file_content = article_file.read()
    # article_content = json.loads(article_file_content)
    # article_entry_list = article_content["_embedded"]["entries"]
    #
    # my_topic = Topic.create(name="Test")
    # Pydesk.create_articles(my_topic, article_entry_list)
