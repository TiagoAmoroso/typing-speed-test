import time
from essential_generators import DocumentGenerator
import random
import os
import GUI as gui
from GUI import pygame
from GUI import Text


#IMPROVEMENTS:
#Tidy weird punctuation out of sentences in essential generators
#Allow test metrics and stats to be toggled
#Use different generator types to generate different text types for user to choose from
#Time taken to type each word
#Implement fixed line count for static GUI text boxes
#reposition restart button depending on position of stats box once filled with text
#Find labels by name instead of by index

#Toggle stats on results page

#COMPLETE
#Create class to hold sentence data 
#Remove additional spaces from end of user sentence
#Remove additional spaces from within user_text
#Random selection of words/sentences
#Allow user to restart
#Display WPM
#Display wrong words
#Use OS to ensure path accuracy
#Create a GUI
#Display stats on GUI
#Restart button
#Fix issue when entering no user text and just pressing enter

"""
gen = DocumentGenerator()

#Generating caches to speed up subsequent calls to generate words or sentences
gen.init_word_cache(500)
gen.init_sentence_cache(50)
"""

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))



class Game:
    def __init__(self, computer_text_box, user_text_box):
        self.all_words = [] 
        self.user_text = Text("", user_text_box)
        self.user_text_box = user_text_box
        self.computer_text = Text("", computer_text_box)
        self.computer_text_box = computer_text_box
        self.correct_words = []
        self.incorrect_words = []
        self.accuracy = 0
        self.wpm = 0
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

        text = Text(' '.join(str(x) for x in text), self.computer_text_box)

        return text


    def start_timer(self):
        self.start_time = time.time()


    def stop_timer(self):
        self.finish_time = time.time()


    def get_time_passed(self):
        time_passed = self.finish_time - self.start_time

        return time_passed


    def update_user_text(self):
        self.user_text.string = self.user_text_box.text.string
        self.user_text.update_words()


    def compare_texts(self):
        self.correct_words = []
        self.incorrect_words = []

        #Cleaning text
        self.user_text.string = self.user_text.string.rstrip()
        self.user_text.update_words()

        word_count = len(self.user_text.words)

        for i in range(word_count):
            #Ensuring that at least one character has been entered
            if self.user_text.words[i] != "":
                computer_word = self.computer_text.words[i]
                user_word = self.user_text.words[i]
            
                #word comparison
                if computer_word == user_word:
                    self.correct_words.append(user_word)
                else:
                    self.incorrect_words.append([computer_word, user_word])
            

    def calculate_statistics(self):
        self.compare_texts()

        total_words_typed = len(self.correct_words) + len(self.incorrect_words)
        
        if total_words_typed > 0:
            self.accuracy = round(len(self.correct_words) / total_words_typed * 100, 2)
            self.wpm = round(len(self.correct_words) * (60/self.get_time_passed()))

        else:
            self.accuracy = 0
            self.wpm = 0


    def get_statistics(self):
        #Ensures stats are up to date
        self.calculate_statistics()

        #retruning the up to date stats
        return [self.accuracy, self.get_time_passed(), self.wpm, len(self.correct_words), len(self.incorrect_words), self.incorrect_words]


    def display_statistics(self):
        print("Accuracy: ", str(self.accuracy) + "%")
        print("Time: ", round(self.get_time_passed(), 2), "seconds")
        print("WPM: ", self.wpm)
        print("Words correct: ", len(self.correct_words))
        print("Words incorrect: ", len(self.incorrect_words))
        print("Mispelled words: ", self.incorrect_words)
        

if __name__ == "__main__":

    #Creating required pygame variables
    clock = gui.pygame.time.Clock()

    #Creating GUI window
    window = gui.Window()


    game_running = True
    game_screen = True
    results_screen = False

    while game_running:
        #Creating on screen labels
        #GAME SCREEN
        text_box_rect = pygame.Rect(50, 50, 700, 0)
        computer_box = gui.TextBox(window, text_box_rect, 20, 20, name = "computer text box")

        text_box_rect = pygame.Rect(50, 350, 700, 0)
        user_box = gui.TextBox(window, text_box_rect, 9, 9, name = "user text box", clickable = True, border_thickness = 0)

        game_screen_labels = [computer_box, user_box]


        #RESULTS SCREEN
        text_box_rect = pygame.Rect(50, 50, 450, 0)
        results_box = gui.TextBox(window, text_box_rect, 20, 20, name = "results text box")

        button_rect = pygame.Rect(50, 350, 200, 100)
        restart_button = gui.Button(window, button_rect, 20, 20, name = "restart button", title = "Restart")
        
        toggle_rect = pygame.Rect(350, 350, 200, 100)
        toggle = gui.Toggle(window, toggle_rect)

        results_screen_labels = [results_box, restart_button, toggle]

        #Passing game scrren labels to GUI window as we begin on the game screen
        window.labels = game_screen_labels

        #Initialising game
        game = Game(computer_box, user_box)

        #Generating game data
        game.all_words = game.generate_word_list(game.words_file_path)
        game.computer_text = game.generate_text(10)

        #Passing game data to GUI window
        window.labels[0].text.string = game.computer_text.string

        game.start_timer()
        while game_screen:
            #Handling events
            window.handle_events()

            #Drawing all content
            window.draw()

            #Check docs
            pygame.display.flip()
            clock.tick(60)

            #Updating the game with data from the GUI
            game.update_user_text()

            #Screen logic

            #Stopping the game
            if window.labels[1].text.string_in_text("\n"):
                #Removing \n so stats can be calculated accurately
                game.user_text.string = game.user_text.string.strip("\n")
                game.user_text.update_words()

                game.stop_timer()
                game_screen = False

                results_screen = True

                #print(game.user_text.words)
                stats = game.get_statistics()
                accuracy, time_passed, wpm = str(stats[0]) + "%", str(round(stats[1], 2)) + " seconds", str(stats[2])
                words_correct, words_incorrect, mispelled_words = str(stats[3]), str(stats[4]), str(stats[5])

                #"\n " act as a line break in text box line drawing
                results_box.text.string = "accuracy: " + accuracy + "\n time: " + time_passed + "\n wpm: " + wpm + "\n words correct: "
                results_box.text.string += words_correct + "\n words incorrect: " + words_incorrect + "\n mispelled words: " + mispelled_words

                window.labels = results_screen_labels

        while results_screen:
            #Handling events
            window.handle_events()

            #Drawing all content
            window.draw()

            #Check docs
            pygame.display.flip()
            clock.tick(60)

            #Screen logic

            if window.labels[1].pressed:
                results_screen = False
                game_screen = True

