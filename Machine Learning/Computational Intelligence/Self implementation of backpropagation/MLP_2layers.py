class MLP_2layers:
    def __init__(self, inputs_n, neurons_layer1, neurons_layer2):
        np.random.seed(100)
        self.inputs_n = inputs_n
        self.output_n = inputs_n
        self.neurons_layer1 = neurons_layer1
        self.neurons_layer2 = neurons_layer2

        # Wagi i biasy dla pierwszej warstwy ukrytej
        self.weights_input_hidden1 = np.random.randn(inputs_n, neurons_layer1)
        self.biases_hidden1 = np.random.randn(neurons_layer1)

        # Wagi i biasy dla drugiej warstwy ukrytej
        self.weights_hidden1_hidden2 = np.random.randn(neurons_layer1, neurons_layer2)
        self.biases_hidden2 = np.random.randn(neurons_layer2)

        # Wagi i biasy dla warstwy wyjściowej
        self.weights_hidden2_output = np.random.randn(neurons_layer2, inputs_n)
        self.bias_output = np.random.randn(1, inputs_n)

        self.errors_array = []
        self.error_matrix = []
        self.epoch_n = []

    def sigmoid(self, x):
        return 1 / (1 + np.exp(-x))

    def train(self, x_train, y_train, iters, learn, activation=None):
        if activation is None:
            activation = self.sigmoid

        for i in range(iters):
            # Propagacja w przód dla danych treningowych
            hidden_layer1_input = np.dot(x_train, self.weights_input_hidden1) + self.biases_hidden1
            hidden_layer1_output = activation(hidden_layer1_input)

            hidden_layer2_input = np.dot(hidden_layer1_output, self.weights_hidden1_hidden2) + self.biases_hidden2
            hidden_layer2_output = activation(hidden_layer2_input)

            output_layer_input = np.dot(hidden_layer2_output, self.weights_hidden2_output) + self.bias_output
            y_predicted = output_layer_input

            error = y_predicted - y_train

            # Aktualizacja wag dla warstwy ukrytej 2 na wyjście
            self.weights_hidden2_output -= learn * np.outer(error,hidden_layer2_output).T
            self.bias_output -= learn * np.sum(error)

            # Obliczenie wagi dla warstwy ukrytej 1
            w_hidden2 = np.dot(error, self.weights_hidden2_output.T) * hidden_layer2_output * (1 - hidden_layer2_output)
            w_hidden2 = w_hidden2.T * hidden_layer1_output

            # Aktualizacja wag dla warstwy ukrytej 1 na warstwę ukrytą 2
            self.weights_hidden1_hidden2 -= learn * np.dot(hidden_layer1_output.T, w_hidden2).T
            self.biases_hidden2 -= learn * np.sum(w_hidden2, axis=0)

            # Ponowna propagacja w przód
            new_hidden_layer1_input = np.dot(x_train, self.weights_input_hidden1) + self.biases_hidden1
            new_hidden_layer1_output = activation(new_hidden_layer1_input)

            new_hidden_layer2_input = np.dot(new_hidden_layer1_output, self.weights_hidden1_hidden2) + self.biases_hidden2
            new_hidden_layer2_output = activation(new_hidden_layer2_input)

            new_output_layer_input = np.dot(new_hidden_layer2_output, self.weights_hidden2_output) + self.bias_output
            new_y_predicted = new_output_layer_input
            error = new_y_predicted - y_train
            self.errors_array.append(np.sum(error))

            if i == 0:
                self.error_matrix.append(error)
                self.epoch_n.append(i)
            if (i % int(iters / 9) == 0) and len(self.error_matrix) < 9:
                self.error_matrix.append(error)
                self.epoch_n.append(i)

        self.epoch_n.append(i)
        self.error_matrix.append(error)
        print("MSE train =", np.mean(np.square(error)))

    def predict(self, x_test, y_test):
        # _______________Propagacja w przód dla danych testowych_______________
        indices = []
        nearest_indices = np.array([np.argmin(np.abs(x_train - value)) for value in x_test])
        for i in range(len(nearest_indices)):
            k = int(np.where(np.abs(x_train - x_test[i]) == np.min(np.abs(x_train - x_test[i])))[0])
            indices.append(k)
        best_weights_hidden1 = self.weights_input_hidden1[indices, :]
        best_weights_output = self.weights_hidden2_output[:, indices]
        best_biases_out = self.bias_output[:, indices]

        # layer 1
        hidden_layer1_input_test = np.dot(x_test, best_weights_hidden1) + self.biases_hidden1.T
        hidden_layer1_output_test = self.sigmoid(hidden_layer1_input_test)

        # layer 2
        hidden_layer2_input_test = np.dot(hidden_layer1_output_test,  self.weights_hidden1_hidden2) + self.biases_hidden2.T
        hidden_layer2_output_test = self.sigmoid(hidden_layer2_input_test)

        output_layer_input_test = np.dot(hidden_layer2_output_test, best_weights_output) + best_biases_out
        difference_test = y_test - output_layer_input_test
        print("MSE test =", np.mean(np.square(difference_test)))

        return output_layer_input_test

    def show_error(self):
        plt.plot(range(1, len(self.errors_array) + 1), self.errors_array)
        plt.xlabel('Epoch')
        plt.ylabel('Error')
        plt.title('Error over Epochs')
        plt.show()

    def show_matrix_error(self):
        fig, axs = plt.subplots(3, 3, figsize=(10, 10))
        k = 0
        for i in range(3):
            for j in range(3):
                ax = axs[i, j]
                error_values = self.error_matrix[k]
                k += 1
                im = ax.imshow(error_values.reshape(1, -1), cmap='Blues', aspect='auto', vmin=0,
                               vmax=self.error_matrix[0].max())
                ax.set_title(f'Epoch {self.epoch_n[k] + 1}')
        cbar = fig.colorbar(im, ax=axs, orientation='vertical', fraction=0.03, pad=0.1)
        cbar.set_label('Error')
        plt.show()
