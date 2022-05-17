a, b = open("save.csv", 'r').read().split(' ')
x = input("Enter a kilometter: ")
print('Predicted price: ', float(a) * float(x) + float(b))
