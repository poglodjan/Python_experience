
import numpy as np
import matplotlib.pyplot as plt

class MultiLayers(object):
    def __init__(self, input_size, layer_sizes, output_size, 
                 weight_init="normal", activation="sigm", exit="linear", measure="mse",
                 momentum = False, rmsProp=False, normalization="none"):
        ## ________________________________________ Initialization ________________________________________ ##
        # 0) layers and architecture init
        np.random.seed(50)
        layers = [input_size] + layer_sizes + [output_size]
        IN = layers[:-1]
        OUT = layers[1:]
        if momentum==True: self.momentum = True
        else: self.momentum = False
        if rmsProp==True: self.rmsProp = True
        else: self.rmsProp = False
        if normalization=="none": self.normalization = None
        if normalization=="std": self.normalization = "std"
        if normalization=="minmax": self.normalization = "minmax"
        # 1) __ wieghts init
        if weight_init == "normal":
            def initializer(a,b): return np.random.normal(0,1, size=(a,b))
        elif weight_init == "he":
            def initializer(a,b): return np.random.normal(0,np.sqrt(2/(a+b)), size=(a,b))
        elif weight_init=="xavier":
            def initializer(a,b): return np.random.normal(0,np.sqrt(6/2*(a+b)), size=(a,b))
        elif weight_init=="uniform":
            def initializer(a,b): return np.random.uniform(0,1, size=(a,b))
        # 2) __ Loss function
        if measure=="mse": self.measure = self.mse_loss
        if measure=="f1": self.measure = self.cross_entropy_loss
        # 3) __ Activation function
        if activation=="relu": 
            self.activation = self.relu
            self.derivative = self.relu_derivative
        elif activation=="tanh": 
            self.activation = self.tanh
            self.derivative = self.tanh_derivative
        elif activation=="linear": 
            self.activation = self.linear
            self.derivative = self.linear_derivative
        elif activation=="sigm": 
            self.activation = self.sigmoid
            self.derivative = self.sigmoid_derivative
        # 4) __ exit activation
        if exit=="linear" and self.normalization==None: self.exit = self.linear
        if exit=="linear" and self.normalization=="std": self.exit = self.denormalize_std
        if exit=="linear" and self.normalization=="minmax": self.exit = self.denormalize_minmax
        if exit!="linear": self.exit = self.softmax

        # 5) _______ weights and biases initialation ______
        self.weights = [initializer(input,output) for (input,output) in zip(IN,OUT)]
        self.biases = [np.zeros(output) for output in OUT]
        # 6) _______ arrays for neurons calculating _______
        self.summed = [None]*len(self.weights) # _______ calculating linear combinations on a single neuron
        self.activated = [None]*len(self.weights) # _______ calculated activation on linear combinations
        # 7) _______ Momentum - velocity _________
        self.V_biases = [np.zeros(b.shape) for b in self.biases]
        self.V_weights = [np.zeros(w.shape) for w in self.weights]
        # 8) _______ Means for RMS prop  _________
        self.M_biases = [np.zeros(b.shape) for b in self.biases]
        self.M_weigths = [np.zeros(w.shape) for w in self.weights]

        # 9) __ arrays for errors
        self.errors_array = []
        self.error_matrix=[]
        self.epoch_n=[]
        self.scores = []

    #####
    ## ________________________________________ Activation Formulas ________________________________________ ##
    def sigmoid(self, x):
        return 1 / (1 + np.exp(-x))
    def relu(self, x):
        return np.maximum(0, x)
    def tanh(self, x):
        return np.tanh(x)
    def linear(self, x):
        return x
    # 1) __ activation - derivative formulas
    def relu_derivative(self,x):
        return np.where(x > 0, 1, 0)
    def tanh_derivative(self,x):
        return 1 - np.tanh(x)**2
    def sigmoid_derivative(self,x):
        return self.sigmoid(x) * (1 - self.sigmoid(x))
    def linear_derivative(self,x):
        return 1
    def softmax(self, x):
        exp_values = np.exp(x - np.max(x, axis=1, keepdims=True))
        return exp_values / np.sum(exp_values, axis=1, keepdims=True)
    # 2) __ loss function - regression
    def mse_loss(self, y_true, y_pred):
        return np.mean((y_true - y_pred)**2)
    def mse_loss_derivative(self, y_true, y_pred):
        return 2 * (y_pred - y_true) / len(y_true)
    # 3) __ loss function - classification
    def cross_entropy_loss(self, y_true, y_pred):
        epsilon = 1e-15  
        y_pred = np.clip(y_pred, epsilon, 1 - epsilon)  
        return -np.sum(y_true * np.log(y_pred)) / len(y_true)
    def cross_entropy_loss_derivative(self, y_true, y_pred):
        return (y_pred - y_true)
    # 4) ___ f1 - score
    def f1_fun(self, output, y_train):
        true_positives = np.sum((output == 1) & (y_train == 1))
        false_positives = np.sum((output == 1) & (y_train == 0))
        false_negatives = np.sum((output == 0) & (y_train == 1))
        precision = true_positives / (true_positives + false_positives) if (true_positives + false_positives) != 0 else 0
        recall = true_positives / (true_positives + false_negatives) if (true_positives + false_negatives) != 0 else 0
        f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) != 0 else 0
        return f1
    ######
    
## ________________________________________ Fit ________________________________________ ##
##
##
    def forward(self, x):
# 1) _______ Propagacja w przód _______
        if self.normalization=="std": layer=self.normalize_std(x)
        if self.normalization=="minmax": layer=self.normalize_minmax(x)
        layer = x 
        n=len(self.weights)
        self.summed[0] = layer   # ____ first layer

        for i in range(n-1): # ____ go over all layers except first/last  
            self.activated[i] = layer
            layer = np.dot(layer,self.weights[i]) + self.biases[i]
            self.summed[i+1] = layer
            layer = self.activation(layer) 

        self.activated[-1]=layer   # ____ last layer
        output_layer = np.dot(layer,self.weights[-1]) + self.biases[-1] 
        output = self.exit(output_layer)
        return output
    
    def backward(self,y,y_predicted, optimization_method):
# 2) _______ backward algorithm with gradients _______ #
        gradient_biases, gradient_weights = self.gradients(y, y_predicted)
        gradient_biases, gradient_weights = optimization_method(gradient_biases, gradient_weights)
        self.weights = [w- self.learn*g for (w,g) in zip(self.weights, gradient_weights)]
        self.biases = [b- self.learn*g for (b,g) in zip(self.biases,gradient_biases)]

# 3) _______ Train data _______ #
    def train(self, x_train, y_train, epochs, batch_size=None, batching=False ,learning_rate=0.001):
        n=len(x_train)
        if batch_size==None: batch_size=n
        self.x_train = x_train
        # ____ setting network optimization
        self.learn=learning_rate
        if self.normalization=="std": self.set_normals(x_train,y_train)
        if self.momentum==True and self.rmsProp==True: optimization=self.Adam
        if self.momentum==True and self.rmsProp==False: optimization=self.Momentum_fun
        if self.momentum==False and self.rmsProp==True: optimization=self.RMSProp_fun
        if self.momentum==False and self.rmsProp==False: optimization=self.no_opt

        for epoch in range(epochs):
            indeces = list(range(n))
            if batching: np.random.shuffle(indeces) # shuffling indeces

            # __________ getting new predictions in new epoch for all branches __________
            for k in range(0,n,batch_size):
                part_in_use = indeces[k:k+batch_size]
                x,y = x_train[part_in_use], y_train[part_in_use]
                #~~~~~
                y_predicted = self.forward(x)
                self.backward(y,y_predicted, optimization_method = optimization)
                #~~~~~

            # __________ saving outputs for showing errors __________
            output = self.forward(x_train)
            self.scores.append(self.measure(output, y_train))
            if epoch in range(1, epochs+1, int(epochs/9)) or epoch==epochs:
                self.epoch_n.append(epoch)
                print_error = self.measure(output, y_train)
                self.errors_array.append(np.sum(self.output_delta))
                self.error_matrix.append(self.output_delta)
            # Print f-score
        if self.measure == self.mse_loss: print(f'Epoch {epoch+1}, Training MSE Score: {print_error}\n')
        if self.measure == self.cross_entropy_loss: print(f'Epoch {epoch+1}, Training Cross-Entropy Score: {print_error}\n')
        return print_error
    
# 4) _____ Gradient implementation ______ ##
    def gradients(self, y, y_predicted):
        n = len(self.weights)
        gradient_biases = [np.zeros(b.shape) for b in self.biases]
        gradient_weights = [np.zeros(w.shape) for w in self.weights]
        if self.measure == self.mse_loss: self.output_delta = self.mse_loss_derivative(y, y_predicted)
        if self.measure == self.cross_entropy_loss: self.output_delta = self.cross_entropy_loss_derivative(y, y_predicted)
        for i in range(1, n+1):
            gradient_biases[-i] = np.sum(self.output_delta, axis=0)
            gradient_weights[-i] = np.dot(self.activated[-i].T, self.output_delta)
            self.output_delta = np.dot(self.output_delta, self.weights[-i].T) * self.derivative(self.summed[-i])
        return gradient_biases,gradient_weights
    
# 5) _______ Predict test data _______ #
    # ___ classification
    def predict_classification(self, x):
        output, _ = self.forward(x)
        return np.argmax(output, axis=1)
    def print_f1_test(self,x_test,y_test):
        print("F1 score test =", self.f1_fun(np.eye(x_test.shape[1])[self.predict_classification(x_test)],y_test))
    # ___ regression
    def predict_regression(self, x_test, y_test):
        indices=[]
        nearest_indices = np.array([np.argmin(np.abs(self.x_train - value)) for value in x_test])
        for i in range(len(nearest_indices)):
            k = int(np.where(np.abs(self.x_train - x_test[i]) == np.min(np.abs(self.x_train - x_test[i])))[0])
            indices.append(k)
        y_predicted = self.forward(self.x_train[indices])
        difference_test = y_test - y_predicted
        return difference_test
    def print_mse_test(self,x_test, y_test):
        difference_test = self.predict_regression(x_test, y_test)
        print("MSE test =", np.mean(np.square(difference_test)))

##
##    
## ________________________________________ Improvements - direction funs ________________________________________ ##
    # 0) ___ normalization of data
    def set_normals(self,x,y):
        self.meanx = np.mean(x)
        self.stdx = np.std(x)
        self.meany = np.mean(y)
        self.stdy = np.std(y)
    def normalize_std(self,x):
        return (x-self.meanx)/self.stdx
    def denormalize_std(self,y_pred):
        return y_pred*self.stdy + self.meany
    def normalize_minmax(self,x):
        return (x-min(x))/(max(x)-min(x))
    def denormalize_minmax(self,y_pred):
        return y_pred*(max(y_pred)-min(y_pred)) + min(y_pred)
    ## 1) ___ improvements - Momentum
    def Momentum_fun(self,G_biases,G_weights, beta = 0.9):
        self.V_biases = [beta*vb+gb for (vb,gb) in zip(self.V_biases, G_biases)]
        self.V_weights = [beta*vw+gw for (vw,gw) in zip(self.V_weights, G_weights)]
        return self.V_biases, self.V_weights
    ## 2) ___ improvements - RMSprop
    def RMSProp_fun(self,G_biases,G_weights,beta = 0.9):
        self.M_biases = [beta*mb + (1-beta)*np.square(gb) for (mb,gb) in zip(self.M_biases,G_biases)]
        self.M_weigths = [beta*mw + (1-beta)*np.square(gw) for (mw,gw) in zip(self.M_weigths,G_weights)]
        # actualization of g function
        eps=1e-15  
        G_biases = [np.divide(gb, np.sqrt(mb)+eps) for (mb,gb) in zip(self.M_biases, G_biases)]
        G_weights = [np.divide(gw, np.sqrt(mw)+eps) for (mw,gw) in zip(self.M_weigths,G_weights)]
        return G_biases, G_weights
    ## 3) ___ Adam - combined RMSprop, momemntum
    def Adam(self, G_biases,G_weights):
        beta1 = 0.9
        beta2= 0.999
        eps=1e-15  
        self.V_biases = [beta1*vb + (1-beta1)*gb for (vb,gb) in zip(self.V_biases,G_biases)]
        self.V_weights = [beta1*vw + (1-beta1)*gw for (vw,gw) in zip(self.V_weights,G_weights)]
        self.M_biases = [beta2*mb + (1-beta2)*np.square(gb) for (mb,gb) in zip(self.M_biases,G_biases)]
        self.M_weigths = [beta2*mw + (1-beta2)*np.square(gw) for (mw,gw) in zip(self.M_weigths,G_weights)]
        G_biases = [np.divide(vw/(1-beta1),np.sqrt(mw/(1-beta2))+eps) for (mw,vw) in zip(self.M_weigths,self.V_weights)]
        G_weights = [np.divide(vb/(1-beta1),np.sqrt(mb/(1-beta2))+eps) for (mb,vb) in zip(self.M_biases,self.V_biases)]
        return G_biases,G_weights
    def no_opt(self, a,b):
        return a,b
## ________________________________________ Visualizations ______________________________________________ ##
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
                im = ax.imshow(error_values.reshape(1, -1), cmap='Blues', aspect='auto', vmin=0, vmax=self.error_matrix[0].max())
                ax.set_title(f'Epoch {self.epoch_n[k]+1}')
                k+=1
        cbar = fig.colorbar(im, ax=axs, orientation='vertical', fraction=0.03, pad=0.1)
        cbar.set_label('Error')
        plt.show()
