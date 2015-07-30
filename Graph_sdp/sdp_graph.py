import pygraphviz as viz
import codecs
import os

#look for .sdp files in current directory
for files in os.listdir(os.curdir):
    if files.endswith('.sdp'):
        _file = files

#open .sdp file, split by tabs and append to sdp_file list
sdp_file = []
with codecs.open(_file,'r','utf-8') as sdp:
    for row in sdp:
        sdp_file.append(row.strip('\n').split('\t'))

#Initialize lists to get all necesary points
graphs = []
edges = []
weights = []
nodes = []
temp = []
temp2 = []
temp3 = []
sentence = []

gr = viz.AGraph()
for y,row in enumerate(sdp_file):

    #Only get rows that have a 2nd column
    try:
        if row[1] == '%':
            row[1] = ' %'
        gr.add_node(row[1])
        temp3.append(row[1])
        if '+' in str(row[5]).strip(' '):
            temp.append(int(row[0])-1) 
        
        #get the weight columns (7-last)
        w_columns = row[6:]
        for x,weight in enumerate(w_columns):
            if (str(weight).strip(' ') != '-' and 
                str(weight).strip(' ') != '_' 
                ):
                #print type(weight),len(weight), str(weight)
                temp2.append([int(row[0])-1,x, weight])

    #When it finds a new sentence append and reset
    except IndexError:
        #print row[0]
        sentence.append(row[0])
        graphs.append(gr)
        gr = viz.AGraph(encoding='UTF-8')
        nodes.append(temp3)
        weights.append(temp2)
        edges.append(temp)
        temp = []
        temp2 = []
        temp3 = []

edges = edges[1::2]
weights = weights[1::2]
nodes = nodes[1::2]
#print 'SENTENCES', sentencearjclear()j
#print 'EDGES ', edges[0]
#print 'WEIGHTS',weights[0]
#print 'NODES', nodes[0]

#Compute and add edges to graph
for i,gr in enumerate(graphs[1::2]):
    for weight in weights[i]:
        try:
            gr.add_edge(nodes[i][edges[i][weight[1]]],
                        nodes[i][weight[0]])
            edge = gr.get_edge(nodes[i][edges[i][weight[1]]],
                    nodes[i][weight[0]])
            edge.attr['label'] = weight[2]
            edge.attr['dir'] = 'forward'
        except TypeError:
            print 'there was an error'
        except IndexError:
            print nodes[i]
            print edges[i]
            print weight[1]

#Draw a DAE for each graph in graphs        
for i,gr in enumerate(graphs[1::]):
    gr.draw('{}.png'.format(str(sentence[i])),prog='dot',format='png')

