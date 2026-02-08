import cv2
import numpy as np
cap = cv2.VideoCapture(0)
while True:
	ret,frame = cap.read()	#capture frame_by_frame
	gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
	cv2.imshow('frame',gray)
	cv2.imshow('color',frame)
	if cv2.waitKey(1)&0XFF ==ord('q'):
		break
cap.release()
cv2.destroyAllWindows()

