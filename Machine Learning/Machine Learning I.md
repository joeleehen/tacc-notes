# Machine Learning I
## Intro to ML
##### Formal Definition
A computer program is said to learn from experience $E$ with respect to some class of tasks $T$ and performance measure $P$, if its performance at the tasks improves with the experiences.
For example, recognizing hand written words within images:
- **Task**: recognize hand written words within images
- **Performance**: percent of words classified correctly
- **Experience**: database of classified hand written words

#### Common Task for "Learning"
- Supervised Learning: data has labels
- Unsupervised Learning: data has NO labels
- Reinforcement Learning: learn from making mistakes
We're focused on supervised learning for today.

### Workflow
##### Training
The process for making a model. Training data is the data "observed" by the learning model.
##### Testing
Process for evaluating the performance of the model. Testing data is NOT observed by the learning model.
##### 80/20 Split
80% available are randomly selected for training, the remaining 20% are used for testing.
##### Prediction
Apply model to data not in either training or testing dataset. Assume the input dat and its prediction are from the same process producing the training data. Note, it is important that the data used for prediction is *relevant* to the data used for training and testing.
"I I build a model for estimating house prices in Alabama, feeding it home data for Los Angeles is an improper fit!"

## Supervised Learning Techniques 
### k-Nearest Neighbors
If two data objects are similar, they are likely from the same **class**.
#### Workflows
Start with a set of data objects with class labels.
Given a distance (similarity) measure of comparing data, compute distance from *unseen data point* to all data in training set.
Retrieve $k$ nearest neighbors for the unknown data.
Assign class label based on the retrieved record.
$k$ is a **hyperparameter**! Hyperparameters are parameters users select that will impact the performance of ML models.
![[Screenshot 2024-10-29 at 11.08.25 AM.png|600]]
#### Decision Boundary for Nearest Neighbor Classification
For a simple binary classification case:
![[Screenshot 2024-10-29 at 11.10.01 AM.png|600]]
We score ~85% with 10 neighbors between our training and testing data.
![[Screenshot 2024-10-29 at 11.11.09 AM.png|300]]
With 1 neighbor, our training score increases to 100%! But test score plummets to 67%, we've *overfit* our data!
![[Screenshot 2024-10-29 at 11.12.30 AM.png|400]]
When we increase $k$ to 50 neighbors, our model performs worse for both training and testing data. We've *underfit* our data.

#### Underfitting vs Overfitting
**Underfitting**: the model can't reflect all the relations from training data; model performs poorly on training and testing data! It 'failed to learn'
**Overfitting**: Model may lead to poor generalization on new testing data; performs very well on training data but poorly on testing data.

#### Classification: Additional Evaluation Metrics
Let's say we build a model predicting whether a patient has cancer:

|                     | Predicted - Cancer | Predicted - NOT Cancer |
| ------------------- | ------------------ | ---------------------- |
| Actual - Cancer     | 0                  | 30                     |
| Actual - NOT Cancer | 0                  | 270                    |
This is a bad model, but we have an accuracy of 90% (270/300)
We rely on a *Confusion Matrix* for some notation:
 
|                   | Predicted (Positive) | Predicted - Negative |
| ----------------- | -------------------- | -------------------- |
| Actual (Positive) | True Positive (TP))  | False Negative (FN)  |
| Actual (Negative) | False Positive (FP)  | True Negative (TN)   |
$$ Recall = \frac{TP}{TP + FN}$$
$$Precision = \frac{TP}{TP + FP}$$
Our $Recall$ score for this model ($\frac{Predicted Cancer}{Total Data Points})$ is 0! Model sucks!

### Linear Regression
We train our model by minimizing "errors". The basic idea of many ML applications is to minimize some loss function. For linear regressions, we use *Ordinary Least squares*:
$$OLS: \sum^n_{i=1}(f(x_i, \theta) - y_i)^2$$
where $\theta$ is some tuple of coefficients $(a, b)$ that minimize our loss over $y=ax + b$.

We can have *multiple* independent variables in our multiple linear regression.
$x$ is a vector of features, $x \in R^N$
$\theta$ is a vector of weights, $\theta \in R^N$
##### Pros
- Linear regression is simple
- Very interpretable!
	- Slopes, $a$, can be defined as: "Holding all else constant, for 1 unit increase in feature $x_i$ the target variable increases by $a_i$"
##### Cons
- not all features in your data have linear relationships with the target
- you need to transform features such that a linear relationship exists to get good results (usually by logging/squaring your independent variables). This is called *feature engineering*.

### Logistic Regression
(Binary) logistic regressions are used for classification problems with a (binary) dependent variable.
$y$ can only take two values, usually 0 and 1. Think boolean dependents (pass/fail, positive/negative, healthy/sick).
We have one or more independent variables $x$.
We predict the probability of a binary response.
$$probability=f(x, \theta) = b + a_0 x_0 + a_1 x_1 + \dots + a_N x_N$$
Our Logistic function $\sigma(t)$ converts log odds ratio to probabilities:
$$\sigma(t) = \frac{1}{1+e^{-t}}$$
Our loss function is given by $$- \sum^n_{i=1} y_i log(p_i)+(1-y_i)log(1-p_i)$$
