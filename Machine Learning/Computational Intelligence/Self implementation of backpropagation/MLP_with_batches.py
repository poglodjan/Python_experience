class MLP_batch:
    def __init__(self, inputs_n, neurons, batch_size=1, weight_init="uniform", normalize=False):
        np.random.seed(100)
        self.inputs_n = inputs_n
        self.output_n = inputs_n
        self.neurons = neurons
        self.normalize = normalize
        self.batch_size = batch_size
        if weight_init=="normal":
            initializer = lambda shape: np.random.randn(*shape)
        elif weight_init=="he":
            initializer = lambda shape: np.random.randn(*shape) * np.sqrt(2 / shape[0])
        elif weight_init=="xavier":
            initializer = lambda shape: np.random.randn(*shape) * np.sqrt(6 / 2*shape[0])
        elif weight_init=="uniform":
            initializer = lambda shape: np.random.uniform(0,1, shape)
        self.weights_input_hidden = initializer((int(inputs_n/batch_size), neurons))
        self.biases_hidden = np.random.randn((neurons))
        self.weights_hidden_output = initializer((neurons, int(inputs_n/batch_size)))
        self.bias_output = initializer((1, int(inputs_n/batch_size)))
        self.errors_array = []
        self.error_matrix=[]
        self.epoch_n=[]

    def sigmoid(self, x):
        return 1 / (1 + np.exp(-x))

    def train(self, x_train, y_train, iters, learn, activation=None):
        if self.normalize:
            x_train = (x_train - np.min(x_train)) / (np.max(x_train) - np.min(x_train))
            y_train = (y_train - np.min(y_train)) / (np.max(y_train) - np.min(y_train))
        if activation is None: activation = self.sigmoid

        part_size = len(x_train) // self.batch_size
        x_train_parts = [x_train[i * part_size : (i + 1) * part_size] for i in range(self.batch_size)]
        y_train_parts = [y_train[i * part_size : (i + 1) * part_size] for i in range(self.batch_size)]
##!
        # Iteracja po mniejszych danych
        k=0
        for x_train_part, y_train_part in zip(x_train_parts, y_train_parts):
            # _______________Propagacja w przód dla danych treningowych_______________
            hidden_layer_input = np.dot(x_train_part, self.weights_input_hidden) + self.biases_hidden
            hidden_layer_output = activation(hidden_layer_input)
            output_layer_input = np.dot(hidden_layer_output, self.weights_hidden_output) + self.bias_output

            y_predicted = output_layer_input
            error = y_predicted - y_train_part

            for i in range(iters):
                learning_rate = learn
                
                    # _______________Aktualizacja wag w warstwie ukrytej na wyjście_______________
                self.weights_hidden_output -= learning_rate * np.outer(error, hidden_layer_output).T
                self.bias_output -= learning_rate * np.sum(np.sum(error))

                # _______________Obliczenie wagi dla warstwy ukrytej_______________
                w = np.dot(error, self.weights_hidden_output.T) * hidden_layer_output * (1 - hidden_layer_output)
                w = w.T * x_train_part

                    # _______________Aktualizacja wag w warstwie wejściowej na ukrytą_______________
                self.weights_input_hidden -= w.T
                suma = np.sum(error.T * self.weights_hidden_output.T * hidden_layer_output * (1 - hidden_layer_output.T))
                self.biases_hidden -= learning_rate * suma

                    # _______________Ponowna propagacja w przód_______________
                new_hidden_layer_input = np.dot(x_train_part, self.weights_input_hidden) + self.biases_hidden
                new_hidden_layer_output = activation(new_hidden_layer_input)
                new_output_layer_input = np.dot(new_hidden_layer_output, self.weights_hidden_output) + self.bias_output
                new_y_predicted = new_output_layer_input
                error = new_y_predicted - y_train_part
                self.errors_array.append(np.sum(error))

                if i==0:
                    self.error_matrix.append(error)
                    self.epoch_n.append(i)
                if (i%int(iters/9)==0) and len(self.error_matrix)<9:
                    self.error_matrix.append(error)
                    self.epoch_n.append(i)
            self.epoch_n.append(i)
            self.error_matrix.append(error)
            k+=1
            print(f"MSE train after {k} batch = ", np.mean(np.square(error)))

    def predict(self, x_test,y_test):
        if self.normalize:
            x_test = (x_test - np.min(x_test)) / (np.max(x_test) - np.min(x_test))
            y_test = (y_test - np.min(y_test)) / (np.max(y_test) - np.min(y_test))
        # _______________Propagacja w przód dla danych testowych_______________
        indices=[]
        nearest_indices = np.array([np.argmin(np.abs(x_train - value)) for value in x_test])
        for i in range(len(nearest_indices)):
            k = int(np.where(np.abs(x_train - x_test[i]) == np.min(np.abs(x_train - x_test[i])))[0])
            indices.append(k)
        best_weights_hidden = self.weights_input_hidden[indices,:]
        best_weights_output = self.weights_hidden_output[:,indices]
        best_biases_out = self.bias_output[:,indices]
        hidden_layer_input_test = np.dot(x_test, best_weights_hidden) + self.biases_hidden.T
        hidden_layer_output_test = self.sigmoid(hidden_layer_input_test)
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
