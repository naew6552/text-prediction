'''
prediction.py
Written by: Nate Ewan

This is a python program that will fulfill a couple functions. It can be used as
a command line utility to generate sentences, take in corpuses, and run accuracy
tests on a langauge prediction model. It can also be run as a CLI utility, where
when using tab-complete, the model will try to predict the next world you will
type.

CLI Arguments:
    - t
    - c

'''
import readline as rl
from collections import defaultdict
from collections import Counter
import numpy as np

class Model:


    def __init__(self, file_name):
        self.b_model = self.buildBigram(file_name)


    def predict(self, buffer):
        prev_word = buffer[-1]
        bigram = (prev_word, "")
        subset_list = []
        counts_list = []
        total = 0
        for b in self.b_model:
            if b[0] == bigram[0]:
                subset_list.append(b)
                counts_list.append(bigram_model[b])

        total = sum(counts_list)
    
        counts_list = [count/total for count in counts_list]

        choice = np.random.choice(len(subset_list), p=counts_list)
        #sentence += " " + subset_list[choice][1]

        #bigram = (subset_list[choice][1], subset_list[choice][1])
        return subset_list[choice][1]

    def completer(self, text, state):
        ## TODO: Get buffer into list, and use last word to pass to predict
        buffer = rl.get_line_buffer()
        print(buffer)
        prediction = self.predict(buffer)
        results = [prediction,None]
        return results[state]


    def buildBigram(self, file_name):
        """
        inputs:
            file_name: The name of the file from which the corpus data is read.

        outputs:
            freqs: A dictionary containing each unique bigram and how often it
            appears in the corpus.

        This function takens in a file name of a corpus, which is read in line by
        line and split into tokens. As with buildUnigram, we are removing words with
        a frequency less than one and replacing those words with <unk>

        This function returns a dictionary of every unique bigram being the key, and
        the frequency of that bigram within the corpus using the Counter data type.
        """
        corpus = []
        with open(file_name, "r") as file_:
            for line in file_:
                corpus += line.split()
        freqs = Counter(corpus)
        counter = 0
        del_list = []
        for token in freqs:
            if freqs[token] < 2:
                counter += 1
                del_list.append(token)

        for i in range(0, len(corpus)):
            if corpus[i] in del_list:
                corpus[i] = '<unk>'

        bigram_corpus = []
        for i in range(1, len(corpus)):
            bigram_corpus.append((corpus[i-1], corpus[i]))

        freqs = Counter(bigram_corpus)
        return freqs



def read_cli():
    print("Enter 'quit' to quit")
    while True:
        text = input()
        if text == "quit":
            break


model = Model("corpus.txt")
rl.set_completer(model.completer)
rl.parse_and_bind('tab: complete') #set the parser to use tab complete
read_cli()
