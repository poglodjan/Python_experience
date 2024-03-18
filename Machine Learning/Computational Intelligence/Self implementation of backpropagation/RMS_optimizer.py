import numpy as np 
import matplotlib.pyplot as plt 
from numpy import arange, meshgrid
def objective(x1, x2): 
    return 5 * x1**2.0 + 7 * x2**2.0
  
def derivative_x1(x1, x2): 
    return 10.0 * x1 
  
def derivative_x2(x1, x2): 
    return 14.0 * x2
  
x1 = arange(-5.0, 5.0, 0.1) 
x2 = arange(-5.0, 5.0, 0.1) 

x1, x2 = meshgrid(x1, x2) 
y = objective(x1, x2) 
fig = plt.figure(figsize=(12, 4)) 

# Plot 1 - 3D plot 
ax = fig.add_subplot(1, 2, 1, projection='3d') 
ax.plot_surface(x1, x2, y, cmap='viridis') 
ax.set_xlabel('x1') 
ax.set_ylabel('x2') 
ax.set_zlabel('y') 
ax.set_title('3D plot of the objective function') 

# Plot 2 - Contour plot 2D plot
ax = fig.add_subplot(1, 2, 2) 
ax.contour(x1, x2, y, cmap='viridis', levels=20) 
ax.set_xlabel('x1') 
ax.set_ylabel('x2') 
ax.set_title('Contour plot of the objective function') 
plt.show()

# Defining the RMSprop optimizer 
def rmsprop(x1, x2, derivative_x1, derivative_x2, learning_rate, gamma, epsilon, max_epochs): 
	x1_trajectory = [] 
	x2_trajectory = [] 
	y_trajectory = [] 
	x1_trajectory.append(x1) 
	x2_trajectory.append(x2) 
	y_trajectory.append(objective(x1, x2)) 

	e1 = 0
	e2 = 0

	for I in range(max_epochs): 
		gt_x1 = derivative_x1(x1, x2) 
		gt_x2 = derivative_x2(x1, x2) 
		e1 = gamma * e1 + (1 - gamma) * gt_x1**2.0
		e2 = gamma * e2 + (1 - gamma) * gt_x2**2.0

		x1 = x1 - learning_rate * gt_x1 / (np.sqrt(e1 + epsilon)) 
		x2 = x2 - learning_rate * gt_x2 / (np.sqrt(e2 + epsilon)) 
 
		x1_trajectory.append(x1) 
		x2_trajectory.append(x2) 
		y_trajectory.append(objective(x1, x2)) 

	return x1_trajectory, x2_trajectory, y_trajectory

x1_initial = -4.0
x2_initial = 3.0
learning_rate = 0.1
gamma = 0.9
epsilon = 1e-8
max_epochs = 50

x1_trajectory, x2_trajectory, y_trajectory = rmsprop(x1_initial, x2_initial, derivative_x1, derivative_x2, learning_rate, gamma, epsilon, max_epochs) 

# Printing the optimal values of x1, x2, and y 
print('The optimal value of x1 is:', x1_trajectory[-1]) 
print('The optimal value of x2 is:', x2_trajectory[-1]) 
print('The optimal value of y is:', y_trajectory[-1])

fig = plt.figure(figsize=(6, 6)) 
ax = fig.add_subplot(1, 1, 1) 

ax.contour(x1, x2, y, cmap='viridis', levels=20) 

ax.plot(x1_trajectory, x2_trajectory, '*', 
		markersize=7, color='dodgerblue') 

ax.set_xlabel('x1') 
ax.set_ylabel('x2') 
ax.set_title('RMSprop Optimization path for ' + str(max_epochs) + ' iterations') 

plt.show()
