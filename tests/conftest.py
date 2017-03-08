"""Test fixtures."""
import pytest
import numpy as np
import tensorflow as tf


@pytest.fixture
def make_data():
    """Make some simple data."""
    N = 100
    x1 = np.linspace(-10, 10, N)
    x2 = np.linspace(-1, 1, N)**2
    x = np.vstack((x1, x2)).T
    w = np.array([[0.5], [2.0]])
    Y = np.dot(x, w) + np.random.randn(N, 1)
    X = tf.tile(tf.expand_dims(x, 0), [3, 1, 1])
    return x, Y, X