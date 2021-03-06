#coding:utf-8
import argparse
import sys
import os
import json
import xml.etree.ElementTree as ET



# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser(description='VOC format to coco format')
ap.add_argument('-p', '--path', type=str, default=None,
    help='Modify to your own path')
args = vars(ap.parse_args())

START_BOUNDING_BOX_ID = 1

PRE_DEFINE_CATEGORIES = {"normal":0,"defect":1,"norbolt":2,"debolt":3}
#Note to modify the number and name according to your own data set name

def get(root, name):
    vars = root.findall(name)
    return vars
 
 
def get_and_check(root, name, length):
    vars = root.findall(name)
    if len(vars) == 0:
        raise NotImplementedError('Can not find %s in %s.'%(name, root.tag))
    if length > 0 and len(vars) != length:
        raise NotImplementedError('The size of %s is supposed to be %d, but is %d.'%(name, length, len(vars)))
    if length == 1:
        vars = vars[0]
    return vars
 
 
def get_filename_as_int(filename):
    try:
        filename = os.path.splitext(filename)[0]
        return int(filename)
    except:
        raise NotImplementedError('Filename %s is supposed to be an integer.'%(filename))
 
 
def convert(xml_dir, json_file):
    xmlFiles = os.listdir(xml_dir)
    
    json_dict = {"images":[], "type": "instances", "annotations": [],
                 "categories": []}
    categories = PRE_DEFINE_CATEGORIES
    bnd_id = START_BOUNDING_BOX_ID
    num = 0
    for line in xmlFiles:
    #print("Processing %s"%(line))
        num +=1
        if num%50==0:
            print("processing ",num,"; file ",line)
            
        xml_f = os.path.join(xml_dir, line)
        tree = ET.parse(xml_f)
        root = tree.getroot()
        ## The filename must be a number
        filename = line[:-4]
        image_id = get_filename_as_int(filename)
        size = get_and_check(root, 'size', 1)
        width = int(get_and_check(size, 'width', 1).text)
        height = int(get_and_check(size, 'height', 1).text)
        # image = {'file_name': filename, 'height': height, 'width': width, 'id':image_id}
        image = {'file_name': (filename+'.jpg'), 'height': height, 'width': width,
                 'id':image_id}
        json_dict['images'].append(image)
        ## Cruuently we do not support segmentation
        #  segmented = get_and_check(root, 'segmented', 1).text
        #  assert segmented == '0'
        for obj in get(root, 'object'):
            category = get_and_check(obj, 'name', 1).text
            if category not in categories:
                new_id = len(categories)
                categories[category] = new_id
            category_id = categories[category]
            bndbox = get_and_check(obj, 'bndbox', 1)
            xmin = int(get_and_check(bndbox, 'xmin', 1).text) - 1
            ymin = int(get_and_check(bndbox, 'ymin', 1).text) - 1
            xmax = int(get_and_check(bndbox, 'xmax', 1).text)
            ymax = int(get_and_check(bndbox, 'ymax', 1).text)
            assert(xmax > xmin)
            assert(ymax > ymin)
            o_width = abs(xmax - xmin)
            o_height = abs(ymax - ymin)
            ann = {'area': o_width*o_height, 'iscrowd': 0, 'image_id':
                   image_id, 'bbox':[xmin, ymin, o_width, o_height],
                   'category_id': category_id, 'id': bnd_id, 'ignore': 0,
                   'segmentation': []}
            json_dict['annotations'].append(ann)
            bnd_id = bnd_id + 1
 
    for cate, cid in categories.items():
        cat = {'supercategory': 'none', 'id': cid, 'name': cate}
        json_dict['categories'].append(cat)
    json_fp = open(json_file, 'w')
    json_str = json.dumps(json_dict)
    json_fp.write(json_str)
    json_fp.close()
 
if __name__ == '__main__':
    folder_list= ["train","val","test"]
    #Note to change base_dir to local actual image and annotated file path
    base_dir = 'args["path"]'
    #Modify to your own path
    
    for i in range(3):
        folderName = folder_list[i]
        xml_dir = base_dir + folderName
        json_dir = base_dir + folderName + "/instances_" + folderName + ".json"

        print("deal: ",folderName)
        print("xml dir: ",xml_dir)
        print("json file: ",json_dir)
        
        convert(xml_dir,json_dir)
