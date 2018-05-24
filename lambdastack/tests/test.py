import torch
assert torch.__version__ >= '0.4.0'

import tensorflow
assert tensorflow.__version__ >= '1.7.0'

hello = tensorflow.constant('hello')
with tensorflow.Session() as sess:
    assert sess.run(hello) == b'hello'
