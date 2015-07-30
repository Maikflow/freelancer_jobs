import os
import matplotlib.pyplot as plt
import operator
import math

SW = ( 'a','able','about','across','after','all','almost','also','am','among','an','and','any','are','as','at','be','because','been','but','by','can','cannot','could','dear','did','do','does','either','else','ever','every','for','from','get','got','had','has','have','he','her','hers','him','his','how','however','i','if','in','into','is','it','its','just','least','let','like','likely','may','me','might','most','must','my','neither','no','nor','not','of','off','often','on','only','or','other','our','own','rather','said','say','says','she','should','since','so','some','than','that','the','their','them','then','there','these','they','this','tis','to','too','twas','us','wants','was','we','were','what','when','where','which','while','who','whom','why','will','with','would','yet','you','your' )

CC = ( ("aren't","are not"),("can't","can not"),("could've","could have"),("couldn't","could not"),("couldn't've","could not have"),("didn't","did not"),("doesn't","does not"),("don't","do not"),("hadn't","had not"),("hadn't've","had not have"),("hasn't","has not"),("haven't","have not"),("he'd","he had"),("he'd've","he would have"),("he'll","he will"),("he's","he is"),("how'd","how did"),("how'll","how will"),("how's","how has"),("I'd","I had"),("I'd've","I would have"),("I'll","I will"),("I'm","I am"),("I've","I have"),("isn't","is not"),("it'd","it had"),("it'd've","it would have"),("it'll","it will"),("it's","it is"),("let's","let us"),("ma'am","madam"),("mightn't","might not"),("mightn't've","might not have"),("might've","might have"),("mustn't","must not"),("must've","must have"),("needn't","need not"),("not've","not have"),("o'clock","of the clock"),("shan't","shall not"),("she'd","she had"),("she'd've","she would have"),("she'll","she will"),("she's","she is"),("should've","should have"),("shouldn't","should not"),("shouldn't've","should not have"),("that's","that is"),("there'd","there had"),("there'd've","there would have"),("there're","there are"),("there's","there is"),("they'd","they had"),("they'd've","they would have"),("they'll","they will"),("they're","they are"),("they've","they have"),("wasn't","was not"),("we'd","we had"),("we'd've","we would have"),("we'll","we will"),("we're","we are"),("we've","we have"),("weren't","were not"),("what'll","what will"),("what're","what are"),("what's","what is"),("what've","what have"),("when's","when is"),("where'd","where did"),("where's","where is"),("where've","where have"),("who'd","who had"),("who'll","who will"),("who're","who are"),("who's","who is"),("who've","who have"),("why'll","why will"),("why're","why are"),("why's","why is"),("won't","will not"),("would've","would have"),("wouldn't","would not"),("wouldn't've","would not have"),("y'all","you all"),("y'all'd've","you all would have"),("you'd","you had"),("you'd've","you would have"),("you'll","you will"),("you're","you are"),("you've","you have"),("-"," ") )

def stemmer(word):
	if word[-4:] not in ['eies', 'aies'] and word[-3:] == 'ies':
		word = word[:-3] + 'y'
	if word[-3:] not in ['aes', 'ees', 'oes'] and word[-2:]=='es':
		word = word[:-1] + 'e'
	if word[-2:] not in ['us' or 'ss'] and word[-1:] == 's':
		word = word[:-1]
        endings = ('able','al','ance','ant','ar','ary','ate','ement','ence'
                    'ent','er','ess','ible','ic','ify','ine''ion','ism','iti','ity'
                    'ive','ize','ly','ment','or','ou','ous','th','ure')       
        for suffix in endings:
            if word.endswith(suffix) and len(word) >= len(suffix)+2:
                word = word[:-len(suffix)]
	return(word)

def parse(S,D):
	for w in [stemmer(w).strip(".,:;!?") for w in S.split() if w not in SW]:
		if w in D:
			D[w] = D[w]+1
		else:
			D[w] = 1

def readInput(filename):
	D = {}
	infile = open(filename, 'r')
	for line in infile:
		for (x,y) in CC:
			line = line.lower().replace(x,y)
		parse(line,D)
	infile.close()
	return(D)
	
def topK(D,k):
	L = [ (item, D[item]) for item in D.keys()]
	return(sorted(L, reverse=True, key = lambda x: x[1])[0:k])
	
def extractTerms(filelist, corpusTerms):
    """extract term frequency dictionary from filelist"""
    tfds = []
    for file_no in filelist:
        D = (readInput(file_no))
        for word in D.keys():
            if word in corpusTerms.keys():
                corpusTerms[word] += 1
            else:
                corpusTerms[word] = 1
        tfds.append(D) 
    return tfds

def createModels(tfds, cfd, k):
    """return k-tuple of word terms and list of N-tuples"""
    # vectors go here
    model = []
    terms = dict(topK(cfd,k))
    doc_lenght = sum(terms.values())
    for document in tfds:
        temp = []
        for term in terms.keys():
            try:
                tfi = document[term]/float(doc_lenght)
            except KeyError:
                tfi = 0
            wi = tfi *math.log((len(tfds)/float(1+cfd[term])),10)
            temp.append(wi)
        model.append(tuple(temp))
    new_model = []
    for vector in model:
        u = sum([math.sqrt(x**2) for x in vector])
        tmp = []
        for element in vector:
            tmp.append(element/u)
        new_model.append(tuple(tmp))
    return (terms.keys(), new_model)

def dotProduct(k):
    p = os.path.join(os.path.curdir, 'corpus')+'/'    
    presidents = []
    for file in os.listdir("corpus"):
        if file.endswith(".txt"):
            presidents.append(file)
    presidents = sorted(presidents)
    unknowns = ['unknown0.txt','unknown1.txt','unknown2.txt','unknown3.txt','unknown4.txt']
    for unk in unknowns:
        presidents.remove(unk)
    cfd = {}
    dotp = {}

    #calculate dot products for each president
    for presi in range(len(presidents[::4])):
        tfds = extractTerms([p+presidents[presi],p+presidents[presi+1],p+presidents[presi+2],p+presidents[presi+3]], cfd)
        terms, models = createModels(tfds,cfd,k)
        dotProduct1 = reduce( operator.add, map( operator.mul, models[0], models[1]))
        dotProduct2 = reduce( operator.add, map( operator.mul, models[0], models[2]))
        dotProduct3 = reduce( operator.add, map( operator.mul, models[0], models[3]))
        dotProduct4 = reduce( operator.add, map( operator.mul, models[1], models[2]))
        dotProduct5 = reduce( operator.add, map( operator.mul, models[2], models[3]))
        dotProduct6 = reduce( operator.add, map( operator.mul, models[3], models[1]))
        DP = (dotProduct1 + dotProduct2 + dotProduct3 + dotProduct4 + dotProduct5 + dotProduct6)/6
        dotp[presidents[presi]] = DP

    # Make histogram 
    plt.hist(dotp.values())
    plt.show()

    #Compute vector model of 5 unknown documents
    tfds = extractTerms([p+unknowns[0],p+unknowns[1],p+unknowns[2],p+unknowns[3],p+unknowns[4]], cfd)
    terms, models = createModels(tfds,cfd,k)
    dotProduct1 = reduce( operator.add, map( operator.mul, models[0], models[1]))
    dotProduct2 = reduce( operator.add, map( operator.mul, models[0], models[2]))
    dotProduct3 = reduce( operator.add, map( operator.mul, models[0], models[3]))
    dotProduct4 = reduce( operator.add, map( operator.mul, models[1], models[2]))
    dotProduct5 = reduce( operator.add, map( operator.mul, models[2], models[3]))
    dotProduct6 = reduce( operator.add, map( operator.mul, models[3], models[1]))
    DP = (dotProduct1 + dotProduct2 + dotProduct3 + dotProduct4 + dotProduct5 + dotProduct6)/6
    dotp['unknown'] = DP
    print dotp


dotProduct(100)
