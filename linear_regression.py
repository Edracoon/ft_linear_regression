import sys
# Library used for plotting the data on graphs (scatter) (Plotting = 'tracage')
import matplotlib.pyplot as plot

# === Defines === #
DEBUG = False
INT_MAX = float(4 ** 16)
INT_MIN = float(-1 * (4 ** 16))
if (len(sys.argv) > 1 and sys.argv[1] == '-debug'):
    DEBUG = True


# === Read and Parse CSV File === #
def parseFileCSV():
    lines = open("data.csv").read().split('\n')
    dataX = []
    dataY = []
    i = 0
    for line in lines:
        if i > 0:
            x, y = line.split(',')
            dataX.append(int(x))
            dataY.append(int(y))
        i += 1
    return [dataX, dataY]


def mean_squared_error(a, b, data):
    n = len(data)
    mse = 0

    i = 0
    for i in range(n):
        x = data[0][i]
        y = data[1][i]
        mse += (y - (a * x + b)) ** 2
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

    a = curr_a - LearningRate * a_step
    b = curr_b - LearningRate * b_step

    return a, b


def getMinMax(data):
    xmin = INT_MAX
    xmax = INT_MIN
    ymin = INT_MAX
    ymax = INT_MIN
    for i in range(len(data[0])):
        if data[0][i] < xmin:
            xmin = data[0][i]
        if data[0][i] > xmax:
            xmax = data[0][i]
        if data[1][i] < ymin:
            ymin = data[1][i]
        if data[1][i] > ymax:
            ymax = data[1][i]
    return xmin, xmax, ymin, ymax


def normalizeData(data):
    xmin, xmax, ymin, ymax = getMinMax(data)
    dataX = []
    dataY = []
    for i in range(len(data[0])):
        x = data[0][i]
        y = data[1][i]
        newX = (x - xmin) / (xmax - xmin)
        newY = (y - ymin) / (ymax - ymin)
        dataX.append(newX)
        dataY.append(newY)
    return [dataX, dataY]


# ================================= Main ==================================== #

data = parseFileCSV()
normData = normalizeData(data)

a = 0
b = 0
LearningRate = 0.01
Iteration = 0
delta_mse = -1

if DEBUG:
    print('x\t\t\ty')
    for i in range(len(normData[0])):
        print(normData[0][i], '\t', normData[1][i])


# We want a precise delta before ending the learning
while abs(delta_mse) > 0.000000001:
    previous_mse = mean_squared_error(a, b, normData)
    a, b = gradientDescentAlgorithm(a, b, normData, LearningRate)

    # Difference between Previous and Current MSE
    delta_mse = previous_mse - mean_squared_error(a, b, normData)

    if DEBUG and Iteration % 50 == 0:
        print(f"--------------------\na = {a}\nb = {b}")
        print(f"delta_mse = {delta_mse}\n--------------------")

    Iteration += 1


print('-------------------- Final Result --------------------')
print(f"Normalized a = {a} b = {b}")

xmin, xmax, ymin, ymax = getMinMax(data)

real_a = a * (ymax - ymin) / (xmax - xmin)
real_b = ymin + ((ymax - ymin) * b) + real_a * (-xmin)
print(f"Unnormalized a = {real_a} b = {real_b}")
print(f"y = ax + b")
print(f"y = {round(real_a,4)}x + {round(real_b,4)}")


# Create 2x2 Visual
figure, axis = plot.subplots(2, 2)

# Vizualize Real Values
r = range(int(xmin), int(xmax), 1000)
axis[0, 0].set_title("Real Values")
axis[0, 0].scatter(data[0], data[1], color="blue")
axis[1, 0].scatter(data[0], data[1], color="blue")
# Imprimer notre function ax + b sur le graph
axis[1, 0].plot(list(r), [real_a * x + real_b for x in r], color="red")

# Vizualize Normalized Values
r = range(0, 2, 1)
axis[0, 1].set_title("Normalized Values")
axis[0, 1].scatter(normData[0], normData[1], color="blue")
axis[1, 1].scatter(normData[0], normData[1], color="blue")
# Imprimer notre function ax + b sur le graph
axis[1, 1].plot(list(r), [a * x + b for x in r], color="red")

# Save a and b in a file
file = open("save.csv", "w")
file.write(f"{real_a} {real_b}")
file.close()

# Print Visualization
plot.setp(axis[:], xlabel="Kilometters")
plot.setp(axis[:], ylabel="Price")
plot.show()
