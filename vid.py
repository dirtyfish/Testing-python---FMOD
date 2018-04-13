from moviepy.editor import *



clip = VideoFileClip('wildlife.wmv')

clip.get_frame(10)

#clip.preview()



























#import cv2

#cap = cv2.VideoCapture('wildlife.wmv')

#while(cap.isOpened()):
    #ret, frame = cap.read()
   	#gray = cv2.cvtColor(frame, 0)
   	#cv2.imshow('frame',gray)
   	#if cv2.waitKey(1) & 0xFF == ord('q'):
        #break

#cap.release()
#cv2.destroyAllWindows()