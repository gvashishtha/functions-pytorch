from .model import *
from .data import *
import os
import sys

scriptpath = os.path.abspath(__file__)
scriptdir = os.path.dirname(scriptpath)
filename = os.path.join(scriptdir, 'spam-rnn-classification.pt')

n_hidden = 128
rnn = RNN(n_feats, n_hidden, n_categories)
rnn.load_state_dict(torch.load(filename))


# Just return an output given a line
def evaluate(line_tensor):
    hidden = rnn.initHidden()

    output, hidden = rnn(torch.unsqueeze(line_tensor, 0), hidden)

    return output

def predict(line):
    output = evaluate(Variable(lineToTensor(processString(line))))

    # Get top N categories
    topv, topi = output.data.topk(1, 1, True)
    predictions = []

    print(f'{output}, {topv}, {topi}')
    for i in range(1):
        value = topv[0][i]
        category_index = topi[0][i]
        print('(%.2f) %s' % (value, all_categories[category_index.item()]))
        predictions.append([value, all_categories[category_index.item()]])

    return predictions

if __name__ == '__main__':
    predict(sys.argv[1])
