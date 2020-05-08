# -*- coding: utf-8 -*-
"""
Created on Mon Apr 13 11:01:19 2020

@author: kanno
"""
import json
import numpy as np
import cv2

all_frame = 204

#出力ファイル名
file_name = 'demo.csv'

# 関節毎の描画色（とりあえず適当な配色）
colors = [(255,0,85), (255,0,0), (255,85,0), (255,170,0), (255,255,0), (170,255,0), 
          (85,255,0), (0,255,0), (0,255,85), (0,255,170), (0,255,255), (0,170,255), 
          (0,85,255), (0,0,255), (255,0,170), (170,0,255), (255,0,255), (85,0,255),
          (0,85,255), (0,0,255), (255,0,170), (170,0,255), (255,0,255), (85,0,255)]

def calculate_distance(x_c,y_c,x_b,y_b):
    r = np.sqrt((x_c-x_b)**2+(y_c-y_b)**2)
    return r

#全てのidを保管
id_all = []

id_list_new = []

for fr in range(all_frame):
    fr_padded = '%03d' % fr
    # jsonのロード
    input_file_name = 'video_000000000'+str(fr_padded)+'_keypoints.json'
    with open(input_file_name) as f:
        data = json.load(f)
    
    if fr != 0:
        fr_padded_b = '%03d' % (fr-1)
        input_file_name_before = 'video_000000000'+str(fr_padded_b)+'_keypoints.json'
        with open(input_file_name_before) as f_b:
            data_b = json.load(f_b)
        d_b = data_b['people']

    img = np.full((720, 1280, 3), 255, dtype=np.uint8)
    
    d = data['people']
    
    #新しい骨格に固有のidを付与
    plus = 1
    
    for i in range(len(d)):
        kpt = np.array(d[i]['pose_keypoints_2d']).reshape((25, 3))
        # print(kpt)
        
        #関節のつながりをリスト化
        pairs = [[17,15],[15,0],[18,16],[16,0],[0,1],[1,2],[1,5],[2,3],[3,4],[5,6],[6,7],[1,8],[8,9],[9,10],[10,11],[11,24],[11,22],[22,23],[8,12],[12,13],[13,14],[14,21],[14,19],[19,20]]
        for p in range(len(pairs)):
            if kpt[pairs[p][0],2] == 0 or kpt[pairs[p][1],2] == 0:
                continue
            cv2.line(img,tuple(map(int,kpt[pairs[p][0],0:2])),tuple(map(int,kpt[pairs[p][1],0:2])),colors[p], thickness=2, lineType=cv2.LINE_4)
        
        if fr == 0:
            cv2.putText(img, 'id:'+str(i), (int(kpt[1,0]),int(kpt[1,1])+10),cv2.FONT_HERSHEY_PLAIN,1,(255, 0, 0), 1, cv2.LINE_AA)
            if i == len(d)-1:
                id_list = list(range(len(d)))
                id_all.extend(id_list)
                max_id = max(id_all)
                f = open(file_name, 'w')
                for x in id_list:
                    f.write(str(x)+',')
                f.write("\n")
                f.close()
            
        else:
            distance = 50
            id = 'none'
            for j in range(len(id_list)):
                kpt_b = np.array(d_b[j]['pose_keypoints_2d']).reshape((25, 3))
                r = calculate_distance(kpt[1,0],kpt[1,1],kpt_b[1,0],kpt_b[1,1])
                if distance > r:
                    distance = r
                    id = id_list[j]
                    index = j
                   
            if id == 'none':
                id = max_id+plus
                plus += 1
            else:
                id_list.remove(id)
                d_b.pop(index)
                
            cv2.putText(img, 'id:'+str(id), (int(kpt[1,0]),int(kpt[1,1])+10),cv2.FONT_HERSHEY_PLAIN,1,(255, 0, 0), 1, cv2.LINE_AA)
            id_list_new.append(id)
            
            if i == len(d)-1:
                id_list = id_list_new
                id_all.extend(id_list_new)
                max_id = max(id_all)
                f = open(file_name, 'a')
                for x in id_list:
                    f.write(str(x)+',')
                f.write("\n")
                f.close()
                id_list_new = []
        
    #画面に画像を表示
    # cv2.imshow("visualize",img)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    
    #同じファイルに保存
    cv2.imwrite(str(input_file_name)+'.jpg', img)
    print('end / '+str(input_file_name))
    #指定したディレクトリに保存
    #cv2.imwrite('C:/Users/kanno.TSIL/Downloads/openpose-1.5.1-binaries-win64-gpu-python-flir-3d_recommended/openpose-1.5.1-binaries-win64-gpu-python-flir-3d_recommended/openpose/output_keypoint/result001/'+str(input_file_name)+'.jpg', img)
    
"""
#参考コード
http://stmind.hatenablog.com/entry/2017/10/01/233655
"""
# for d in data['people']:
#      kpt = np.array(d['pose_keypoints']).reshape((18, 3))
#      # 関節位置の全ペアについて
#      for p in pairs:
#          pt1 = tuple(list(map(int, kpt[p[0], 0:2])))
#          c1 = kpt[p[0], 2]
#          pt2 = tuple(list(map(int, kpt[p[1], 0:2])))
#          c2 = kpt[p[1], 2]
#          # 信頼度0.0の関節は無視
#          if c1 == 0.0 or c2 == 0.0:
#              continue
#          # 関節の描画
#          color = tuple(list(map(int, colors[p[0]])))
#          img = cv2.line(img, pt1, pt2, color, 7)

# cv2.imshow('nacho', img)