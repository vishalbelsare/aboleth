"""Package helper utilities."""
import tensorflow as tf
import numpy as np


def pos(X, minval=1e-10):
    """Constrain a ``tf.Variable`` to be positive only."""
    # return tf.exp(X)  # Medium speed, but gradients tend to explode
    # return tf.nn.softplus(X)  # Slow but well behaved!
    return tf.maximum(tf.abs(X), minval)  # Faster, but more local optima


def batch(data_dict, N_, batch_size, n_iter=10000, seed=None):
    """
    Create random batches for Stochastic gradients.

    Feed dict data generator for SGD that will yeild random batches for a
    a defined number of iterations, which can be infinite. This generator makes
    consecutive passes through the data, drawing without replacement on each
    pass.

    Parameters
    ----------
    data : dict of ndarrays
        The data with ``{tf.placeholder: data}`` entries.
    N_ : tf.placeholder (int)
        Place holder for the size of the dataset. This will be fed to an
        algorithm.
    batch_size : int
        number of data points in each batch.
    n_iter : int, optional
        The number of iterations
    seed : None, int or RandomState, optional
        random seed

    Yields
    ------
    dict:
        with each element an array length ``batch_size``, i.e. a subset of
        data, and an element for ``N_``. Use this as your feed-dict when
        evaluating a loss, training, etc.
    """
    N = data_dict[list(data_dict.keys())[0]].shape[0]
    perms = endless_permutations(N, seed)

    i = 0
    while i < n_iter:
        i += 1
        ind = np.array([next(perms) for _ in range(batch_size)])
        batch_dict = {k: v[ind] for k, v in data_dict.items()}
        batch_dict[N_] = N
        yield batch_dict


def endless_permutations(N, seed=None):
    """
    Generate an endless sequence of permutations of the set [0, ..., N).

    If we call this N times, we will sweep through the entire set without
    replacement, on the (N+1)th call a new permutation will be created, etc.

    Parameters
    ----------
    N: int
        the length of the set
    seed: None, int or RandomState, optional
        random seed

    Yields
    ------
    int:
        a random int from the set [0, ..., N)
    """
    if isinstance(seed, np.random.RandomState):
        generator = seed
    else:
        generator = np.random.RandomState(seed)

    while True:
        batch_inds = generator.permutation(N)
        for b in batch_inds:
            yield b
