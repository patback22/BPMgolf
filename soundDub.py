from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from pydub import AudioSegment
from pydub.playback import play
import random
from kivy.config import Config
Config.set('kivy', 'keyboard_mode', 'dock')
from kivymd.app import MDApp
from kivymd.uix.button import MDRoundFlatButton
from kivy.core.window import Window
from kivy.uix.vkeyboard import VKeyboard
from numpad import NumPadPopUp, NumPadWidget
from kivy.uix.popup import Popup



#define variables at their starting values

kempo = 60
tempo = kempo
hole = 0
score = 0

class SoundPlayer(FloatLayout):

    #create a class to play sound

    def play_sound(self):

    #assign the soundfile to a variable and pass that variable through AudioSegment for processing
        
        root = r'/home/kinglyon976/Estimator2/metronome60T.mp3'
        
        sound = AudioSegment.from_file(root)
        
        def speed_change(sound, speed=1.0):

            # Manually override the frame_rate. This tells the computer how many
            # samples to play per second
            sound_with_altered_frame_rate = sound._spawn(sound.raw_data, overrides={
             "frame_rate": int(sound.frame_rate * speed)
            })

            # convert the sound with altered frame rate to a standard frame rate
            # so that regular playback programs will work right. They often only
            # know how to play audio at standard frame rate (like 44.1k)
            return sound_with_altered_frame_rate.set_frame_rate(sound.frame_rate)

              
        print(tempo)

        #pass the AudioSegment though speed change function
        #the original audio clip is at 60 bpm, diving by 60 gives our tempo rate

        self.rate = tempo/60
        print(self.rate)


        slow_sound = speed_change(sound, self.rate)
        
        play(slow_sound)



    
     
class MyApp(MDApp):

    #creates the app layout, widgets, and GUI
    #VB and HB create two diefferent layout orientations for the widgets

    def build(self):

        multiplyer = 1

        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Purple"

        Window.size = (400,500)
        layout = FloatLayout(size = (100, 100))
        #VB = GridLayout(size = (100, 100))
        #HB = GridLayout(size = (100, 100))
        submit = MDRoundFlatButton(text = 'Submit', pos=(50, 250), line_width = 2, on_press=self.submit)
        layout.add_widget(submit)
        playsound = MDRoundFlatButton(text = 'Play', line_width = 2, pos=(275, 250), on_press=SoundPlayer.play_sound)
        layout.add_widget(playsound)
        self.ScoreLabel = Label(text = str(score), pos=(15, 150))
        layout.add_widget(self.ScoreLabel)
        self.BPMinput = TextInput(hint_text = 'Enter BPM here', size_hint = (.2, None), pos = (150,250))
        layout.add_widget(self.BPMinput)

        keyboard = NumPadWidget()            #on_key_up = self.on_key_up)

        #NumPadPopUp.open()
        
        #popup = NumPadPopUp(self.BPMinput)
        '''
        if self.BPMinput.focus == True:
            print('FOCUS')
           
        else:
            pass
        '''
    
        #layout.add_widget(keyboard)
       

        #Window.softinput_mode = ‘below_target’

        

        #layout.add_widget(VB)
        #layout.add_widget(HB)

        return layout
    '''
    def key_up(self, keyboard, keycode, *args):
        if isinstance(keycode, tuple):
            keycode = keycode[1]

        inputVAR = self.BPMinput.text
        print(keycode)

        if keycode == 'backspace':
            inputVAR = inputVAR[:-1]
            keycode = ''
        elif keycode == 'spacebar':
            keycode = ' '
        elif keycode == [10]:
            inputVAR = ']'



        self.BPMinput.text = f'{inputVAR}{keycode}'
    '''     

    
          

    def end_round():

        #stops the game after the desired number of levels
        #function is triggered by the sumbit function

        if hole == 3:
            print("STTTTTTTOOOPPPPPPPPP")
            App.get_running_app().stop() 

    
    def clear_inputs(self, BPMinput):

        #clears the input in the BPM input box

        self.BPMinput.text = ''



    def update_score(self, ScoreLabel):

        #updates the ScoreLabel widget on the main GUI window

        self.ScoreLabel.text = str(score)

    
        
    def submit(self,obj):

            #function takes the BPM input from user and passes the difference into the score variable
            #a new random tempo is assigned for the next level
            #on submit button press a new level is created

            global hole
            global score
            global tempo

            print('BPM guess: ' + self.BPMinput.text)
            BPMguess = self.BPMinput.text

            guessDifference = int(BPMguess) - int(tempo)
            guessDifferenceABS = abs(guessDifference)
            print('LL:  ' + str(guessDifferenceABS))  

            tempo = random.randint(30, 220)
            print("new tempo: " + str(kempo))

            score = score + guessDifferenceABS
            print("score: " + str(score))

            hole += 1
            print("hole :" + str(hole))

            MyApp.update_score(self, self.ScoreLabel)

            MyApp.clear_inputs(self, self.BPMinput)

            MyApp.end_round()


    
MyApp().run()


