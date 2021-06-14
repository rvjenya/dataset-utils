#A number in a txt text stores the name of the picture,
#To save the pictures with these names in another folder
#Modify two places, pay attention to create your own files
import argparse
from PIL import Image
import os



# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser(description='A number in a txt text stores the name of the picture, To save the pictures with these names in another folder Modify two places, pay attention to create your own files')
ap.add_argument('-i', '--train', type=str, default=None,
    help='train file path')
ap.add_argument('-a', '--annot-xml', type=str, default=None,
    help='Absolute path of all xml files')
ap.add_argument('-e', '--extracted', type=str, default=None,
    help='Absolute path extracted from the xml file used for train')
args = vars(ap.parse_args())



f3 = open('args["train"]') #train file path
for line2 in f3.readlines():
    line3=line2[:-1] #Read all numbers 000000
    xmldir = 'args["annot-xml"]'
     #Absolute path of all xml files
    savedir = 'args["extracted"]'
    #Absolute path extracted from the xml file used for train
    xmllist = os.listdir(xmldir)
    for xml in xmllist:
        # if '.xml' in xml:
        if '.xml' in xml:
            if line3 in xml:
                fo = open(savedir + '/' + '{}'.format(xml), 'w')  
                print('{}'.format(xml))
                fi = open(xmldir + '/' + '{}'.format(xml), 'r')
                content = fi.readlines()
                for line in content:
                    fo.write(line)
                fo.close()
                print('Replacement succeeded')
f3.close()
