# Copyright 2020 The Feverbase Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json
import os

from absl import app
from absl import flags
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import tensorflow as tf
import tensorflow_hub as hub

FLAGS = flags.FLAGS

flags.DEFINE_string('data', './articles.json', 'JSON file path.')
flags.DEFINE_integer('k', 10, 'Number of nearest neighbors.')


def load_data(path): 
    """Read article titles from a MongoDB JSON dump."""
    with open(os.path.expanduser(path), 'r') as f:
        data = json.load(f)
        titles = [article['title'] for article in data]
    return titles


def nearest_neighbors(sentence, sentences, embeddings, k=10):
    """Returns the k nearest neighbor vectors given an index."""
    idx = sentences.index(sentence)
    def compare(j):
        return embeddings[idx] @ embeddings[j].T
    nearest_idx = sorted(list(range(len(sentences))), key=compare)[1:k+1]
    nearest_sent = [sentences[i] for i in nearest_idx]
    return nearest_sent


def pretty_print(ranked):
    """Pretty prints a ranked list."""
    for i, v in enumerate(ranked):
        print("{}) {}".format(i+1, v))


def main(unused_argv):
    del unused_argv
    
    sentences = load_data(FLAGS.data)

    embed = hub.load("https://tfhub.dev/google/universal-sentence-encoder/4")
    embeddings = embed(sentences).numpy()

    sampled = np.random.choice(sentences)
    print("Sampled: {}".format(sampled))
    pretty_print(nearest_neighbors(sampled, sentences, embeddings, k=FLAGS.k))


if __name__ == '__main__':
    app.run(main)