import numpy as np

class NeuralNetwork:
    def __init__(self, input_size, hidden_size, output_size):
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.output_size = output_size
        
        # ______ Inicjalizacja wag i biasów ______
        self.weights_input_hidden = np.random.randn(input_size, hidden_size)
        self.bias_hidden = np.random.randn(hidden_size)
        self.weights_hidden_output = np.random.randn(hidden_size, output_size)
        self.bias_output = np.random.randn(output_size)
        
    def sigmoid(self, x):
        return 1 / (1 + np.exp(-x))
    
    def softmax(self, x):
        exp_values = np.exp(x - np.max(x, axis=1, keepdims=True))
        return exp_values / np.sum(exp_values, axis=1, keepdims=True)
    
    def forward(self, x):
        # _______ Propagacja w przód _______
        hidden_layer_input = np.dot(x, self.weights_input_hidden) + self.bias_hidden
        hidden_layer_output = self.sigmoid(hidden_layer_input)
        output_layer_input = np.dot(hidden_layer_output, self.weights_hidden_output) + self.bias_output
        output = self.softmax(output_layer_input)
        return output, hidden_layer_output
    
    def backward(self, x, y, output, hidden_output, learning_rate):

        # ________ Obliczanie gradientów ________
        output_delta = output - y
        hidden_delta = np.dot(output_delta, self.weights_hidden_output.T) * hidden_output * (1 - hidden_output)
        d_weights_hidden_output = np.dot(hidden_output.T, output_delta)
        d_bias_output = np.sum(output_delta, axis=0)
        d_weights_input_hidden = np.dot(x.T, hidden_delta)
        d_bias_hidden = np.sum(hidden_delta, axis=0)
        
        # ______ Aktualizacja wag i biasów _______
        self.weights_hidden_output -= learning_rate * d_weights_hidden_output
        self.bias_output -= learning_rate * d_bias_output
        self.weights_input_hidden -= learning_rate * d_weights_input_hidden
        self.bias_hidden -= learning_rate * d_bias_hidden
    
    def train(self, x_train, y_train, epochs, learning_rate):
        for epoch in range(epochs):
            output, hidden_output = self.forward(x_train) # forward 
            self.backward(x_train, y_train, output, hidden_output, learning_rate) # backward

            f1 = self.f1_fun(output, y_train)
            ac = self.accuracy(output, y_train)

            # Print f-score
        print(f'Epoch {epoch}, F1 Score: {f1}\n')
        print(f'Epoch {epoch}, Accuracy Score: {ac}')
        
    def predict(self, x):
        output, _ = self.forward(x)
        return np.argmax(output, axis=1)

    def f1_fun(self, output, y_train):
        true_positives = np.sum((output == 1) & (y_train == 1))
        false_positives = np.sum((output == 1) & (y_train == 0))
        false_negatives = np.sum((output == 0) & (y_train == 1))
        precision = true_positives / (true_positives + false_positives) if (true_positives + false_positives) != 0 else 0
        recall = true_positives / (true_positives + false_negatives) if (true_positives + false_negatives) != 0 else 0
        f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) != 0 else 0
        return f1
    def accuracy(self, output, y_train):
        true_positives = np.sum((output == 1) & (y_train == 1))
        true_negatives = np.sum((output == 0) & (y_train == 0))
        return (true_positives + true_negatives) / len(y_train)
