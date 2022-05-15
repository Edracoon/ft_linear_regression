# Library used for real world data analysis : intuitive data sets (SCV)
import pandas as panda

# Library used for plotting the data on graphs (scatter) (Plotting = 'tracage')
import matplotlib.pyplot as plot

data = panda.read_csv('data_test.csv') # Recuperer et parser le .csv

print(data)

# MSE: E = (1/n) * SUM(0,n)((yi - (a * xi + b)) ** 2)
# y = ax + b
def mean_squared_error(a, b, data):
    n = len(data)
    mse = 0

    i = 0
    while i < n:                # range(n) retourne un tableau de nombre de 0 a n
        x = data.iloc[i].km     # ligne du tableau a l'index i en precisant la column km
        y = data.iloc[i].price
        mse +=  (y - (a * x + b)) ** 2
        i += 1
    mse = (1/n) * mse # <=> (mse / n)

# Gradient Descent Algorithm :
    # Calculer la direction de la pente la plus raide
    # Puis aller dans la direction opposee : Ce qui va
    # nous aider reduire la mean squared error (MSE)
    # Pour calculer la pente on va utiliser la derivation de fonction :
        # On derive partiellement E(a,b) par rapport a 'a', puis a 'b'
        # -> partial derivative of E with respect to 'a' or 'b'
    # Pour aller dans direction opposee, on soustrait notre derivation a 'a' et 'b', precedemment calcule
    # En prenant en compte le LearningRate = les steps plus ou moins grands que l'on va faire faire a notre fonction
        # steps grand = trouver vite la solution avec des grands 'pas'
        # steps petit = trouver une solution plus precise qui prends en compte les details

    # Formule :
    # Derivee partielle de E par respect a 'a' = -2/n * SUM(0,n)( xi * (yi - (axi + b)))
    # Derivee partielle de E par respect a 'b' = -2/n * SUM(0,n)( yi - (axi + b))
def gradient_descent_algorithm(curr_a, curr_b, data_values, LearningRate):
    n = float(len(data_values))
    a_step = 0 # Notre derivation de E par respect a 'a' (gradient)
    b_step = 0 # Notre derivation de E par respect a 'b' (gradient)

    for i in range(len(data_values)):
        x = data_values.iloc[i, 0]
        y = data_values.iloc[i, 1]
        # print(i, x, y)

        # (1/n) * SUM(0,n)((yi - (a * xi + b)) ** 2) = derivee de E par a = -(2/n) * x * (y - (curr_a * x + curr_b))
        
        # a_step += -(2/n) * x * (y - (curr_a * x + curr_b))
        # b_step += -(2/n) * (y - (curr_a * x + curr_b))
        a_step += (1/n) * ((2 * x) * ((curr_a * x + curr_b) - y))
        b_step += (1/n) * (2 * ((curr_a * x + curr_b) - y))

    # On soustrait donc notre descente pour aller dans le sens opposer et reduire les erreurs
    
    a = curr_a - LearningRate * a_step
    b = curr_b - LearningRate * b_step
    
    return a, b

def gradient_descent(m_now, b_now, points, L):
    m_gradient = 0
    b_gradient = 0
    n = float(len(points))
    for i in range(len(points)):
        x = points.iloc[i, 0]
        y = points.iloc[i, 1]
        m_gradient += -(2/n) * x * (y - (m_now * x + b_now))
        b_gradient += -(2/n) * (y - (m_now * x + b_now))
    m = m_now - L * m_gradient
    b = b_now - L * b_gradient
    return [m, b]

# ============================ #
# ===== Learning Process ===== #
# ======== y = ax + b ======== #
# a = 0
# b = 0
# LearningRate = 0.0001
# LearningIteration = 20

# for i in range(LearningIteration):
#     a, b = gradient_descent(a, b, data, LearningRate)
#     print(f"{i} -> {a} {b}")


m = 0
b = 0
L = 0.001
epochs = 10000

for i in range(epochs):
    m, b = gradient_descent(m, b, data, L)
    print(m, b)

print(m, b)

plot.scatter(data.x, data.y, color="blue")

r = range(0, 100, 1)
plot.plot(list(r), [m * x + b for x in r], color="red")

plot.show()
