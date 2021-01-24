import cv2
import numpy as np
import  time
video = cv2.VideoCapture('C:/Users/Lam/Pictures/BlueStacks/input.mp4')
fps=video.get(cv2.CAP_PROP_FPS)
width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))  # float `width`
height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
print(height)

# video.set(cv2.CAP_PROP_FPS, 60)
image=cv2.imread('C:/Users/Lam/Pictures/BlueStacks/OJYV110ad.png')
image=cv2.resize(image, (width,height))
image=cv2.cvtColor(image,cv2.COLOR_BGR2BGRA)
fourcc = cv2.VideoWriter_fourcc(*'MP4V')
output=cv2.VideoWriter("C:/Users/Lam/Pictures/BlueStacks/outputx.avi",  cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), fps,(width,height))
# try:
while 1:
    font=cv2.FONT_HERSHEY_SIMPLEX
    # time.sleep(1)
    ret, frame = video.read()
    if ret == False:
        break
    frame=cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA)
    cv2.putText(frame,
                'TOVANLAM',
                (int(width*0.21), int(height*0.03)),
                font,
                .7, # font size
                (255,100,0)  # color
                ,1,  # thickness
                cv2.LINE_4)
    overlay =np.zeros((height,width,4), dtype='uint8')
    for i in range(0,height):
        for j in range(0,width):
            if image[i,j][3]!=0:
                overlay[i,j]=image[i,j]
    cv2.addWeighted(overlay,1,frame,1,0,frame)
    cv2.imshow("OL",frame)
    output.write(frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video.release()
output.release()






# except:
#     print("ok")
