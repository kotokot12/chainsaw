from hashlib import new
import pickle
import argparse
import re
import numpy as np
from random import randint as rnd

def clear_text(inp):
    inp = re.sub('[^a-zа-яё,.?0-9\s-]', ' ', inp, flags=re.IGNORECASE)
    inp = inp.replace("\n", " ")
    inp = inp.lower()
    return inp

class chain:
    def __init__(self, text, size = 3):
        self.transitions= dict()
        self.size = size
        self.text = []
        
        for subtext in text:
            current_prefix = []
            subtext = subtext.split()
            self.text = self.text + subtext[:-1]
            for word in subtext:
                if '' == re.sub('[^a-zа-яё0-9]', '', word, flags=re.IGNORECASE):
                    continue
                
                for i in range(1, min(len(current_prefix), size) + 1):
                    hashable_token = ' '.join(current_prefix[-i:])
                    if not hashable_token in self.transitions.keys():
                        self.transitions[hashable_token] = dict()
                    if not word in self.transitions[hashable_token].keys():
                        self.transitions[hashable_token][word] = 0
                    self.transitions[hashable_token][word] += 1
                    
                if (len(current_prefix) == size):
                    hashable_token = ' '.join(current_prefix)
                    if not hashable_token in self.transitions.keys():
                        self.transitions[hashable_token] = dict()
                    if not word in self.transitions[hashable_token].keys():
                        self.transitions[hashable_token][word] = 0
                    self.transitions[hashable_token][word] += 1
                    
                    current_prefix = current_prefix[1:] + [word]
                else:
                    current_prefix.append(word)
        #print(self.transitions)
    def get(self, prefix, length):
        prefix = prefix.split()
        ans = prefix
        prefix = prefix[-min(len(prefix), self.size):]
        for i in range(length):
            while True:
                if (prefix == []):
                    prefix = [self.text[rnd(0, len(self.text) - 1)]]
                cur = ' '.join(prefix)
                #print(prefix)
                if (cur in self.transitions.keys()):
                    if (len(prefix) == self.size and rnd(0, 4) == 5):
                        prefix = prefix[1:]
                        continue
                    
                    tmp = np.array(list(self.transitions[cur].values()))
                    new_word = np.random.choice(list(self.transitions[cur].keys()), p=tmp/tmp.sum())
                    ans.append(new_word)
                    
                    if (len(prefix) == self.size):
                        prefix = prefix[1:]
                        prefix.append(new_word)
                    else:
                        prefix.append(new_word)
                        
                    break
                else:
                    prefix = prefix[1:]
        
        return  ans

def load(path):
    with open(path, "rb") as f:
        return pickle.load(f)

def save(model, path):
    with open(path, "wb") as f:
        pickle.dump(model, f)

def main():
    parser = argparse.ArgumentParser(description="Generates text using Markov chains. Use --help for command information")
    parser.add_argument("--model", type=str, help="Path to model(required!!!)", required=True)
    parser.add_argument("--prefix", type=str, help="Prefix of generated text(default = '')", default='')
    parser.add_argument("--length", type=int, help="Length of generated text(count of words, default = 0)", default=0)
    arguments = parser.parse_args()
    
    if arguments.length < 0:
        print("Error. Negative length")
        exit(0)
    
    try:
        model = load(arguments.model)
    except:
        print("Сan't load it using this path")
    
    print(*model.get(clear_text(arguments.prefix), arguments.length))
    
if __name__ == '__main__':
    main()