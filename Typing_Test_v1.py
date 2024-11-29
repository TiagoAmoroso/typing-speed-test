import time
import keyboard
from essential_generators import DocumentGenerator
import random
import os
import pygame


#IMPROVEMENTS:
#Tidy weird punctuation out of sentences in essential generators
#Create a GUI
#Allow test metrics and stats to be toggled
#Use different generator types to generate different text types for user to choose from
#Time taken to type each word 


#COMPLETE
#Create class to hold sentence data 
#Remove additional spaces from end of user sentence
#Remove additional spaces from within user_text
#Random selection of words/sentences
#Allow user to restart
#Display WPM
#Display wrong words
#Use OS to ensure path accuracy

"""
gen = DocumentGenerator()

#Generating caches to speed up subsequent calls to generate words or sentences
gen.init_word_cache(500)
gen.init_sentence_cache(50)
"""

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))

#Text is required in string format
class Text:
  def __init__(self, text_string):
    self.string = text_string.rstrip()
    self.words = self.string.split()




class Game:
  def __init__(self):
    self.all_words = [] 
    self.user_text = Text("")
    self.computer_text = Text("")
    self.correct_words = []
    self.incorrect_words = []
    self.accuracy = 0
    self.WPM = 0
    self.start_time = time.time()
    self.finish_time = time.time()
    self.words_file_path = os.path.join(THIS_FOLDER, "data/words.txt")


  def reset(self):
    self.__init__(self)


  def generate_word_list(self, file_path):
    with open(file_path) as f:
      words = f.read().splitlines()

    return words


  def generate_text(self, text_length):
    #gen.sentence()

    words = self.all_words
    word_count = len(words)
    text = []
  
    for i in range(text_length):
      random_index = random.randint(0, word_count)
      text.append(words[random_index])

    text = Text(' '.join(str(x) for x in text))

    return text


  def start_timer(self):
    self.start_time = time.time()


  def stop_timer(self):
    self.finish_time = time.time()


  def get_time_passed(self):
    time_passed = self.finish_time - self.start_time

    return time_passed


  def request_user_text(self):
    self.user_text = Text(input("Type: "))


  def compare_texts(self):
    word_count = len(self.user_text.words)

    for i in range(word_count):
      if i < word_count:
        computer_word = self.computer_text.words[i]
        user_word = self.user_text.words[i]
    
        #word comparison
        if computer_word == user_word:
          self.correct_words.append(user_word)
        else:
          self.incorrect_words.append([computer_word, user_word])
          
      else:
        break


  def calculate_statistics(self):
    total_words_typed = len(self.correct_words) + len(self.incorrect_words)
    
    if total_words_typed > 0:
      self.accuracy = round(len(self.correct_words) / total_words_typed * 100, 2)
      self.WPM = round(len(self.correct_words) * (60/self.get_time_passed()))

    else:
      self.accuracy = 0
      self.WPM = 0


  def display_statistics(self):
    print("Accuracy: ", str(self.accuracy) + "%")
    print("Time: ", round(self.get_time_passed(), 2), "seconds")
    print("WPM: ", self.WPM)
    print("Words correct: ", len(self.correct_words))
    print("Words incorrect: ", len(self.incorrect_words))
    print("Mispelled words: ", self.incorrect_words)
      

if __name__ == "__main__":

  while True:
    game = Game()

    game.all_words = game.generate_word_list(game.words_file_path)
    game.computer_text = game.generate_text(10)

    input("Press enter to begin...")
    
    print("\n\n\n")
    print(game.computer_text.string)
    print("\n")

    game.start_timer()
    
    game.request_user_text()

    game.stop_timer()

    game.compare_texts()

    game.calculate_statistics()

    print("\n")
    game.display_statistics()

    print("\n")

