import numpy as np
import cv2
from datetime import datetime
 
# Function to display clicks and gather user input when a mouse click occurs 
def click_event(event, x, y, flags, params): 
  
    global clickList, waitingOnUser, basket, basket_notext, height, width, font

    # checking for left mouse clicks 
    if (event == cv2.EVENT_LBUTTONDOWN) and (waitingOnUser == False): 
        
        # set this so that other clicks won't register until you finish the data input with this one
        waitingOnUser = True

        # draw a grey cross at the clicked area
        cross_length = int(((height + width) * 0.5) / 50)
        cv2.line(basket_notext, (x + cross_length, y + cross_length), (x - cross_length, y - cross_length), (0, 0, 0), 4) 
        cv2.line(basket_notext, (x - cross_length, y + cross_length), (x + cross_length, y - cross_length), (0, 0, 0), 4) 
        basket = basket_notext.copy()
        # give instructions to enter putt result
        cv2.rectangle(basket, (0, height), (width, height - 50), (0, 0, 0), -1)
        cv2.putText(basket, "Press 'y' for make, 'n' for miss.", (75, height-20), font, 0.75, (255, 255, 255), 2) 
        # display image
        cv2.imshow('Putting Data Collection', basket) 

        # collect putt result from the user
        cross_color = (0, 0, 0)
        outcome = 0 # 1 = make, 0 = miss
        while True:
            key = cv2.waitKey(1)
            if key == ord("y"):
                outcome = 1
                cross_color = (0, 225, 0)
                break
            elif key == ord("n"):
                outcome = 0
                cross_color = (0, 0, 255)
                break
    
        # color the cross based on putt result (make = green, miss = red).
        cv2.line(basket_notext, (x + cross_length, y + cross_length), (x - cross_length, y - cross_length), cross_color, 5) 
        cv2.line(basket_notext, (x - cross_length, y + cross_length), (x + cross_length, y - cross_length), cross_color, 5) 
        cv2.imshow('Putting Data Collection', basket_notext) 

        # collect centered position data and putt result for saving out
        x_centered = x - width/2
        y_centered = height/2 - y
        clickList.append((x_centered, y_centered, outcome))

        # allow for new clicks to register
        waitingOnUser = False
  
if __name__=="__main__": 
  
    # read the image 
    basket = cv2.imread('data/basket.png') 
    basket_notext = basket.copy()

    # set global variables
    waitingOnUser = False
    height = basket.shape[0] 
    width = basket.shape[1]
    clickList = []
  
    # display initial image
    #cv2.namedWindow('Putting Data Collection', cv2.WINDOW_NORMAL)
    #cv2.setWindowProperty('Putting Data Collection', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    cv2.namedWindow('Putting Data Collection', cv2.WINDOW_KEEPRATIO)
    font = cv2.FONT_HERSHEY_SIMPLEX 
    cv2.rectangle(basket_notext, (0, height), (width, height - 50), (0, 0, 0), -1)
    cv2.putText(basket_notext, "Click to add putt. Press 'q' to save & quit.", (35, height-20), font, 0.67, (255, 255, 255), 2) 
    cv2.imshow('Putting Data Collection', basket_notext) 
    cv2.resizeWindow('Putting Data Collection', 1000, 1000)
  
    # setting mouse handler for the image  
    cv2.setMouseCallback('Putting Data Collection', click_event) 
  
    # wait for the 'q' key to be pressed to exit 
    while True:
        if cv2.waitKey(0) == ord('q'):
            break
  
    # close the window 
    cv2.destroyAllWindows() 

    # save out the putting location and outcome data
    data = np.array(clickList)
    if len(data) > 0:
        now = datetime.now()
        date_string = now.strftime("%Y-%m-%d_%H-%M-%S")
        np.savetxt("data/output/sputting_" + date_string + ".csv", data, fmt="%i", delimiter=", ")