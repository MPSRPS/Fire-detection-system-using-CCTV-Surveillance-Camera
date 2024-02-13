import cv2         # Library for openCV
import threading   # Library for threading -- which allows code to run in backend
import playsound   # Library for alarm sound we can also use MediaPlayer().
import os
from twilio.rest import Client #Import's TWILIO API
import time
import telegram
from telegram import InputFile
import asyncio

TOKEN = '5985891587:AAFlei0lIpR6zvwF4L9c-5iU_R3bBOh7uh0'
CHAT_ID = '1412481203'

# Create a Telegram Bot object
bot = telegram.Bot(token=TOKEN)

async def send_video_to_telegram(video_bytes):
    # Send the video frame to Telegram
    await bot.send_video(chat_id=CHAT_ID, video=InputFile(video_bytes))
## Twilio API credentials

account_sid = 'AC36e6c8e94c9e0cfa97082aa6d6025c29'# $TWILIO_ACCOUNT_SID
auth_token = '01534fa18ac0a7d49c505064acd1d92d'#$TWILIO_AUTH_TOKEN
twilio_phone = '+12058802207'#YOUR_TWILIO_PHONE_NUMBER
recipient_phone = '+919579000974'#RECIPIENT_PHONE_NUMBER

fire_cascade = cv2.CascadeClassifier('fire_detection_cascade_model.xml') # To access xml file which includes positive and negative images of fire. (Trained images)

# Twilio message sending function
#                                                                         
def send_message():
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        to=recipient_phone, 
        from_=twilio_phone,
        body='URGENT: Fire accident at VVP COLLEGE SOLAPUR. Please send immediate assistance. All occupants have been evacuated.  Fire Accident Threat Evacuation Order for Leave Now FAST FIRE DETECTED!')
    print('Message sent.')

# Twilio calling function

def send_call():
    client = Client(account_sid, auth_token)
    call = client.calls.create(
        to=recipient_phone, 
        from_=twilio_phone,
          twiml='<Response><Say>ALERT! FIRE DETECTED! FROM VVP COLLEGE Hello, this is AN EMERGENCY calling from VVP COLLEGE SOLAPUR. We have a fire accident and need immediate assistance. All occupants have been evacuated. Please send help as soon as possible. LEAVE NOW</Say></Response>')
    print('Call sent.')
    
video = cv2.VideoCapture(0)
vid = cv2.VideoCapture(0) # To start camera this command is used "0" for laptop inbuilt camera and "1" for USB attahed camera
runOnce = False # created boolean
fourcc = cv2.VideoWriter_fourcc(*'XVID')
output_file = 'video.avi'
out = cv2.VideoWriter(output_file, fourcc, 20.0, (640,480))

def play_alarm_sound_function(): # defined function to play alarm post fire detection using threading
    playsound.playsound('fire.mp3',True) # to play alarm # mp3 audio file .
    print("Fire alarm end") # to print in console		
while(True):
    Alarm_Status = False
    ret, frame = vid.read() # Value in ret is True # To read video frame
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) # To convert frame into gray color
    fire = fire_cascade.detectMultiScale(frame, 1.2, 5) # to provide frame resolution
    

        # Wait for a short time before capturing the next frame
    time.sleep(0.60)
    
    ## to highlight fire with square 

    for (x,y,w,h) in fire:
        cv2.rectangle(frame,(x-20,y-20),(x+w+20,y+h+20),(255,0,0),2)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = frame[y:y+h, x:x+w]

        print("Fire alarm initiated")
        threading.Thread(target=play_alarm_sound_function).start()  # To call alarm thread
        _, buffer = cv2.imencode('.jpg', frame)
        video_bytes = buffer.tobytes()
        out.write(frame)
        loop = asyncio.get_event_loop()
        loop.run_until_complete(send_video_to_telegram(video_bytes))
        send_message() #Twilio message sending function invoked
        send_call() #Twilio calling function invoked
        with open(output_file, 'rb') as f:
             video_bytes = f.read()
             loop = asyncio.get_event_loop()
             loop.run_until_complete(send_video_to_telegram(video_bytes))

    cv2.imshow('frame', frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'): # Exit loop if 'q' is pressed
        break
    
cv2.destroyAllWindows()
video.release()

