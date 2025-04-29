import numpy as np

train_data = ( 
    ((5, 2, 3), 15),
    ((6, 5, 9), 25),
    ((11, 12, 13), 41),
    ((1, 1, 1), 8),
    ((11, 12, 13), 41),
)

test_data = (((515, 22, 13), 555), ((61, 35, 49), 150))

parameter_vector = [2, 4, 1, 5]

m = len(train_data)

LEARNING_RATE = 0.009


def _error(example_no, data_set="train"):
    """
    Calculates the error between the predicted and actual output for a given example.

    Inputs:
        example_no (int): Index of the example in the specified dataset.
        data_set (str): Either "train" or "test" to specify the dataset. Default is "train".

    Outputs:
        float: Difference between the hypothesis value and the actual output.

    Notes:
        This function internally calls the hypothesis and output functions.
    """
    return calculate_hypothesis_value(example_no, data_set) - output(example_no, data_set)


def _hypothesis_value(data_input_tuple):
    """
    Computes the hypothesis (predicted value) for a given input using the current parameter vector.

    Inputs:
        data_input_tuple (tuple): Input features as a tuple of numeric values.

    Outputs:
        float: Predicted output computed by the linear hypothesis function.

    Notes:
        The hypothesis function is of the form: h(x) = θ₀ + θ₁x₁ + θ₂x₂ + ... + θₙxₙ,
        where θ are the model parameters.
    """
    hyp_val = 0
    for i in range(len(parameter_vector) - 1):
        hyp_val += data_input_tuple[i] * parameter_vector[i + 1]
    hyp_val += parameter_vector[0]
    return hyp_val


def output(example_no, data_set):
    """
    Retrieves the actual output value (label) for a given example.

    Inputs:
        example_no (int): Index of the example.
        data_set (str): Either "train" or "test" to specify the dataset.

    Outputs:
        int: Actual output value corresponding to the example.

    Notes:
        Returns None if an invalid dataset name is provided.
    """
    if data_set == "train":
        return train_data[example_no][1]
    elif data_set == "test":
        return test_data[example_no][1]
    return None


def calculate_hypothesis_value(example_no, data_set):
    """
    Computes the hypothesis value for a specific example number from the given dataset.

    Inputs:
        example_no (int): Index of the example.
        data_set (str): Either "train" or "test" to specify the dataset.

    Outputs:
        float: Hypothesis output computed for the example.

    Notes:
        Returns None if an invalid dataset name is provided.
    """
    if data_set == "train":
        return _hypothesis_value(train_data[example_no][0])
    elif data_set == "test":
        return _hypothesis_value(test_data[example_no][0])
    return None


def summation_of_cost_derivative(index, end=m):
    """
    Calculates the summation term used in computing the gradient (cost derivative).

    Inputs:
        index (int): Feature index (-1 indicates bias term).
        end (int, optional): Number of examples to consider. Defaults to m (total training examples).

    Outputs:
        float: Summation of errors (or errors multiplied by feature value) across examples.

    Notes:
        Used to compute partial derivatives of the cost function with respect to each parameter.
    """
    summation_value = 0
    for i in range(end):
        if index == -1:
            summation_value += _error(i)
        else:
            summation_value += _error(i) * train_data[i][0][index]
    return summation_value


def get_cost_derivative(index):
    """
    Computes the gradient (partial derivative) of the cost function with respect to a parameter.

    Inputs:
        index (int): Index of the parameter to differentiate with respect to.

    Outputs:
        float: Average gradient value over the training set.

    Notes:
        This function normalizes the summation value by the number of examples (m).
    """
    cost_derivative_value = summation_of_cost_derivative(index, m) / m
    return cost_derivative_value


def run_gradient_descent():
    """
    Runs batch gradient descent to update the parameter vector until convergence.

    Inputs:
        None (relies on global parameter_vector and training data).

    Outputs:
        None (updates parameter_vector in-place).

    Notes:
        - Convergence is based on absolute tolerance (atol) using numpy's allclose function.
        - Assumes a fixed learning rate (LEARNING_RATE).
        - Terminates when parameter updates are within the specified tolerance.
        - Prints the number of iterations taken to converge.

    Maintenance:
        - Tuning LEARNING_RATE, absolute_error_limit, or using a dynamic learning rate schedule
          could improve training.
        - Extending to stochastic or mini-batch gradient descent would require reworking the summation step.
    """
    global parameter_vector
    
    absolute_error_limit = 0.000002
    relative_error_limit = 0
    j = 0
    while True:
        j += 1
        temp_parameter_vector = [0, 0, 0, 0]
        for i in range(len(parameter_vector)):
            cost_derivative = get_cost_derivative(i - 1)
            temp_parameter_vector[i] = (
                parameter_vector[i] - LEARNING_RATE * cost_derivative
            )
        if np.allclose(
            parameter_vector,
            temp_parameter_vector,
            atol=absolute_error_limit,
            rtol=relative_error_limit,
        ):
            break
        parameter_vector = temp_parameter_vector
    print(("Number of iterations:", j))


def test_gradient_descent():
    """
    Tests the trained model on the test dataset and prints predicted vs actual values.

    Inputs:
        None.

    Outputs:
        None (prints results to standard output).

    Notes:
        Useful for checking the generalization of the model after training.
    """
    for i in range(len(test_data)):
        print(("Actual output value:", output(i, "test")))
        print(("Hypothesis output:", calculate_hypothesis_value(i, "test")))


if __name__ == "__main__":
    """
    Entry point for running the script.

    Behavior:
        - Trains the model using gradient descent.
        - Tests the trained model on the test data.

    Notes:
        Ensure that train_data, test_data, and parameter_vector are properly defined before running.
    """
    run_gradient_descent()
    print("\nTesting gradient descent for a linear hypothesis function.\n")
    test_gradient_descent()
