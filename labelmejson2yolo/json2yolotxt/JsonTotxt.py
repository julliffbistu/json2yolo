# -*- coding: utf-8 -*-
import shutil
import os
import json
import cv2
import io
import numpy as np
NameToIdex={'cup':0}
#NameToIdex={'#':0,'souppot':1,'pan':2,'plate':3,'saucer':4}
jsonnum=0
num=[0]

if __name__ == '__main__':
    base_path="C:/Users/lifu_/Desktop/json2yolotxt/newtxt/"
    jsons_path="C:/Users/lifu_/Desktop/json2yolotxt/jsons/"
    imgs_path="C:/Users/lifu_/Desktop/json2yolotxt/images/"
    json_file = os.listdir(jsons_path) # 读取所有json文件
    train_path=base_path + 'train' + '.txt'
    valid_path=base_path + 'test' + '.txt'
    if os.path.exists(train_path)==True:     
        os.remove(train_path)
        print("!!!!!!!!!!!!!!!!!!")
    if os.path.exists(valid_path)==True:     
        os.remove(valid_path)
    train_txt = open((base_path + 'train' + '.txt'), 'wt') 
    valid_txt = open((base_path + 'test' + '.txt'), 'wt') 

    for file in json_file:
        jsonnum=jsonnum+1
        #file='243.json'

        print('file',file)
        file_path = os.path.join(jsons_path, file) # 找到json文件路径
        with io.open(file_path, 'r', encoding='utf-8') as f:
            file_json = json.load(f)
            imagename = file.split('.')[0]
            image_path=imgs_path + imagename+'.jpg'
            if os.path.exists(image_path)==False:
                print("~~~~~~~~~~~~~~~~~")     
                continue
            if jsonnum%5==0:
                valid_txt.write(image_path+'\n')
            else:
                train_txt.write(image_path+'\n')
            TXT_path=imgs_path + imagename + '.txt'
            if os.path.exists(TXT_path)==True:     
                os.remove(TXT_path)
            savename = open((imgs_path + imagename + '.txt'), 'wt') 
            image = cv2.imread(image_path)


            if image is None: # 如果没有这种照片，检查图片路径
                print("No image")
                continue
            #print("1111111111",image.shape)
            Img_Height=512
            Img_Width=640
            print("33333333333",Img_Height,Img_Width)
            shapes = file_json['shapes'] 
            for i in range(len(shapes)):
                classname = file_json['shapes'][i]['label'] # 类别
                index=NameToIdex[classname]
                num[index]=num[index]+1
                print('index',classname,index)
                points=file_json['shapes'][i]['points']
                #print("points",points)
                np_points=np.asarray(points)
                x=np_points[:,0]
                y=np_points[:,1]
                minx=np.min(x)
                maxx=np.max(x)
                miny=np.min(y)
                maxy=np.max(y)
                #print("x,y",minx,maxx,miny,maxy)
                '''
                cv2.namedWindow("image",cv2.WINDOW_NORMAL)
                cv2.imshow('image',image[int(miny)*2:int(maxy)*2,int(minx)*2:int(maxx)*2,:])
                cv2.waitKey(0)
                '''
                width=(maxx-minx)/Img_Width
                height=(maxy-miny)/Img_Height
                x_center=(minx+maxx)/(2*Img_Width)
                y_center=(miny+maxy)/(2*Img_Height)
                print("p",x_center,y_center,width,height)
                print("pe",x_center*Img_Width,y_center*Img_Height,width*Img_Width,height*Img_Height)
                savename.write(str(index) + " " + str(x_center)+" "+str(y_center)+" "+str(width)+" "+str(height)+'\n')
            savename.close()
            print(savename)
            #break
train_txt.close()
valid_txt.close()
print('num:',num)


