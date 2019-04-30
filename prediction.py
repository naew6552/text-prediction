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


    def predict(self, in_list):
        prev_word = in_list[-1]
        bigram = (prev_word, "")
        subset_list = []
        counts_list = []
        total = 0
        for b in self.b_model:
            if b[0] == prev_word:
                subset_list.append(b)
                counts_list.append(self.b_model[b])

        total = sum(counts_list)
    
        counts_list = [count/total for count in counts_list]

        if len(subset_list) == 0:
            for b in self.b_model:
                if b[0] == '<unk>':
                    subset_list.append(b)
                    counts_list.append(self.b_model[b])
            total = sum(counts_list)
            counts_list = [count/total for count in counts_list]
            choice = np.random.choice(len(subset_list), p=counts_list) 
            if subset_list[choice][1] == '<unk>':
                return self.predict('<unk>')
            return subset_list[choice][1]
        else: 
            choice = np.random.choice(len(subset_list), p=counts_list) 
            if subset_list[choice][1] == '<unk>':
                return self.predict('<unk>')
            return subset_list[choice][1]

    def completer(self, text, state):
        buffer = rl.get_line_buffer().split() 
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


    def BuildFormatted(self, file_name):
        freqs = {}
        with open(file_name, "r") as file_:
            for line in file_:
                line = line.split()
                freqs[(line[1], line[2])] = line[0]

        print(freqs)
        return freqs



def read_cli():
    print("Enter 'quit' to quit")
    while True:
        text = input()
        if text == "quit":
            break

def test_prediction(file_name, model):
    correct = 0
    incorrect = 0
    total = 0
    with open(file_name, "r") as file_:
        for line in file_:
            line = line.split()
            for i in range(0,len(line)):
                word = line[i]
                prediction = model.predict(word)
                if word == prediction:
                    correct += 1
                else:
                    incorrect += 1
                total += 1
    print(file_name)
    print(correct, incorrect, total)
    print("{}% correct, {}%incorrect".format((correct/total),(incorrect/total)))
                


model = Model("corpus/nate_corpus.txt")
rl.set_completer(model.completer)
rl.parse_and_bind('tab: complete') #set the parser to use tab complete
model.BuildFormatted("corpus/w2_.txt")
#test_prediction("corpus/test1.txt", model)
#test_prediction("corpus/test2.txt", model)
#read_cli()
