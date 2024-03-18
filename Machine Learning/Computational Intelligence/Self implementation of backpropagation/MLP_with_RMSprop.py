class MLP_with_RMSprop:
    def __init__(self, inputs_n, neurons, weight_init="uniform", normalize=False):
        np.random.seed(100)
        self.inputs_n = inputs_n
        self.output_n = inputs_n
        self.neurons = neurons
        self.normalize = normalize
        if weight_init=="normal":
            initializer = lambda shape: np.random.randn(*shape)
        elif weight_init=="he":
            initializer = lambda shape: np.random.randn(*shape) * np.sqrt(2 / shape[0])
        elif weight_init=="xavier":
            initializer = lambda shape: np.random.randn(*shape) * np.sqrt(6 / 2*shape[0])
        elif weight_init=="uniform":
            initializer = lambda shape: np.random.uniform(0,1, shape)
        #inicjalizacja wag + biasów    
        self.weights_input_hidden = initializer((inputs_n, neurons))
        self.biases_hidden = np.random.randn((neurons))
        self.weights_hidden_output = initializer((neurons, inputs_n))
        self.bias_output = initializer((1, inputs_n))
        #inicjalizacja momentu
        self.g_weights_input_hidden=np.zeros((inputs_n,neurons))
        self.g_bias_hidden=np.zeros(neurons)
        self.g_weights_hidden_output=np.zeros((neurons,inputs_n))
        self.g_bias_output=np.zeros(inputs_n)
        # pomocnicze tabele
        self.errors_array = []
        self.error_matrix=[]
        self.epoch_n=[]

    def sigmoid(self, x):
        return 1 / (1 + np.exp(-x))
    def expected2(self, x):
        return np.var(x) - np.mean(x)*np.mean(x)

    def train(self, x_train, y_train, iters, learn, activation=None, beta=0.5):
        if self.normalize:
            x_train = (x_train - np.min(x_train)) / (np.max(x_train) - np.min(x_train))
            y_train = (y_train - np.min(y_train)) / (np.max(y_train) - np.min(y_train))
        if activation is None: activation = self.sigmoid
        self.x_train = x_train
        self.y_train = y_train
        self.momentum_lambda = beta
            # _______________Propagacja w przód dla danych treningowych_______________
        hidden_layer_input = np.dot(x_train, self.weights_input_hidden) + self.biases_hidden
        hidden_layer_output = activation(hidden_layer_input)
        output_layer_input = np.dot(hidden_layer_output, self.weights_hidden_output) + self.bias_output

        y_predicted = output_layer_input
        error = y_predicted - y_train
        print(np.sum(error))

        for i in range(iters):
            learning_rate = learn

                           # _______________Aktualizacja funkcji g w warstwie ukrytej na wyjście_______________
            self.g_weights_hidden_output=self.g_weights_hidden_output - learning_rate * np.outer(error, hidden_layer_output).T
            self.g_bias_output=self.g_bias_output - learning_rate * np.sum(np.sum(error)) 

            w = np.dot(error, self.g_weights_hidden_output.T) * hidden_layer_output * (1 - hidden_layer_output)
            w = w.T * x_train
            self.g_weights_input_hidden=self.g_weights_input_hidden - w.T

            suma = np.sum(error.T * self.g_weights_hidden_output.T * hidden_layer_output * (1 - hidden_layer_output.T))
            self.g_bias_hidden=self.g_bias_hidden - learning_rate * suma

            expexted_g_weights_hidden_output = beta * self.expected2(self.g_weights_hidden_output) + (1-beta) * self.expected2(self.g_weights_hidden_output)
            expexted_g_weights_input_hidden = beta * self.expected2(self.g_weights_input_hidden) + (1-beta) * self.expected2(self.g_weights_input_hidden)
            expected_g_bias_hidden = beta * self.expected2(self.g_bias_hidden) + (1-beta) * self.expected2(self.g_bias_hidden)
            expected_g_bias_output = beta * self.expected2(self.g_bias_output) + (1-beta) * self.expected2(self.g_bias_output)

            # obliczenie delty na wagach #
            self.weights_hidden_output -= learning_rate * self.g_weights_hidden_output/np.sqrt(expexted_g_weights_hidden_output)
            self.weights_input_hidden -= learning_rate * self.g_weights_input_hidden/np.sqrt(expexted_g_weights_input_hidden)
            self.bias_output -= learning_rate * self.g_bias_output/np.sqrt(expected_g_bias_output)
            self.biases_hidden -= learning_rate * self.g_bias_hidden/np.sqrt(expected_g_bias_hidden)
            # 

                # _______________Nowa propagacja w przód_______________
            hidden_layer_input =np.dot(x_train, self.weights_input_hidden) + self.biases_hidden
            hidden_layer_output = activation(hidden_layer_input)
            output_layer_input = np.dot(hidden_layer_output, self.weights_hidden_output) + self.bias_output
            new_y_predicted = output_layer_input
            error = new_y_predicted - y_train
            self.errors_array.append(np.sum(error))
            print(error)

        self.epoch_n.append(i)
        self.error_matrix.append(error)
        print("MSE train =", np.mean(np.square(error)))

    def predict(self, x_test,y_test):
        if self.normalize:
            x_test = (x_test - np.min(x_test)) / (np.max(x_test) - np.min(x_test))
            y_test = (y_test - np.min(y_test)) / (np.max(y_test) - np.min(y_test))
        # _______________Propagacja w przód dla danych testowych_______________
        indices=[]
        nearest_indices = np.array([np.argmin(np.abs(self.x_train - value)) for value in x_test])
        for i in range(len(nearest_indices)):
            k = int(np.where(np.abs(self.x_train - x_test[i]) == np.min(np.abs(self.x_train - x_test[i])))[0])
            indices.append(k)
        best_weights_hidden = self.weights_input_hidden[indices,:]
        best_weights_output = self.weights_hidden_output[:,indices]
        best_biases_out = self.bias_output[:,indices]
        hidden_layer_input_test = np.dot(x_test, best_weights_hidden) + self.biases_hidden.T
        hidden_layer_output_test = sigm(hidden_layer_input_test)
        output_layer_input_test = np.dot(hidden_layer_output_test, best_weights_output) + best_biases_out
        difference_test = y_test - output_layer_input_test
        print("MSE test =", np.mean(np.square(difference_test)))

        return output_layer_input_test
    
    def show_error(self):
        plt.plot(range(1, len(self.errors_array)+1), self.errors_array)
        plt.xlabel('Epoch')
        plt.ylabel('Error')
        plt.title('Error over Epochs')
        plt.show()

    def show_matrix_error(self):
        fig, axs = plt.subplots(3,3, figsize=(10, 10))
        k=0
        for i in range(3):
            for j in range(3):
                ax = axs[i, j]
                error_values = self.error_matrix[k] 
                k+=1
                im = ax.imshow(error_values.reshape(1, -1), cmap='Blues', aspect='auto', vmin=0, vmax=self.error_matrix[0].max())
                ax.set_title(f'Epoch {self.epoch_n[k]+1}')
        cbar = fig.colorbar(im, ax=axs, orientation='vertical', fraction=0.03, pad=0.1)
        cbar.set_label('Error')
        plt.show()
