class Filter():

    def __init__(self, attribute, filter_type):
        self.attribute = attribute
        self.filter_type = filter_type

class Topic():

    def __init__(self, name, filters=dict()):
        self.name = name
        self.filters = filters

class Category():
    
    def __init__(self, name, default_topic, topics=dict()):
        self.name = name
        self.topics = topics
        self.default_topic = default_topic

### Filters

# Character - other info: main
male_filter = Filter('Male', 'bool')
female_filter = Filter('Female', 'bool')

# Title

romance_filter = Filter('Romance', 'bool')
drama_filter = Filter('Drama', 'bool')
comedy_filter = Filter('Comedy', 'bool')
action_filter = Filter('Action', 'bool')

# Element - other info: thing, power, event, place

### Topics - other info:

characters_topic = Topic('Characters')
characters_topic.filters = {'Male':male_filter,
                            'Female':female_filter}

titles_topic = Topic('Titles')
titles_topic.filters = {'Romance':romance_filter,
                        'Drama':drama_filter,
                        'Comedy':comedy_filter,
                        'Action':action_filter}

elements_topic = Topic('Elements')

### Anime

anime_category = Category('Anime', 'Characters')
anime_category.topics = {"Characters":characters_topic,
                        "Titles":titles_topic,
                        "Elements":elements_topic}

### Serie

serie_category = Category('Serie', 'Characters')
serie_category.topics = {"Characters":characters_topic,
                        "Titles":titles_topic,
                        "Elements":elements_topic}

### Movie

movie_category = Category('Movie', 'Characters')
movie_category.topics = {"Characters":characters_topic,
                        "Titles":titles_topic,
                        "Elements":elements_topic}

### Game

game_category = Category('Game', 'Characters')
game_category.topics = {"Characters":characters_topic,
                        "Titles":titles_topic,
                        "Elements":elements_topic}

### Traditional

traditional_category = Category('Traditional', 'Elements')
traditional_category.topics = {'Elements':elements_topic}

#This are the possible 'Sekais' for players to choose.
CATEGORIES = {'serie' : serie_category,
              'anime' : anime_category,
              'movie' : movie_category,
              'game' : game_category,
              'traditional' : traditional_category}

CATEGORY_NAMES = [category_name for category_name in CATEGORIES]