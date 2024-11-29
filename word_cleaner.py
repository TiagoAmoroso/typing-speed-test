def clean_words(words):
  words_to_remove = []

  #Finding words to remove
  for word in words:
  
    if word.isupper() or (not word.isupper() and not word.islower()):
      words_to_remove.append(word)

    elif len(word) > 7:
      words_to_remove.append(word
                            )
  #Removing words
  for word in words_to_remove:
    words.remove(word)
    
  return words

def write_list_to_file(my_list, file_path):
  with open(file_path, "w") as f:
    for item in my_list:
      f.write("{i}\n".format(i = item))


def JSONify_file(src_file_path, destination_file_path):
    pass
      


#Making list of words
with open("data/words_complete.txt") as f:
  words = f.read().splitlines()

#Cleaning word list
clean_words = clean_words(words)

#Writing clean list to file
write_list_to_file(clean_words, "data/words.txt")