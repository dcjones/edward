#!/usr/bin/env python
"""
Probability model
    Posterior: (1-dimensional) Normal
Inference: Maximum a posteriori
"""
import edward as ed
import tensorflow as tf

from edward.stats import norm

class NormalModel:
    """
    p(x, z) = Normal(x; z, Sigma)Normal(z; mu, Sigma)
    """
    def __init__(self, mu, Sigma):
        self.mu = mu
        self.Sigma = Sigma
        self.num_vars = 1

    def log_prob(self, xs, zs):
        log_prior = norm.logpdf(zs, mu, Sigma)
        log_lik = tf.pack([tf.reduce_sum(norm.logpdf(xs, z, Sigma))
                           for z in tf.unpack(zs)])
        return log_lik + log_prior

ed.set_seed(42)
mu = tf.constant(3.0)
Sigma = tf.constant(0.1)
model = NormalModel(mu, Sigma)
data = ed.Data(tf.constant((3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,0, 1, 0, 0, 0, 0, 0, 0, 0, 1), dtype=tf.float32))

inference = ed.MAP(model, data)
inference.run(n_iter=200, n_print=50)
