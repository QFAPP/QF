from models import Article
from models import Topic


def populate():
    """Creates the tables required by the knowledge base extractor."""
    Topic.create_table()
    Article.create_table()

# Start execution here!
if __name__ == '__main__':
    print("Starting BizQuiz population script...")
    populate()
