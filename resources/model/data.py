import glob
import os
import re
import string
import torch
import unicodedata

from statistics import mean

all_letters = string.ascii_letters + " .,;'-!?"
label_dict = {}
label_counter = 0

def findFiles(path): return glob.glob(path)

# Turn a Unicode string to plain ASCII, thanks to http://stackoverflow.com/a/518232/2809427
def unicodeToAscii(s):
    return ''.join(
        c for c in unicodedata.normalize('NFD', s)
        if unicodedata.category(c) != 'Mn'
        and c in all_letters
    )

# Read a file and split into lines
def readLines(filename):
    lines = open(filename).read().strip().split('\n')
    return [unicodeToAscii(line) for line in lines]

# Build the category_lines dictionary, a list of lines per category
category_lines = {}
all_categories = {0: 'not spam', 1: 'spam'}

scriptpath = os.path.abspath(__file__)
scriptdir = os.path.dirname(scriptpath)
filename = os.path.join(scriptdir, 'spambase.data')

with open(filename) as file:
    out = file.readlines()
    for line in out:
        label = all_categories[int(line.rstrip('\n')[-1])]
        cur = category_lines.pop(label, [])
        line = list(map(float, line.rstrip('\n')[:(len(line)-3)].split(',')))
        cur.append(line)
        category_lines[label]=(cur)
        # print(cur)
        # print(f'cur line sum is {sum(cur)}')
    print(f"num spam {len(category_lines['spam'])} num non spam \
        {len(category_lines['not spam'])}") #line[:len(line) - 1])



n_feats = len(category_lines['not spam'][0])
#print(f'number feats {n_feats}')
n_categories = len(all_categories)

filename = os.path.join(scriptdir, 'spambase.names')
# process label file, generating a dictionary mapping each word to its index
with open(filename) as file:
    strings_of_interest = set(['word_freq_', 'char_freq_'])
    for line in file.readlines():
        prefix = line[:10]
        if prefix in strings_of_interest:
            #print(line)
            #print(line[10:])
            out_list = re.split(':[\s]+', line[10:])
            #print(out_list)
            label_dict[out_list[0]] = label_counter
            label_counter += 1

label_list = list(label_dict.keys())
#print(label_list)

# Find letter index from all_letters, e.g. "a" = 0
def wordToIndex(letter):
    return all_letters.find(letter)

# Turn a line into a <line_length x 1 x n_letters>,
# or an array of one-hot letter vectors
def lineToTensor(line):
    tensor = torch.tensor(line)
    #print(f'line is {line}, tensor is {tensor}')
    return tensor

def get_uppercase_metrics_from_string(s):
    # construct a list of all the uppercase segments in your string
    list_of_uppercase_runs = re.findall(r"[A-Z]+", s)

    # find out what the longest string is in your list


    run_lengths = list(map(len, list_of_uppercase_runs))
    longest_string = max(run_lengths, default=0.)
    # for run in list_of_uppercase_runs:
    #     running_total += len(run)

    if len(run_lengths) > 0:
        avg_length = mean(run_lengths)
    else:
        avg_length = 0.

    # return the length of this string to the user
    return [avg_length, longest_string, avg_length]

def processString(line):
    list_of_strings = re.split('[\s]+', line)
    word_accumulator = {}
    total_word_counter = total_char_counter = 0.
    for word in list_of_strings:
        # cap_letters = filter(lambda x: x.isupper(), word)
        if word not in word_accumulator:
            word_accumulator[word] = 1.
        else:
            word_accumulator[word] += 1.
        if len(word) == 1:
            total_char_counter += 1.
        else:
            total_word_counter += 1.
    out = [0. for i in range(54)]
    seen_words = list(word_accumulator.keys())
    for word in seen_words:
        if word not in label_dict.keys():
            continue
        if len(word) > 1:
            #print(label_dict)
            out[label_dict[word]]= ((word_accumulator[word]/total_word_counter)*100.)
        else:
            out[label_dict[word]]= ((word_accumulator[word]/total_char_counter)*100.)
    out += get_uppercase_metrics_from_string(line)
    print(out)
    return out
