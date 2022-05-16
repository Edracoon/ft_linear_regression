import sys
# Library used for real world data analysis : intuitive data sets (SCV)
import pandas as panda
# Library used for plotting the data on graphs (scatter) (Plotting = 'tracage')
import matplotlib.pyplot as plot

DEBUG = False
if (len(sys.argv) > 1 and sys.argv[1] == '-debug') :
    DEBUG = True


INT_MAX = float(4 ** 16)
INT_MIN = float(-1 * (4 ** 16))

data = panda.read_csv('data.csv') # Recuperer et parser le .csv

# MSE: E = (1/n) * SUM(0,n)((yi - (a * xi + b)) ** 2)
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
def mean_squared_error(a, b, data):
    n = len(data)
    mse = 0

    i = 0
    for i in range(n):
        x = data[0][i]
        y = data[1][i]
        mse +=  (y - (a * x + b)) ** 2
    mse = (1/n) * mse
    return mse

def gradientDescentAlgorithm(curr_a, curr_b, data, LearningRate):
    n = float(len(data[0]))
    a_step = 0
    b_step = 0

    for i in range(len(data[0])):
        x = data[0][i]
        y = data[1][i]
        a_step += (1/n) * ((2 * x) * ((curr_a * x + curr_b) - y))
        b_step += (1/n) * (2 * ((curr_a * x + curr_b) - y))

    # On soustrait donc notre descente pour aller dans le sens opposer et reduire les erreurs
    a = curr_a - LearningRate * a_step
    b = curr_b - LearningRate * b_step
    
    return a, b

def getMinMax(data):
    xmin = INT_MAX
    xmax = INT_MIN
    ymin = INT_MAX
    ymax = INT_MIN
    r = len(data)
    for i in range(r) :
        if float(data.iloc[i, 0]) < xmin :
            xmin = float(data.iloc[i, 0])
        if float(data.iloc[i, 0]) > xmax :
            xmax = float(data.iloc[i, 0])
        if float(data.iloc[i, 1]) < ymin :
            ymin = float(data.iloc[i, 1])
        if float(data.iloc[i, 1]) > ymax :
            ymax = float(data.iloc[i, 1])
    return xmin, xmax, ymin, ymax

def normalizeData(data):
    xmin, xmax, ymin, ymax = getMinMax(data)

    dataX = []
    dataY = []
    for i in range(len(data)):
        x = data.iloc[i, 0]
        y = data.iloc[i, 1]
        newX = (x - xmin) / (xmax - xmin) # Normalization Formula for X
        newY = (y - ymin) / (ymax - ymin) # Normalization Formula for Y
        dataX.append(newX)
        dataY.append(newY)
    return [dataX, dataY]



a = 0
b = 0
LearningRate = 0.2
LearningIteration = 0

normalizedData = normalizeData(data)

if DEBUG :
    print('x\t\t\ty')
    for i in range(len(normalizedData[0])):
        print(normalizedData[0][i], '\t', normalizedData[1][i])

delta_mse = -1
while abs(delta_mse) > 0.000000001:                                     # We want a precise delta before ending the learning
    previous_mse = mean_squared_error(a, b, normalizedData)             # Previous SE
    a, b = gradientDescentAlgorithm(a, b, normalizedData, LearningRate) # Compute a step
    delta_mse = previous_mse - mean_squared_error(a, b, normalizedData) # Difference between Previous and Current MSE

    if DEBUG and LearningIteration % 50 == 0:
        print(f"--------------------\na = {a}\nb = {b}")
        print(f"delta_mse = {delta_mse}\n--------------------")
    
    LearningIteration += 1


print('-------------------- Final Result --------------------')
print(f"Normalized a = {a} b = {b}")

xmin, xmax, ymin, ymax = getMinMax(data)

real_a = a * (ymax - ymin) / (xmax - xmin)
real_b = ymin + ((ymax - ymin) * b) + real_a * (-xmin)
print(f"Unnormalized a = {real_a} b = {real_b}")
print(f"y = ax + b")
print(f"y = {round(real_a,4)}x + {round(real_b,4)}")
# Creat 2x2 Visu
figure, axis = plot.subplots(2, 2)

# Vizualize Real Values
r = range(int(xmin), int(xmax), 1000)
axis[0, 0].set_title("Real Values")
axis[0, 0].scatter(data.km, data.price, color="blue")
axis[1, 0].scatter(data.km, data.price, color="blue")
axis[1, 0].plot(list(r), [real_a * x + real_b for x in r], color="red") # Imprimer notre function ax + b sur le graph

# Vizualize Normalized Values
r = range(0, 2, 1)
axis[0, 1].set_title("Normalized Values")
axis[0, 1].scatter(normalizedData[0], normalizedData[1], color="blue")
axis[1, 1].scatter(normalizedData[0], normalizedData[1], color="blue")
axis[1, 1].plot(list(r), [a * x + b for x in r], color="red") # Imprimer notre function ax + b sur le graph

# Save a and b in a file
file = open("save.csv", "w")
file.write(f"{real_a} {real_b}")
file.close()

# Print Visualization
plot.setp(axis[:], xlabel="Kilometters")
plot.setp(axis[:], ylabel="Price")
plot.show()
