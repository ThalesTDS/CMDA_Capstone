class CNN:
    """
    A basic Convolutional Neural Network (CNN) model implementation with one convolutional layer,
    one pooling layer, and two fully connected layers.

    Attributes:
        num_bp1 (int): Number of neurons in the first fully connected (backpropagation) layer.
        num_bp2 (int): Number of neurons in the second fully connected layer.
        num_bp3 (int): Number of output neurons.
        conv1 (tuple): A tuple (kernel_size, number_of_kernels) specifying the first convolutional layer parameters.
        step_conv1 (int): Step size (stride) for the convolution operation.
        size_pooling1 (int): Size of the pooling window after the first convolutional layer.
        rate_weight (float): Learning rate for weight updates.
        rate_thre (float): Learning rate for threshold (bias) updates.
        w_conv1 (list of np.matrix): List of convolutional kernel weight matrices initialized randomly.
        wkj (np.matrix): Weight matrix connecting second and third backpropagation layers, initialized randomly.
        vji (np.matrix): Weight matrix connecting first and second backpropagation layers, initialized randomly.
        thre_conv1 (np.ndarray): Thresholds for the convolutional layer, initialized randomly.
        thre_bp2 (np.ndarray): Thresholds for the second backpropagation layer, initialized randomly.
        thre_bp3 (np.ndarray): Thresholds for the third backpropagation layer, initialized randomly.

    Inputs:
        conv1_get (tuple): A tuple (kernel_size, number_of_kernels, stride) specifying convolutional layer setup.
        size_p1 (int): Size of the pooling operation window.
        bp_num1 (int): Number of neurons in the first fully connected layer.
        bp_num2 (int): Number of neurons in the second fully connected layer.
        bp_num3 (int): Number of output neurons.
        rate_w (float, optional): Learning rate for weights. Default is 0.2.
        rate_t (float, optional): Learning rate for thresholds. Default is 0.2.

    Notes:
        - Weights and thresholds are initialized using uniform random distributions scaled and shifted to center around 0.
        - Convolutional kernels are initialized as square matrices with dimensions (kernel_size, kernel_size).
        - All weights are stored as numpy matrices for easier matrix operations during forward and backward passes.

    Maintenance Notes:
        - The current design assumes a very simple CNN with only one convolution-pooling layer and two fully connected layers.
        - Extending this model to deeper CNNs would require additional handling for multiple convolution and pooling stages.
        - To update the random initialization method (e.g., Xavier or He initialization), modify the np.random.random logic.
        - Ensure any changes to weight or threshold structures are reflected in both model creation and save/load functions.
    """

    def __init__(self, conv1_get, size_p1, bp_num1, bp_num2, bp_num3, rate_w=0.2, rate_t=0.2):
        """
        Initializes the CNN model structure with random weights and thresholds.
        """
        self.num_bp1 = bp_num1  
        self.num_bp2 = bp_num2  
        self.num_bp3 = bp_num3  
        self.conv1 = conv1_get[:2] 
        self.step_conv1 = conv1_get[2] 
        self.size_pooling1 = size_p1  
        self.rate_weight = rate_w  
        self.rate_thre = rate_t  

        rng = np.random.default_rng()

        self.w_conv1 = [np.asmatrix(-1 * rng.random((self.conv1[0], self.conv1[0])) + 0.5) for _ in range(self.conv1[1])]
        self.wkj = np.asmatrix(-1 * rng.random((self.num_bp3, self.num_bp2)) + 0.5) 
        self.vji = np.asmatrix(-1 * rng.random((self.num_bp2, self.num_bp1)) + 0.5)  

        self.thre_conv1 = -2 * rng.random(self.conv1[1]) + 1  
        self.thre_bp2 = -2 * rng.random(self.num_bp2) + 1  
        self.thre_bp3 = -2 * rng.random(self.num_bp3) + 1  

    def save_model(self, save_path):
        """
        Saves the current CNN model configuration to a file.

        Inputs:
            save_path (str): File path where the model will be serialized and stored.

        Outputs:
            None. Saves model parameters as a dictionary using pickle.

        Notes:
            - The model is saved in binary format using Python's pickle library.
            - Saved parameters include network architecture, weights, and thresholds.
            - When loading the model later, users must manually reconstruct the CNN object and reassign these parameters.
        """
        model_dic = {  
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
        with open(save_path, "wb") as f:
            pickle.dump(model_dic, f)
        print(f"Model saved: {save_path}")