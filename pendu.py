import inspect
import random
from math import floor

from flask import session

# niveau de difficulté
# mots avec plusieurs lettre
# verifier si les lettres sont dans l'alphabet
# chosse underscore show duplicated letter
fr_words = [
    "PETIT CHAT", "GRAND ELEPHANT", "BONBON SUCRE", "SALLE DE BAIN",
    "MAISON BLANCHE", "BALLON ROUGE", "TASSE DE THE", "CITRON VERT",
    "VOITURE BLEUE", "POMME DE TERRE", "JUMELLE IDENTIQUE", "TABLE RONDE",
    "BALLE DE TENNIS", "DOUDOU DOUX", "CASQUE AUDIO", "ROULETTE EN FER",
    "BEBE ADORABLE", "SCOOTER NOIR", "FENETRE OUVERTE", "CASSEROLE VIDE",
    "SERVIETTE MOELLEUSE", "CHAUD ET FROID", "PAPIER CADEAU",
    "CHAT DE RUE", "PUZZLE COMPLET", "PLAGE DE SABLE", "SOLEIL BRULANT",
    "BULLE DE SAVON", "GOURDE METALLIQUE", "ROUTE LONGUE",
    "ROUE LIBRE", "MONTAGNE ENNEIGEE", "BOUTEILLE D'EAU",
    "SALLE A MANGER", "MONTRE D'OR", "PLUME DE PAON", "SOUPE A L'OIGNON"
]
en_words = ["DOG", "CAT", "HOUSE", "TREE", "CAR", "PLANE", "BOOK", "SCHOOL", "MOUNTAIN", "BEACH", "BICYCLE", "COMPUTER",
            "CUP", "SKY", "FLOWER", "FISH", "PHONE", "STAR", "APPLE", "CLOCK", "MOON", "CACTUS", "CHOCOLATE",
            "BUTTERFLY", "HORSE", "BALLOON", "WINDOW", "HEART", "CAKE", "ROBOT", "CAMERA", "BACKPACK", "PANTS",
            "PENCIL", "DUCK", "PAINTING", "SNAIL", "DOLL", "KEY", "MONSTER"]


class Pendu:
    def __init__(self, difficult):
        self.fr_words = fr_words
        self.en_words = en_words
        self.difficult = difficult
        self.secret_word = ""
        if self.difficult < 1 and self.difficult > 3:
            self.difficult = 3

    def reset(self):
        session['death_count'] = 0
        session['letter_said'] = []
        session['done'] = False
        self.choose_fr_word()
        print(self.secret_word)
        session['word_to_render'] = self.to_underscore_word()
        print(session['word_to_render'])

    def to_underscore_word(self):
        # 1=> max 3 letter
        # 2=> 1 letter
        # 3=> 0 letter

        len_of_word = len(self.secret_word)
        liste = ['_' if self.secret_word[k] != ' ' else ' ' for k in range(len_of_word)]

        if self.difficult == 3:
            return "".join(liste)

        if len_of_word == 3 or len_of_word == 4 or self.difficult == 2:
            # one letter shower
            ints_letter =  self.get_occurs(self.secret_word,1)
            if (len(ints_letter)==1):
                 liste[ints_letter[0]] = self.secret_word[ints_letter[0]]
            return "".join(liste)

        if self.difficult == 1:
            ints_letter = self.get_occurs(self.secret_word, floor(2 / 5 * len_of_word))
            for int in ints_letter:
                liste[int] = self.secret_word[int]
            return "".join(liste)

    def get_occurs(self, word, nb_indexs_wanted):

        print(nb_indexs_wanted)
        indexs = []
        letters = []
        enought_values = False

        while not enought_values:

            randomint = random.randint(0,len(word)-1)
            min_letter = word[randomint]
            min_count = word.count(word[randomint])


            for letter in word:
                if letter not in letters and letter != " ":
                    occurs = word.count(letter)
                    if occurs < min_count:
                        min_count = occurs
                        min_letter = letter
            if (min_count + len(indexs) <= floor(len(word) / 2) and min_count + len(indexs) <= nb_indexs_wanted):

                for i in range(len(word)):
                    if word[i] == min_letter:
                        indexs.append(i)
                        letters.append(word[i])

            if len(indexs) == nb_indexs_wanted or min_count + len(indexs) > nb_indexs_wanted:

                enought_values = True

        return indexs

    def choose_fr_word(self):
        # Choose a random word from the list
        random_choice = random.choice(fr_words)

        self.secret_word = random_choice

        return

    def choose_en_word(self):
        # Choose a random word from the list
        random_choice = random.choice(en_words)
        self.secret_word = random_choice

    def get_stats(self):
        if not "death_count" in session:
            self.reset()
        print(self.secret_word)
        print(session['letter_said'])
        if session['death_count'] == 8:
            self.discover_word_when_loose()
        return session['word_to_render'], session['letter_said'], session['death_count'],  session['done']

    def run_pendu(self, given_letter) -> (bool, str):
        #when many letter in input it's hit or miss
        if type(given_letter) == list:

            session['letter_said'] += (given_letter)
            session['letter_said'].sort()
            for letter in given_letter :
                print(letter)
                if letter not in self.secret_word:
                    session['death_count'] = 8
                    return False ,""
                    # get states will be call to render missed letter
            #good write as done
            session['word_to_render']=self.secret_word
            session['done']=True
            return True ,""


        #when reload => don't calculate again
        if session['word_to_render'] == self.secret_word:
            return True, ""


        print("given wletter",given_letter)
        session['letter_said'].append(given_letter)
        session['letter_said'].sort()

        # verify if the letter is in
        print("given letter in word ?", given_letter in self.secret_word)
        if given_letter in self.secret_word:
            self.replace_letter(given_letter)
            if session['word_to_render'] == self.secret_word:
                session['done'] = True
                return True, ""
            return False, "Good letter !"
        else:
            session['death_count'] = session['death_count'] + 1
            return False, "Bad Letter !"

    def replace_letter(self, letter):
        word_list = list(session['word_to_render'])
        for k in range(len(self.secret_word)):
            if letter == self.secret_word[k]:
                # transform to list to replace index and return word

                word_list[k] = letter

        session['word_to_render'] = "".join(word_list)
    def discover_word_when_loose(self):
            word_list = list(session['word_to_render'])
            for k in range(len(self.secret_word)):
                if word_list[k] == "_":
                    word_list[k] = self.secret_word[k].lower()

            session['word_to_render'] = "".join(word_list)
