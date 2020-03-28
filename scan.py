import cv2
import os
import numpy as np

img_path = './src/imgsource.jpg'
filename, ext = os.path.splitext(os.path.basename(img_path))
ori_img= cv2.imread(img_path)

src=[]
res=0
img=0

# mouse callback handler
def mouse_handler(event,x,y,flag,param):
    if event == cv2.EVENT_LBUTTONUP:
        img = ori_img.copy()   #왜 이렇게 행동하는 걸까? 복사 안하고 원본을 넣어도 되지 않을까 싶은데...

        src.append([x,y])

        for xx,yy in src:
            cv2.circle(img,center=(xx,yy), radius=5, color=(0,255,0), thickness=-1, lineType=cv2.LINE_AA)

        cv2.imshow('img',img)

        #perspective transform
        if len(src)==4:
            src_np= np.array(src,dtype=np.float32)
            #scr_np라는 float32화 된 복사본을 만들어서 배열 카피본을 뜬다.
            #왜 점을 32비트 float로 바꾸는 것일까?

            width= max(np.linalg.norm(src_np[0]-src_np[1]),np.linalg.norm(src_np[2]-src_np[3]))
            height= max(np.linalg.norm(src_np[0]-src_np[3]),np.linalg.norm(src_np[1]-src_np[2]))

            dst_np= np.array([
                [0,0],
                [width,0],
                [width,height],
                [0,height]
            ], dtype=np.float32)

            M=cv2.getPerspectiveTransform(src=src_np, dst=dst_np)
            result = cv2.warpPerspective(ori_img,M=M,dsize=(width,height))

            cv2.imshow('result',result)
            cv2.imwrite('./src/%s_result%s'% (filename,ext), result)

            res =1;


# main
cv2.namedWindow('img')
cv2.setMouseCallback('img',mouse_handler)

cv2.imshow('img',ori_img)
cv2.waitKey(0)





