import argparse
import pickle
import generate
import re
import os

def clear_text(inp):
    inp = re.sub('[^a-zа-яё,.?0-9\s-]', ' ', inp, flags=re.IGNORECASE)
    inp = inp.replace("\n", " ")
    inp = inp.lower()
    #print(inp)
    return inp

parser = argparse.ArgumentParser(description="Generates text using Markov chains. Use --help for command information")
parser.add_argument("--input-dir", type=str, help="Path to input folder(do not specify for console input). Only txt files are considered using UTF-8 encoding")
parser.add_argument("--model", type=str, help="Еhe path by which the model will be saved", default="./out_model.mdl")

arguments = parser.parse_args()
input_dir = arguments.input_dir
model = arguments.model

if (input_dir == None):
    inp = input("Enter text: ")
    inp = [clear_text(inp)]
else:
    inp = []
    for file in os.listdir(input_dir):
        path = f"{input_dir}\{file}"
        if (os.path.isfile(path)):
            if not(len(path) > 3 and path[-4:] == '.txt'):
                print(f"File {path} skipped. Not txt")
                continue
            
            try:
                with open(path, "r", encoding="utf-8") as f:
                    inp.append(clear_text(f.read()).replace("\n", " "))
            except UnicodeDecodeError:
                print(f"File '{path}' skipped. Unicode error")

try:
    with open(model, "wb") as f:
        pickle.dump(":)", f)
except:
    print("Сan't save it using this path")
    print("Your path is incorrect. Use correct path(example: outfolder/model.mdl)")
    exit(0)

result = generate.chain(inp)

with open(model, "wb") as f:
    pickle.dump(result, f)