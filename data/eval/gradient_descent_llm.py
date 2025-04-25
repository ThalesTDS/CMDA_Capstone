import numpy as np  # import numerical computing library

train_data = (  # training dataset with input-output pairs
    ((5, 2, 3), 15),
    ((6, 5, 9), 25),
    ((11, 12, 13), 41),
    ((1, 1, 1), 8),
    ((11, 12, 13), 41),
)
test_data = (((515, 22, 13), 555), ((61, 35, 49), 150))  # test dataset
parameter_vector = [2, 4, 1, 5]  # initial weights
m = len(train_data)  # number of training samples
LEARNING_RATE = 0.009  # learning rate for gradient descent

def _error(example_no, data_set="train"):
    """Returns prediction error for a specific example."""
    return calculate_hypothesis_value(example_no, data_set) - output(example_no, data_set)

def _hypothesis_value(data_input_tuple):  # evaluate linear hypothesis
    hyp_val = 0
    for i in range(len(parameter_vector) - 1):  # weighted sum of inputs
        hyp_val += data_input_tuple[i] * parameter_vector[i + 1]
    hyp_val += parameter_vector[0]  # add bias
    return hyp_val

def output(example_no, data_set):  # return true output from dataset
    if data_set == "train":
        return train_data[example_no][1]
    elif data_set == "test":
        return test_data[example_no][1]
    return None

def calculate_hypothesis_value(example_no, data_set):  # get model prediction
    if data_set == "train":
        return _hypothesis_value(train_data[example_no][0])
    elif data_set == "test":
        return _hypothesis_value(test_data[example_no][0])
    return None

def summation_of_cost_derivative(index, end=m):  # compute sum of partials
    summation_value = 0
    for i in range(end):
        if index == -1:
            summation_value += _error(i)
        else:
            summation_value += _error(i) * train_data[i][0][index]
    return summation_value

def get_cost_derivative(index):  # get partial derivative for weight
    cost_derivative_value = summation_of_cost_derivative(index, m) / m
    return cost_derivative_value

def run_gradient_descent():
    """Minimizes cost by updating parameters based on gradient estimates."""
    global parameter_vector
    absolute_error_limit = 0.000002  # tolerance for absolute error
    relative_error_limit = 0  # tolerance for relative error
    j = 0
    while True:
        j += 1
        temp_parameter_vector = [0, 0, 0, 0]  # placeholder for updated weights
        for i in range(len(parameter_vector)):
            cost_derivative = get_cost_derivative(i - 1)  # compute gradient
            temp_parameter_vector[i] = (
                parameter_vector[i] - LEARNING_RATE * cost_derivative
            )
        if np.allclose(  # check convergence
            parameter_vector,
            temp_parameter_vector,
            atol=absolute_error_limit,
            rtol=relative_error_limit,
        ):
            break
        parameter_vector = temp_parameter_vector  # update weights
    print(("Number of iterations:", j))

def test_gradient_descent():  # evaluate model on test data
    for i in range(len(test_data)):
        print(("Actual output value:", output(i, "test")))  # expected result
        print(("Hypothesis output:", calculate_hypothesis_value(i, "test")))  # prediction

if __name__ == "__main__":  # main entry point
    run_gradient_descent()
    print("\nTesting gradient descent for a linear hypothesis function.\n")
    test_gradient_descent()
