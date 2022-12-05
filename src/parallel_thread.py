from typing import TextIO
import nltk
import re
import os
import json
from time import time
from threading import Thread


PATH_DELIMITER = "/"   # Use "/" for mac/lx, "\" for Windows
PROGRAM_TYPE = "THREAD"  # Change for other types.


# ####################################################################################################################
class WordCount (Thread):
    # The following code will run as soon as the class is loaded into memory.
    # All WordCount objects will share the nltk library and the all_stopwords list.
    # nltk.download('stopwords', quiet=True)
    # nltk.download('punkt', quiet=True)
    all_stopwords = nltk.corpus.stopwords.words("english")
    all_stopwords.append("br")

    def __init__(self, filename: str):
        """Initializes the WordCount object, initializing the filename to read, and the filename where the computed
        dictionary will be saved.
        Also we keep track of the running time. """
        # super.__init__(self)

        super().__init__()
        self.__filename = filename
        self.__output = "../output/" + PROGRAM_TYPE + "_" + filename.split(PATH_DELIMITER)[-1].replace(".txt",".json")
        self.__word_count = {}
        self.__start_time = None
        self.__end_time = None

    def run(self):
        self.count_file_words()

    @property
    def filename(self):
        return self.__filename

    @property
    def output_file(self):
        return self.__output

    @property
    def runtime(self):
        if self.__start_time and self.__end_time:
            return self.__end_time - self.__start_time
        else:
            return None

    def count_file_words(self):
        """Opens the filename linked with the object and counts how many times each word appears in the file.
        Updates start and end times. Once the process is completed, the __word_count dict is saved to __output file."""
        file: TextIO
        self.__start_time = time()
        with open(self.__filename, mode="r", encoding="utf-8") as file:
            while line := file.readline():
                self.__count_line_words(line)

        with open(self.__output, mode="w") as file:
            json.dump(self.__word_count, file)
        self.__end_time = time()

    def __count_line_words(self, line : str):
        """Counts the line words, updating the object's __word_count dictionary ."""

        words = nltk.tokenize.word_tokenize(line.lower())
        words_wo_stopwords = [word for word in words if word not in self.all_stopwords and re.fullmatch("[A-Z]*[a-z]*", word)]

        for word in words_wo_stopwords:
            self.__word_count[word] = self.__word_count.get(word, 1) + 1
    pass


# ####################################################################################################################
if __name__ == "__main__":
    file_paths = "/Users/sammyel-sherif/Desktop/Lab5/word-count/"  # Location of word-count folder

    # Program Menu
    print(f"""{"=" * 80}\n{f"{PROGRAM_TYPE} PROGRAM":80}\n{"=" * 80}""")
    print(f"""{"Main Menu":80}\n{"-" * 80}""")
    print(f"""1. To run on Many Small Files""")
    print(f"""2. To run on Few Large Files""")
    print("-" * 80)
    option = int(input("Select option [1,2]>"))
    if option == 1:
        file_paths += "1.Small.Files" + PATH_DELIMITER
    elif option == 2:
        file_paths += "2.Large.Files" + PATH_DELIMITER
    else:
        print("Error - Terminating.")
        exit(1)

    # For each file: Create a WordCount(WC) object to process the file. Each WC object is stored in the word_counts list
    word_counts = []
    start_total_time = time()
    for root, directory, files in os.walk(file_paths):
        for file in files:
            if not file.endswith(".txt"):
                continue
            filename = os.path.join(root, file)
            print(f"""Processing File:{filename}""")
            wc = WordCount(filename)
            wc.start()
            # wc.join()
            # wc.count_file_words()
            word_counts.append(wc)
    for threads in word_counts:
        threads.join()
    end_total_time = time()
    # Print the results per file.
    print(">>>>>>>>> RESULTS >>>>>>>>>")
    print("-" * 120)
    for wc in word_counts:
        filename = wc.filename.split(PATH_DELIMITER)[-1]
        output = wc.output_file
        # print(f"""Running time for file "{filename}" was {wc.runtime:.3f}s. Output file is {output}.""")
    # Prints the total processing runtime.

    print("=" * 120)
    print(f"""Total Running time {end_total_time - start_total_time:.3f} sec\n""")


