#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import urllib2
import os
import Tkinter as tk
from argparse import ArgumentParser
from gui import Application

from amazonproduct import API
from lxml import etree
from openpyxl import Workbook

CATEGORIES = ['beauty', 'health', 'grocery', 'HealthPersonalCare']
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
        os.system('cls' if os.name == 'nt' else 'clear')
        print '\rRetrieving page {} of {}'.format(page,args.pages)
        if args.category != 'HealthPersonalCare':
            args.category=args.category.capitalize()

        # get all products from result set and append to data dictionary
        for y, product in enumerate(api.item_search(args.category,
                                    Keywords=args.keyword,
                                    ResponseGroup='Large', ItemPage=page)):
            print '\rRetrieving {} attributes '\
                  'from {} category'.format(args.keyword,
                                            args.category)+update_progress(y+1),
            sys.stdout.flush()
            for x, attribute in enumerate(OPERATIONS):
                # print x, attribute
                ancestor = '.Ancestors.BrowseNode'
                try:
                    data[FIELDS[x]].append(eval('product.'+attribute).text)
                except AttributeError:
                    data[FIELDS[x]].append('None')

                # Obtain the root node recursively
                count = 0
                while True:
                    try:
                        try:
                            eval('product.'+'BrowseNodes')
                        except AttributeError:
                            data['Root Category'].append('No browse nodes')
                            break
                        root = 'BrowseNodes.BrowseNode{}'.format(ancestor) 
                        eval('product.'+root+'.IsCategoryRoot')
                        data['Root Category'].append(eval('product.'+root+
                            '.Ancestors.BrowseNode.Name').text)
                        break
                    except AttributeError, e:
                        count += 1
                        # print 'the error is {}'.format(str(e))
                        ancestor+='.Ancestors.BrowseNode'
                        if count>=6:
                            data['Root Category'].append('No root nodes')
                            break
                        continue

            #write down xml in blank file
            #et = etree.tostring(product, pretty_print=True)
            #print et
            #with open('archivo.xml', 'w') as f: f.write(et)
    print '\n'

    # get star review count
    for x, asin in enumerate(data["ASIN"]):
        print '\rRetrieving star review count'+update_progress(x/args.pages+1),
        sys.stdout.flush()
        data['Star Rating'].append(get_star_reviews(asin))

    # write all the data obtained into an excel file
    write_to_excel(data, args)
    print '\n\nSUCCESS :)'

def get_star_reviews(asin):

    # URL string for extracting star reviews
    star_review_url = ('http://www.amazon.com/gp/'
                       'customer-reviews/widgets/'
                       'average-customer-review/popover/'
                       'ref=dpx_acr_pop_?contextId=dpx&asin={}'
                      ).format(asin)

    # print star_review_url
    # Handle disconnects
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

    # parse the response
    tag = url.find('out of')
    return url[tag-4:tag-1]

def update_progress(progress):
        return '[{0}] {1}%'.format('#'*(progress/10), progress)

def write_to_excel(data, args):
    '''write xml to excel file'''
    
    # First create the workbook
    wb = Workbook()
    ws = wb.active
    
    # write the column headers 
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
    wb.save(args.output_name+'.xlsx') 

def CLI(values):

    """
       Extract all available information for specified item and category
       from the amazon website trough the CLI. 
    """

    parser = ArgumentParser(prog = 'amazon product extractor', 
                            description = """Extract all item information from
                                             Health, Beauty, Grocery or
                                             Health and Personal Care Categories
                                          """
                            )
    parser.add_argument('--category', default=values['category'], choices=CATEGORIES,
                        required=False, type=str)
    parser.add_argument('--keyword', required=False, default=values['keyword'], 
                        type=str)
    parser.add_argument('--output_name', default=values['output'], type=str)
                        #widget='FileChooser')
    parser.add_argument('--pages', default=values['pages'], type=int, required=False,
                        help='number of pages retrieved for your product')
    args = parser.parse_args()
    search_products(args)

if __name__ == "__main__":
    root = tk.Tk()
    app = Application(root)
    root.mainloop()
