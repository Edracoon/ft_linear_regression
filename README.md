# Introduction in Machine Learning : Linear Regression

Une introduction au machine learning

Hypothèse de type y = a \* x + b:

![Screen Shot 2022-05-11 at 12 51 22 PM](https://user-images.githubusercontent.com/77042040/167832913-a7613b76-8260-4e2e-ba86-74b575587fe9.png)


# The Mean Squared Error :

MSE is the Mean Squared Error of our prediction function y = a * x + b.
It is expressed by E like so :

E = (1/n) * ∑((yi - (a * xi + b)) ** 2)

For n = length of the data ; a = lastly computed a and b = lastly computed 'b' by the linear regression algorithm.

# Gradient Descent Algorithm :

    Calculer la direction de la pente la plus raide
    Puis aller dans la direction opposee : Ce qui va
    nous aider reduire la mean squared error (MSE)
    Pour calculer la pente on va utiliser la derivation de fonction :
        On derive partiellement E(a,b) par rapport a 'a', puis a 'b'
        (partial derivative of E with respect to 'a' or 'b')
    Pour aller dans direction opposee, on soustrait notre derivation a 'a' et 'b', precedemment calcule
    En prenant en compte le LearningRate = les steps plus ou moins grands que l'on va faire faire a notre fonction
        steps grand = trouver vite la solution avec des grands 'pas'
        steps petit = trouver une solution plus precise qui prends en compte les details

# Partial Derivative Formulas :

    # Derivee partielle de E par respect a 'a' = -2/n * SUM(0,n)( xi * (yi - (axi + b)))
    # Derivee partielle de E par respect a 'b' = -2/n * SUM(0,n)( yi - (axi + b))
