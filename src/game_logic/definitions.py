class Filter():

    def __init__(self, attribute, attribute_type):
        self.attribute = attribute
        self.atrribute_type = attribute_type

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
kids_filter = Filter('Kids', 'bool')

# Element - other info: thing, power, event, place

### Topics - other info:

characters_topic = Topic('Characters')
characters_topic.filters = [male_filter, female_filter]

title_topic = Topic('Title')
title_topic.filters = [romance_filter, drama_filter, comedy_filter, kids_filter]

element_topic = Topic('Element')

### Anime

anime_category = Category('Anime')
anime_category.topics = [characters_topic, title_topic, element_topic]

### Serie

serie_category = Category('Serie')
serie_category.topics = [characters_topic, title_topic, element_topic]

### Movie

movie_category = Category('Movie')
movie_category.topics = [characters_topic, title_topic, element_topic]

### Game

game_category = Category('Game')
game_category.topics = [characters_topic, title_topic, element_topic]

### Traditional

traditional_category = Category('Game')
traditional_category.topics = [element_topic]

#This are the possible 'Sekais' for players to choose.
categories = {'serie' : serie_category,
              'anime' : anime_category,
              'movie' : movie_category,
              'game' : game_category,
              'traditional' : traditional_category}

category_names = list()
for category_name in categories:
    category_names.append(category_name)