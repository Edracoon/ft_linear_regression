try:
    file = open("save.csv", 'r')
except:
    print('Error: file \"save.csv\" not found.')
    exit(0)
a, b = file.read().split(' ')
x = input("Enter a kilometer: ")
print('Predicted price: ', float(a) * float(x) + float(b))
