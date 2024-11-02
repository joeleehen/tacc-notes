# Deep Learning
Deep learning is a subset of machine learning based on neural networks that permit a machine to train itself to perform a task.
Machine learning requires some kind of *feature extraction*, which involves describing your data with features a computer can understand. this is very hard! and requires Ph.D. level of domain specific talent!
Deep learning, on the other hand, abstracts feature extraction away from the user. Feature extraction is handled by the neural network rather than the guy.

## Multilayer Perceptrons (MPLs)
First, some notation:
$$\begin{matrix} TODO \\ slide\\51 \end{matrix}$$

MLPs can be expressed as a directed (not necessarily acyclic) graph.
The image below shows a multilinear regression with two independent variables, represented as a directed graph:
![[Screenshot 2024-10-29 at 1.02.40 PM.png|400]]
Similarly, we can represent a [[Machine Learning I#Logistic Regression|logistic regression]] in the same way!
![[Screenshot 2024-10-29 at 1.04.02 PM.png|400]]

Let's expand this logistic regression with a single *hidden layer*. This hidden layer has two neurons. We call it a 'hidden' layer since a multilayered perceptron is a strictly determinant output; we expect one output for any given input. Any in-between 'output' that isn't the output we care about is hidden.
![[Screenshot 2024-10-29 at 1.07.55 PM.png|400]]

Alternatively, we can represent this MLP using matrix notation:
$$\text{Input Layer: } x = \begin{bmatrix} x_1, x_2\end{bmatrix}$$
$$\text{Input Weights: }w^{(1)} = \begin{bmatrix} w_{111} & w_{112} \\ w_{121} & w_{122}\end{bmatrix}$$
$$\text{Layer 1 Output: } o^{(1)} = \sigma \left( (w^{(1)})^Tx \right) \; \; \text{where } \sigma \text{ is our activation function (sigmoid, ReLU, etc.)}$$
$$\text{Layer 2 Output: } o^{(2)} = \left( (w^{(2)})^T o^{(1)}\right)$$

Layers in MLP are called **fully connected layer**s. Neurons in each layer are fully connected to the neurons in the following layer.
### Activation Functions
We map specific activation functions within a node to determine the output of a specific output node. Most important to MLPs is the *Rectified linear unit* (RELU) function.
We use activation functions (rather than more linear/logistic regressions) to allow use to find non-linear relationships. More layers and neurons can approximate more complex functions.
Activation functions enable neural networks to learn non-linear relationships!

## Training
What are the optimal values for the weight matrices?
This is similar to optimizing a linear regression! We still need
- data
- a loss function
- a numerical optimizer to minimize loss functions
### Gradient Descent
Gradient Descent is an iterative optimization algorithm used for minimizing functions.
Say we're minimizing a function $f(x)$:
$$x^{t+1} = s^t-\alpha^t \nabla f(x^t), \; t=0,1,2,...,$$
### Loss Functions
There are a few common loss functions for regressions; we typically see least absolute deviations or ordinary least squares. Most loss functions include some $\frac{1}{N}$ term since we're taking an average over all our training points. We can think of a loss function as an *average per data point loss*!
$$L(x,y,\theta) = \frac{1}{N} \sum^N_{i=1}l(x,y, \theta)$$
Iterating over your entire data set can be *very* costly. Since we're taking an average, we can extract a sample and get an estimation of average per data point loss to make the iteration cost cheaper!
For a number of iterations:
We compute the gradients: $g = \frac{1}{n} \sum^n_{i-=1} \nabla_\theta l(x, y, \theta)$
We update the weights: $\theta_{i+1} = \theta_i -\alpha g$
The sample we pull from the training data is called a *batch*. We use $n$ to denote the size of our batch.
When using mini batch gradient descent, we need to specify the batch size, or the umber of data points used to approximate gradients. The number of mini batch iterations needed to sample the entire training set is an **epoch**.
For 1,200,000 images with a 512 mini-batch size, an epoch takes ~2400 iterations.
$$\text{Gradient Descent: }\; \;  \begin{matrix} \text{compute gradients: } g=\sum^N_{i=1} \nabla_\theta l(x,y, \theta) \\ \text{update weights: } \theta_{i+1} = \theta_i - \alpha g\end{matrix}$$
$\alpha$ is the **learning rate**! It controls the interval between each compute-gradient iteration. A small $\alpha$ will descend very slowly and take a long time to find the minimum. A large $\alpha$ might skip over the minimum altogether!
Remember, $\theta$ is a $\underline{vector}$ of weights! We evaluate each partial differential of the gradient at all values of our sample batch and get a vector of scalar weights.

---
## Hands-On: Hurricane Harvey Image Classification
We have a bunch of images of house damage from Hurricane Harvey. We will classify each image as Low (C0), Medium (C2), or High (C4) Damage using a convolutional neural network.