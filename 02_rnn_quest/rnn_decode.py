"""RNN Quest: forward pass Elman RNN + жадібний декодинг повідомлення з ваг.

Запуск: python rnn_decode.py <папка_з_розпакованим_архівом>
"""
import json
import sys

import numpy as np

D = sys.argv[1] if len(sys.argv) > 1 else "quest"


def load(name):
    return np.array(json.load(open(f"{D}/{name}.json")))


vocab = json.load(open(f"{D}/vocab.json"))
E, W_h, b_h, U_h, W_y = (load(n) for n in
                         ("embedding.weight", "W_h.weight", "W_h.bias", "U_h.weight", "W_y.weight"))

h = np.zeros(U_h.shape[0])
token = vocab.index("[")
out = []
for _ in range(1000):
    h = np.tanh(W_h @ E[token] + b_h + U_h @ h)   # h_t = tanh(W_h x_t + b + U_h h_{t-1})
    token = int(np.argmax(W_y @ h))               # y_t = W_y h_t, greedy
    if vocab[token] == "]":
        break
    out.append(vocab[token])
print("".join(out))
