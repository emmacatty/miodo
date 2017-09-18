# coding:utf-8
# 2017/9/18 下午8:01
# 286287737@qq.com

from common import *


class NFM(object):
    def __init__(self, conf_file):
        cf_str, cf_float, cf_int = read_config(conf_file)
        self.random_seed = 1314
        self.sparse_dim = cf_int("sparse_dim")
        self.layer_dim = eval(cf_str("layer_dim"))
        self.batch_norm = False
        self.hidden_factor = cf_int("fm_factor")

    def inference(self, kv):
        tf.set_random_seed(self.random_seed)

        self.fea = tf.sparse_merge(kv['fid'], kv['fval'], self.sparse_dim)

        self._initialize_weights()

        embeds = tf.nn.embedding_lookup(self.weights['emb_weight'], self.fea)
        self.mean_embeds = tf.reduce_sum(embeds, 1)

        self.square_last_embeds = tf.square(self.mean_embeds)

        self.square_embeds = tf.square(embeds)
        self.mean_last_embeds = tf.reduce_sum(self.square_embeds, 1)

        self.FM = 0.5 * tf.subtract(self.square_last_embeds, self.mean_last_embeds)

        for i in range(0, len(self.layer_dim)):
            self.FM = tf.add(tf.matmul(self.FM, self.weights['l%d' % i]), self.weights['b%d' % i])
            self.FM = tf.nn.relu(self.FM)

        self.FM = tf.matmul(self.FM, self.weights['pred']) + self.weights['bias']
        self.emb_bias = tf.nn.embedding_lookup_sparse(self.weights['emb_bias'], self.fea, None, combiner="mean")
        self.out = self.FM + self.emb_bias

    def get_weight_size(self):
        total_parameters = 0
        for variable in self.weights.values():
            shape = variable.get_shape()  # shape is an array of tf.Dimension
            variable_parameters = 1
            for dim in shape:
                variable_parameters *= dim.value
            total_parameters += variable_parameters
        print "#params: %d" % total_parameters

    def batch_norm_layer(self, x, train_phase, scope_bn):
        # tf.layers.batch_normalization()
        bn_train = tf.layers.batch_normalization(x, momentum=0.9, center=True, scale=True, training=True)
        # bn_inference = batch_norm(x, decay=0.9, center=True, scale=True, updates_collections=None,
        #                           is_training=False, reuse=True, trainable=True, scope=scope_bn)
        # z = tf.cond(train_phase, lambda: bn_train, lambda: bn_inference)
        return tf.no_op()

    def _initialize_weights(self):
        all_weights = dict()
        glorot = tf.uniform_unit_scaling_initializer()
        all_weights['emb_weight'] = tf.get_variable(
            shape=[self.sparse_dim, self.hidden_factor], initializer=glorot, name='feature_embeddings')
        all_weights['emb_bias'] = tf.get_variable(
            shape=[self.sparse_dim, 1], initializer=tf.zeros_initializer, name='feature_bias')

        assert self.layer_dim
        all_weights['l0'] = tf.get_variable(
            name="l0", initializer=glorot, shape=[self.hidden_factor, self.layer_dim[0]], dtype=tf.float32)
        all_weights['b0'] = tf.get_variable(
            name="b0", initializer=tf.zeros_initializer, shape=[self.layer_dim[0]], dtype=tf.float32)
        for i in range(1, len(self.layer_dim)):
            all_weights['l%d' % i] = tf.get_variable(
                name="l%d" % i, initializer=glorot, shape=self.layer_dim[i - 1:i + 1], dtype=tf.float32)
            all_weights['b%d' % i] = tf.get_variable(
                name="b0", initializer=tf.zeros_initializer, shape=[self.layer_dim[0]], dtype=tf.float32)
        all_weights['pred'] = tf.get_variable(
            name="pred", initializer=glorot, shape=[self.layer_dim[-1], 1], dtype=tf.float32)
        all_weights['bias'] = tf.Variable(0.0, name='bias')
        self.weights = all_weights


if __name__ == "__main__":
    pass
