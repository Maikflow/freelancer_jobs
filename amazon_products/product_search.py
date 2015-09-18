#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import urllib2
import os
from argparse import ArgumentParser

from amazonproduct import API
from gooey import Gooey
from lxml import etree
from openpyxl import Workbook

CATEGORIES = ['beauty', 'health', 'grocery', 'health and personal care']
FIELDS = ['ASIN', 'UPC', 'EAN', 'Brand', 'Manufacturer', 'Title', 'Product URL',
          'Image URL', 'Price', 'Long description', 'Leaf Category',
          'Parent Category', 'BrowseNode ID', 'Child Category',
          'Short Description', 'Star Rating', 'Root Category']
OPERATIONS = [
              'ASIN',
              'ItemAttributes.UPC',
              'ItemAttributes.EAN',
              'ItemAttributes.Brand',
              'ItemAttributes.Manufacturer',
              'ItemAttributes.Title',
              'DetailPageURL',
              'LargeImage.URL',
              'OfferSummary.LowestNewPrice.FormattedPrice',
              'ItemAttributes.Feature',
              'BrowseNodes.BrowseNode.Name',
              'BrowseNodes.BrowseNode.Ancestors.BrowseNode.Name',
              'BrowseNodes.BrowseNode.BrowseNodeId',
              'BrowseNodes.BrowseNode.Children.BrowseNode.Name',
              'ItemAttributes.Feature'
              ] 
Root = True
             
data = {k: [] for k in FIELDS}


api = API(locale='us')
def search_products(args):
    """
       Make use of the amazon product-advertising 
       api to retrieve all FIELDS.
    """

    for z, page in enumerate(xrange(1,args.pages+1),1):
        os.system('clear')
        print '\rRetrieving page {} of {}'.format(page,args.pages)
        # get all products from result set and append to data dictionary
        for y, product in enumerate(api.item_search(args.category.capitalize(),
                                    Keywords=args.keyword,
                                    ResponseGroup='Large', ItemPage=page)):
            print '\rRetrieving {} attributes'\
                  'from {} category'.format(args.keyword,
                                            args.category.capitalize())+\
                                            update_progress(y+1),
            sys.stdout.flush()
            for x, attribute in enumerate(OPERATIONS):
                #print x, attribute
                ancestor = '.Ancestors.BrowseNode'
                try:
                    data[FIELDS[x]].append(eval('product.'+attribute).text)
                except AttributeError:
                    data[FIELDS[x]].append('None')

                #Obtain the root node recursively
                while True:
                    try:
                        root = 'BrowseNodes.BrowseNode{}'.format(ancestor) 
                        eval('product.'+root+'.IsCategoryRoot')
                        data['Root Category'].append(eval('product.'+root+
                            '.Ancestors.BrowseNode.Name').text)
                        break
                    except AttributeError:
                        ancestor+='.Ancestors.BrowseNode'
                        continue

            #write down xml in blank file
            #et = etree.tostring(product, pretty_print=True)
            #print et
            #with open('archivo.xml', 'w') as f: f.write(et)
    print '\n'

    #get star review count
    for x, asin in enumerate(data["ASIN"]):
        print '\rRetrieving star review count'+update_progress(x/args.pages+1),
        sys.stdout.flush()
        data['Star Rating'].append(get_star_reviews(asin))

    #write all the data obtained into an excel file
    write_to_excel(data, args)
    print '\n\nSUCCESS :)'

def get_star_reviews(asin):

    #URL string for extracting star reviews
    star_review_url = ('http://www.amazon.com/gp/'
                       'customer-reviews/widgets/'
                       'average-customer-review/popover/'
                       'ref=dpx_acr_pop_?contextId=dpx&asin={}'
                      ).format(asin)

    print star_review_url
    #Handle disconnects
    attempts = 0
    while True:
        try:
            if attempts < 20:
                url = urllib2.urlopen(star_review_url).read()
                break
            else:
                break
        except:
            attempts += 1
            continue

    #parse the response
    tag = url.find('out of')
    return url[tag-4:tag-1]

def update_progress(progress):
        return '[{0}] {1}%'.format('#'*(progress/10), progress)

def write_to_excel(data, args):
    '''write xml to excel file'''
    
    #First create the workbook
    wb = Workbook()
    ws = wb.active
    
    #write the column headers 
    ws.append(i for i in FIELDS)
    print '\n'

    # now we'll fill the workbook with the FIELDS headers and populate it with
    # the data we extracted 
    for x in range(len(data.values()[0])):
        try:
            print '\rWriting excel file '+update_progress(x/args.pages+1),
            sys.stdout.flush()
            ws.append(data[field][x] for field in FIELDS)
        except:
            pass
        # save the file
    wb.save(args.output+'.xlsx') 

@Gooey
def main():
    parser = ArgumentParser(prog = 'amazon product extractor', 
                            description = """Select between categories: 
                                             health, beauty, grocery or
                                             health and personal care.
                                          """
                            )
    parser.add_argument('--category', default = 'beauty', choices = CATEGORIES,
                        required = False)
    parser.add_argument('--keyword', default = 'eye cream')
    parser.add_argument('--output', default = 'output')
    parser.add_argument('--pages', default = 2, type=int,
                        help='number of pages retrieved for your product')
    args = parser.parse_args()
    search_products(args)

if __name__ == "__main__":
    main() 
