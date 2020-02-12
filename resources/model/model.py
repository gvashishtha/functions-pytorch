import logging
try:
    import torch
except ModuleNotFoundError:
    logging.info(help("modules"))
    print(help("modules"))
    raise ModuleNotFoundError(help("modules"))
import torch.nn as nn
from torch.autograd import Variable

class RNN(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super(RNN, self).__init__()

        self.hidden_size = hidden_size

        self.i2h = nn.Linear(input_size + hidden_size, hidden_size)
        self.i2o = nn.Linear(input_size + hidden_size, output_size)
        #print(f'self.i2o is {self.i2o}')
        self.softmax = nn.LogSoftmax(dim=1)

    def forward(self, input, hidden):
        # print(f'input len is {len(input[0])}')
        # raise Exception()
        # print(f'input is {input}, hidden is {hidden}')
        combined = torch.cat((input, hidden), 1)

        hidden = self.i2h(combined)
        output = self.i2o(combined)
        #print(f'output is {output}')
        output = self.softmax(output)
        #print(f'after softmax, {output}')
        return output, hidden

    def initHidden(self):
        return Variable(torch.zeros(1, self.hidden_size))
