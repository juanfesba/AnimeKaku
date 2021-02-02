class Filter():

    def __init__(self, attribute, filter_type):
        self.attribute = attribute
        self.filter_type = filter_type

class Topic():

    def __init__(self, name, filters=list()):
        self.name = name
        self.filters = filters

class Category():
    
    def __init__(self, name, topics=list()):
        self.name = name
        self.topics = topics

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
characters_topic.filters = [male_filter, female_filter]

titles_topic = Topic('Titles')
titles_topic.filters = [romance_filter, drama_filter, comedy_filter, action_filter]

elements_topic = Topic('Elements')

### Anime

anime_category = Category('Anime')
anime_category.topics = [characters_topic, titles_topic, elements_topic]

### Serie

serie_category = Category('Serie')
serie_category.topics = [characters_topic, titles_topic, elements_topic]

### Movie

movie_category = Category('Movie')
movie_category.topics = [characters_topic, titles_topic, elements_topic]

### Game

game_category = Category('Game')
game_category.topics = [characters_topic, titles_topic, elements_topic] #TODO: Check if we can change this to sets.

### Traditional

traditional_category = Category('Game')
traditional_category.topics = [elements_topic]

#This are the possible 'Sekais' for players to choose.
categories = {'serie' : serie_category,
              'anime' : anime_category,
              'movie' : movie_category,
              'game' : game_category,
              'traditional' : traditional_category}

category_names = list()
for category_name in categories:
    category_names.append(category_name)