import random
import json
import nltk
from nltk.corpus import wordnet as wn
from lemminflect import getInflection


def create_data():
    """One-time function to create json files containing word lists"""

    noun_synsets = list(wn.all_synsets("n"))
    verb_synsets = list(wn.all_synsets("v"))
    adjective_synsets = list(wn.all_synsets("a"))

    nouns = []
    verbs = []
    conjugated_verbs = []
    adjectives = []

    for noun_synset in noun_synsets:
        for lemma in noun_synset.lemmas():
            noun = lemma.name()
            if "_" not in noun:
                nouns.append(noun)

    for verb_synset in verb_synsets:
        for lemma in verb_synset.lemmas():
            verbs.append(lemma.name())

    for verb in verbs:
        conjugated_verb = "".join(getInflection(verb, tag="VBG"))
        if "_" not in conjugated_verb:
            conjugated_verbs.append(conjugated_verb)

    for adjective_synset in adjective_synsets:
        for lemma in adjective_synset.lemmas():
            adjective = lemma.name()
            if "_" not in adjective:
                adjectives.append(adjective)

    with open("utils/data/nouns.json", "w") as file:
        json.dump(nouns, file, indent=2)

    with open("utils/data/verbs.json", "w") as file:
        json.dump(conjugated_verbs, file, indent=2)

    with open("utils/data/adjectives.json", "w") as file:
        json.dump(adjectives, file, indent=2)


class Generator:
    """Random generator for creating Event Titles"""

    def __init__(self):
        with open("utils/data/nouns.json", "r") as file:
            self.nouns = json.load(file)

        with open("utils/data/verbs.json", "r") as file:
            self.verbs = json.load(file)

        with open("utils/data/adjectives.json", "r") as file:
            self.adjectives = json.load(file)

    def generate_operation(self):

        def random_noun():
            noun_choice = random.choice(self.nouns).title()
            return noun_choice

        def random_verb():
            verb_choice = random.choice(self.verbs).title()
            return verb_choice

        def random_adjective():
            adj_choice = random.choice(self.adjectives).title()
            return adj_choice

        format_1 = "Operation " + random_verb() + " " + random_noun()
        format_2 = "Operation " + random_noun()
        format_3 = "Operation " + random_adjective() + " " + random_noun()

        formats = [format_1, format_2, format_3]
        choice = random.choice(formats)
        return choice















