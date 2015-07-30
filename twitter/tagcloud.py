import requests, collections, operator
from pytagcloud import create_tag_image, create_html_data, make_tags, LAYOUT_HORIZONTAL, LAYOUTS, LAYOUT_MIX, LAYOUT_VERTICAL, LAYOUT_MOST_HORIZONTAL, LAYOUT_MOST_VERTICAL
from pytagcloud.colors import COLOR_SCHEMES
from pytagcloud.lang.counter import get_tag_counts

def make_cloud(text,fname):
    '''create the wordcloud from variable text'''
    Data1 = text.lower().replace('http','').replace('rt ','').replace('.co','')
    Data = Data1.split()
    two_words = [' '.join(ws) for ws in zip(Data, Data[1:])]
    wordscount = {w:f for w, f in collections.Counter(two_words).most_common() if f > 200}
    sorted_wordscount = sorted(wordscount.iteritems(), key=operator.itemgetter(1),reverse=True)

    tags = make_tags(get_tag_counts(Data1)[:50],maxsize=350,minsize=100)
    create_tag_image(tags,fname+'.png', size=(3000,3250), background=(0, 0, 0, 255), layout=LAYOUT_MIX, fontname='Lobster', rectangular=True)