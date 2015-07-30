import turtle
f = open('labdata.txt','r')
def plotRegression(data):
    turtle.Screen()
    for aline in data:
        items = aline.split()
	items = [int(i) for i in items]
	turtle.setpos(items)
	turtle.dot()

f.close()
