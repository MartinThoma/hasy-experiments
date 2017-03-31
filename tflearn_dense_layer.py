"""
Dense-Net functions.

Author : Sukrit Shankar
"""

import tensorflow as tf
from tflearn.layers.conv import conv_2d


def batch_activ_conv_densenet(network,
                              in_features,
                              out_features,
                              kernel_size,
                              is_training,
                              keep_prob):
    """
    Create part of a dense block.

    Parameters
    ----------
    network : tensor
    in_features : int
        Number of input channels
    out_features : int
        Number of Kernels
    kernel_size : int
        often 3
    is_training : bool
    keep_prob : float
        often 0.5
    """
    network = tf.contrib.layers.batch_norm(network,
                                           scale=True,
                                           is_training=is_training,
                                           updates_collections=None)
    network = tf.nn.relu(network)
    network = conv_2d(network, out_features, kernel_size)
    network = tf.nn.dropout(network, keep_prob)
    return network


def block_densenet(input, layers, in_features, growth, is_training, keep_prob):
    network = input
    features = in_features
    for idx in xrange(layers):
        tmp = batch_activ_conv_densenet(network,
                                        features,
                                        growth, 3,
                                        is_training,
                                        keep_prob)
        network = tf.concat(3, (network, tmp))
        features += growth
    return network, features
