class Topic(object):
    """Represents a topic.

    The meta field is specific to the source and will contain the metadata
    allowing to retrieve the articles contained within a specific topic.
    """

    def __init__(self):
        self.name = ""
        self.subtopics = []
        self.meta = {}


class Article(object):
    """Represents an article."""

    def __init__(self):
        self.topic = ""
        self.subject = ""
        self.body = ""