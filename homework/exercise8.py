f = open("studentdata.txt", "r")

for aline in f:
    items = aline.split()
    print (items[0],float(sum(items[1:])/len(items[1:]))

f.close()