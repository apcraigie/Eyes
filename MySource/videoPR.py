#Programmer: Austin Craigie
#Github: apcraigie
#created: 8/15/2018
#last modified: 8/15/2018
#file: VideoPR.py
#description: This file contains all of the code for getting input from the web camera and 
#             prossessing though the face_recognition library and displying all results

#Note:
#I got alot of help for this file from Github user: ageitgey
#and his example file located here: 
#https://github.com/ageitgey/face_recognition/blob/master/examples/facerec_from_webcam_faster.py


import cv2
import face_recognition
import numpy
import pybind11
import os


#user
user_name = None
user_pic = None   

#lists of known people
friends = []
friend_names = []
enemies = []
enemies_names = []
face_Stat_Name = []

#input stream
videoStream = None

#recognition information
face_encoding = []
face_locations = []

#differnt frames that are need for the prossess
start_Frame = None
rgb_Frame = None #opencv uses BGR and face_recognition uses RGB
small_Frame = None


#Function getCamera()
#Description: imports the feed from the defualt camera  
#input: None
#output: bool for if camera was found
def getCamera():
    global video_Stream
    video_Stream = cv2.VideoCapture(0)
    if video_Stream == None:
        print("Error 0: No Camera Found!!")
        return False
    else:
        print("Camera loaded!!")
        return True

def newFrame():
    global start_Frame
    global rgb_Frame
    global small_Frame
    
    start_Frame = cv2.imread("./MySource/people.jpg") #video_stream.read()
    #resize to speed up face idetification
    small_Frame = cv2.resize(start_Frame, (0,0), fx=.25, fy=.25)
    #recolor
    rgb_Frame = small_Frame[:, :, ::-1] 

def prossessFrame():
    global face_encoding
    global face_locations
    global rgb_Frame
    face_locations = face_recognition.face_locations(rgb_Frame)
    face_encoding = face_recognition.face_encodings( rgb_Frame, face_locations)

def friendEnemyOther():
    global face_Stat_Name
    global face_encoding
    global friends
    global friend_names
    global enemies
    global enemies_names
    global user_name
    global user_pic
    
    prossessFrame()
    face_Stat_Name = []
    friend_Matchs = []
    enemy_Matchs = []

    for face in face_encoding:
        match = face_recognition.compare_faces(user_pic, face)
        if True in match: #user is 2
            person = (2, user_name)
        else:        
            #look though known faces
            for friendFace in friends:
                friend_Matchs.append(face_recognition.compare_faces(friendFace, face, .4))
            print(str(friend_Matchs))
            for enemyFace in enemies:
                enemy_Matchs.append(face_recognition.compare_faces(enemyFace, face, .4))
        
            #print("frineds " + str(friend_Matchs))
            #print("Enemies" + str(enemy_Matchs))
            if [True] in friend_Matchs:
                index = friend_Matchs.index([True])
                person = (1, friend_names[index])
            elif [True] in enemy_Matchs:
                index = enemy_Matchs.index([True])
                person = (-1, enemies_names[index])
            else:
                person = (0, "Unknown")

            
        face_Stat_Name.append(person)
        enemy_Matchs = []
        friend_Matchs = []
        match =[]

def display():
    global face_locations
    global face_Stat_Name
    global start_Frame

    for (top, right, bottom, left), (stat, name) in zip(face_locations, face_Stat_Name):
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        #correct color BGR
        if stat == 2: #user
            color = (0, 200, 200)
        elif stat == 1: #friend
            color = (0,255,0)
        elif stat == -1: #enemy
            color = (0,0,255)
        else:
            color = (255, 0, 0)

        # Draw a box around the face
        cv2.rectangle(start_Frame, (left, top), (right, bottom), color, 2)

        # Draw a label with a name below the face
        cv2.rectangle(start_Frame, (left, bottom - 35), (right, bottom), color, cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(start_Frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    #disply
    cv2.imshow('Feed', start_Frame)

def populate():
    global user_name
    global user_pic
    global friend_names
    global friends
    global enemies
    global enemies_names
    
    user_dir = os.listdir("./MySource/user/")
    friend_dir = os.listdir("./MySource/friend/")
    enemy_dir = os.listdir("./MySource/enemy/")
    for pic in user_dir:
        pic2 = face_recognition.load_image_file(str("./MySource/user/") + str(pic))
        user_pic = face_recognition.face_encodings(pic2)
        user_name = str(pic)
    for pic in friend_dir:
        pic2 = face_recognition.load_image_file(str("./MySource/friend/") + str(pic))
        friends.append(face_recognition.face_encodings(pic2))
        friend_names.append(str(pic))
    for pic in enemy_dir:
        pic2 = face_recognition.load_image_file(str("./MySource/enemy/") + str(pic))
        enemies.append(face_recognition.face_encodings(pic2))
        enemies_names.append(str(pic))



#Function run()
#Description: this funtion sets up the camera and starts prossessing frames
#input: None
#output: None
def run():
    prossess = True
    populate()
    if True: #getCamera():
        while True:
            if prossess:
                newFrame()
                friendEnemyOther()
                display()
            prossess = not prossess
            # Hit 'q' on the keyboard to quit!
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break