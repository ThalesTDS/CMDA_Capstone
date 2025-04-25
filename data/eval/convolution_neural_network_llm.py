class CNN:
    def __init__(self, conv1_get, size_p1, bp_num1, bp_num2, bp_num3, rate_w=0.2, rate_t=0.2):
        """Initialize layers and weights for convolutional neural network."""
        self.num_bp1 = bp_num1  # number of units in flatten layer
        self.num_bp2 = bp_num2  # number of units in hidden layer
        self.num_bp3 = bp_num3  # number of units in output layer
        self.conv1 = conv1_get[:2]  # kernel size and count
        self.step_conv1 = conv1_get[2]  # stride for convolution
        self.size_pooling1 = size_p1  # pooling window size
        self.rate_weight = rate_w  # learning rate for weights
        self.rate_thre = rate_t  # learning rate for thresholds

        rng = np.random.default_rng()  # random number generator

        self.w_conv1 = [np.asmatrix(-1 * rng.random((self.conv1[0], self.conv1[0])) + 0.5) for _ in range(self.conv1[1])]  # conv layer weights
        self.wkj = np.asmatrix(-1 * rng.random((self.num_bp3, self.num_bp2)) + 0.5)  # output to hidden weights
        self.vji = np.asmatrix(-1 * rng.random((self.num_bp2, self.num_bp1)) + 0.5)  # hidden to input weights

        self.thre_conv1 = -2 * rng.random(self.conv1[1]) + 1  # thresholds for conv layer
        self.thre_bp2 = -2 * rng.random(self.num_bp2) + 1  # thresholds for hidden layer
        self.thre_bp3 = -2 * rng.random(self.num_bp3) + 1  # thresholds for output layer

    def save_model(self, save_path):
        """Save all model parameters using pickle."""
        model_dic = {  # model parameters to save
            "num_bp1": self.num_bp1,
            "num_bp2": self.num_bp2,
            "num_bp3": self.num_bp3,
            "conv1": self.conv1,
            "step_conv1": self.step_conv1,
            "size_pooling1": self.size_pooling1,
            "rate_weight": self.rate_weight,
            "rate_thre": self.rate_thre,
            "w_conv1": self.w_conv1,
            "wkj": self.wkj,
            "vji": self.vji,
            "thre_conv1": self.thre_conv1,
            "thre_bp2": self.thre_bp2,
            "thre_bp3": self.thre_bp3,
        }
        with open(save_path, "wb") as f:  # write model to file
            pickle.dump(model_dic, f)
        print(f"Model saved: {save_path}")
