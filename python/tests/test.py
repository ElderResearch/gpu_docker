import boto3
import cssselect
import jupyter
import lxml
import neo4j.v1
import networkx
import nltk
import plotly
import psycopg2
import requests
# don't import via cli, only via web console (tk not installed)
#import seaborn
import sqlalchemy
import tables
import tqdm
import xlrd


# torch testing
import torch
assert torch.__version__ >= '0.4.0'

import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim

torch.manual_seed(1)
lin = nn.Linear(5, 3)
data = torch.randn(2, 5)
x = torch.Tensor([[0.1755, -0.3268, -0.5069], [-0.6602, 0.2260, 0.1089]])
assert not ((x - lin(data)).abs() > 1e-4).any()



# tensorflow testing
import tensorflow
assert tensorflow.__version__ >= '1.7.0'

hello = tensorflow.constant('hello')
with tensorflow.Session() as sess:
    assert sess.run(hello) == b'hello'


# mxnet validation (via http://mxnet.incubator.apache.org/install/index.html)
import mxnet as mx
import numpy as np

a = mx.nd.ones((2, 3), mx.gpu())
b = a * 2 + 1
assert np.array_equal(
    b.asnumpy(),
    np.array([
        [3., 3., 3.],
        [3., 3., 3.]
    ])
)
