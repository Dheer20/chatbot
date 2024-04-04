from PIL import Image
import speech_recognition as sr
import action
import customtkinter as ctk


# Creating Window

class App(ctk.CTk):
    def __init__( self , title , size ):

        super().__init__()
        self.title(title)   
        self.resizable(False,False)
        
        self.geometry(f'{size[0]}x{size[1]}')

        i_o = IO(self)
        main = ManageFile(self,i_o)
        
        self.mainloop()

# Creating the File Manager
        
class ManageFile(ctk.CTkFrame):

    def __init__(self, master ,io_instance):
        super().__init__(master)
        self.io_instance = io_instance
        self.create_widgets()
        self.place(
            relx=0.01,
            rely=0.01,
            relwidth=0.33,
            relheight=0.98)

    def create_file(self):
        self.file_display.file_count += 1
        self.file_display.file_index = self.file_display.file_count-1

        self.file_display.file_var_list =['self.'+'file_'+ str(num) for num in range (1,self.file_display.file_count+1)]

        file_name = self.file_display.file_var_list[self.file_display.file_index].split('.')[1]
        self.file_display.file_name_list.append(file_name)

        file_path = f"chats/{file_name}.txt"
        self.file_display.file_path_list.append(file_path)

        self.file_display.file_var_list[self.file_display.file_index] = FileTile(self.file_display, file_name)
        self.file_display.file_var_list[self.file_display.file_index].pack(fill = 'x' ,pady = 5 , padx = 10)
    
    def create_widgets(self):

        #Create Widgets
        self.new_chat_button = ctk.CTkButton(
            self,
            text ='+  New Chat',
            font = ('Arial', 15),
            command = self.create_file)
        
        self.file_button = ctk.CTkButton(self)
        self.file_display = FileDisplay(self,self.io_instance)    

        #Place Widgets
        self.new_chat_button.place(
            relx = 0.39,
            rely = 0.1,
            relwidth = 0.73 ,
            relheight = 0.07,
            anchor ='center')
        
        self.file_button.place(
            relx = 0.77,
            rely = 0.1,
            relwidth = 0.2,
            relheight = 0.07,
            anchor ='w')
            
class FileDisplay(ctk.CTkFrame):
    def __init__(self, master,io_instance):
        super().__init__(master)
        self.io_instance = io_instance
        self.file_count = 0
        self.file_index = 0
        self.file_name_list = []
        self.file_var_list = []
        self.file_path_list = []

        self.fill_frame = ctk.CTkFrame(
            self,
            height = 10,
            fg_color='transparent')
        self.fill_frame.pack()
        self.place(
            relx = 0.5,
            y = 315,
            relwidth = 1,
            relheight = 0.80,
            anchor ='center')

class FileTile(ctk.CTkFrame):
    def __init__(self, master , file_name):
        super().__init__(master,height = 48)
        self.file_display = master
        self.file_name = ctk.StringVar(value = file_name)
        self.file_init = False

        self.handle_images()

        #Create Widgets
        self.file_label = ctk.CTkLabel(self, textvariable= self.file_name)
        self.file_delete_button = ctk.CTkButton(
            self,
            height = 35,
            width = 35,
            text='',
            fg_color='transparent',
            border_width=1.5,
            command = self.delete,
            image=self.trash_icon_ctk,
            hover_color="#E63C3C")
        
        #Place Widgets
        self.file_label.place(relx=0.425,rely=0.5 ,anchor='center')
        self.file_delete_button.place(relx =0.90,rely=0.5,anchor='center')
        
        #Binding Events
        self.bind('<ButtonPress-1>',self.init_file)

    def handle_images(self):
        self.trash_icon_black = Image.open('trash_icon_black.png')
        self.trash_icon_white = Image.open('trash_icon_white.png')
        self.trash_icon_ctk = ctk.CTkImage(self.trash_icon_black,self.trash_icon_white)

    def init_file(self,event):
        file_name = self.file_name.get()
        file_path_index = self.file_display.file_name_list.index(file_name)
        self.file_path = self.file_display.file_path_list[file_path_index]

        if self.file_init:
            print(f'Loading {file_name}...')
            self.file_display.io_instance.load_file(self.file_path)
        else:    
            print(f"{file_name} is initializing...")
            file_path_index = self.file_display.file_name_list.index(file_name)
            self.file_path = self.file_display.file_path_list[file_path_index]
            self.file_display.io_instance.load_new_file(self.file_path)
            self.file_display.io_instance.clear_text_box()
            self.file_init = True
            
    def delete(self):
        self.destroy()

# Creating the Response Text box

class IO(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color= 'black')
        self.create_widgets()
        self.place(relx=0.35 ,rely=0.01, relwidth=0.64 ,relheight=0.98)

    def load_new_file(self,file_path):
        self.active_file = file_path
        with open(file_path,'w') as file:
            file.write('')

    def load_file(self,file_path):
        self.clear_text_box()
        with open(file_path) as file:
            content = file.readlines()
        self.init_text_box(content)
        self.active_file = file_path

    def clear_text_box(self):
        self.text_box.delete('1.0','end')

    def init_text_box(self,content):
        for line in content:
            self.text_box.insert('end',line)

    def generate_response_text(self,entry_text):

        if entry_text:
            self.entry_text = entry_text
            if "search" in self.entry_text.lower():
                query = self.entry_text.replace("search", "").strip()
                api_response = self.search_api(query)
                self.text_box.insert('end', f"User---> {self.entry_text}\n")
                self.text_box.insert('end', f"API <---- {str(api_response)} \n\n")
            else:
                self.bot_reply = action.Action(self.entry_text).handle_action()
                with open(self.active_file,'a') as file:
                    file.write(f"User---> {self.entry_text}\nBOT <---- {str(self.bot_reply)} \n\n")
                self.text_box.insert('end',f"User---> {self.entry_text}\n")
                self.text_box.insert('end' , f"BOT <---- {str(self.bot_reply)} \n\n")
            if self.bot_reply == "Ok sir" :
                self.master.destroy()
        else: 
            self.bot_reply = 'Input was not received'
            self.bot_reply = action.Action(self.bot_reply).handle_action()
            self.text_box.insert('end' , f"BOT <---- {str(self.bot_reply)} \n\n")
    
    def create_widgets(self):

        # Making Widgets
        self.text_box = ctk.CTkTextbox(self, fg_color = 'black' )
        self.text_box.configure(font = ('DestructoBeam BB',20))  
        self.input_box = InputBox(self,'transparent',io_instance = self)

        # Widget Layout
        self.text_box.place(
            relx=0.01,
            rely=0.01,
            relwidth=0.98,
            relheight=0.89)
        
        self.input_box.place(
            relx=0.507,
            rely=0.93,
            relwidth=0.95,
            relheight=0.07,
            anchor='center')

# Creating the Entry Widget

class InputBox(ctk.CTkFrame):
    def __init__(self , master , fg_color, io_instance):
        super().__init__(master,fg_color = fg_color) 
        self.handle_images()
        self.create_widgets()
        self.io_instance = io_instance

    def handle_entry(self):
        self.entry_text = self.entry.get()
        self.io_instance.generate_response_text(self.entry_text)

    def speech_to_text(self):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            audio = r.listen(source)
            try:
                voice_data=""
                voice_data = r.recognize_google(audio)
                return voice_data
            except sr.UnknownValueError:
                print("Sorry , not able to hear you")    
            except sr.RequestError:
                print("RequestError")


    def handle_mic_input(self):
        self.mic_input = self.speech_to_text()
        self.io_instance.generate_response_text(self.mic_input)

    def handle_images(self):
        self.mic_icon_white =Image.open('mic_icon_white.png')
        self.mic_icon_black =Image.open('mic_icon_black.png')
        self.mic_icon_ctk = ctk.CTkImage(self.mic_icon_black,self.mic_icon_white)
        
    def create_widgets(self):

        # Making Widgets
        self.mic_button = ctk.CTkButton(
            self,
            text = '',
            compound = 'left',
            image = self.mic_icon_ctk,
            command = self.handle_mic_input,
            corner_radius = 15,
            # border_spacing =1 
            )
        self.ask_button = ctk.CTkButton(
            self ,
            text = "  Ask",
            command = self.handle_entry,
            font = ('Comic Sans MC',15),
            corner_radius = 15
            # border_color='#575757'
            )
        self.frame1 = ctk.CTkFrame(self,
            fg_color='transparent',
            )
        self.entry = ctk.CTkEntry(
            self.frame1,
            fg_color='transparent',
            corner_radius = 15
            )

        # Placing Widgets

        self.frame1.place(
            relx = 0,
            rely = 0,
            relwidth = 0.80,
            relheight = 1)
        
        self.entry.place(
            relx = 0,
            rely = 0,
            relwidth = 1.1,
            relheight = 1)
        
        self.ask_button.place(
            relx = 0.78,
            rely = 0,
            relwidth = 0.11,
            relheight = 1)
        
        self.mic_button.place(
            relx = 0.91,
            rely = 0,
            relwidth = 0.074,
            relheight = 1)

        # Binding Events

        self.entry.bind('<Return>', lambda event: self.handle_entry())
        
if __name__ == '__main__':
    virtual_assistant = App('Virtual Assistant',[960,540])