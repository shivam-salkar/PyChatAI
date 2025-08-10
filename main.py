from customtkinter import *
import ai
from PIL import Image
from playsound import playsound
import json
import datetime
import os

"""------------------------ TKINTER APP CONFIG --------------------"""

app = CTk()
app.geometry('960x620')
app.title('PyChatAI')
set_appearance_mode("dark")
if app._get_appearance_mode() == 'light':
    app.configure(fg_color="#F1DEDE")
else:
    app.configure(fg_color='#5D576B')

set_widget_scaling(1)
app.resizable(False, False)

os.makedirs('assets/', exist_ok=TRUE)
os.makedirs('assets/history', exist_ok=TRUE)
file_path = 'assets/history/data.json'



"""---------------------- FUNCTIONS -------------------------"""

def change_theme():

    playsound('assets/click.mp3')
    current_mode = app._get_appearance_mode()
    if current_mode == "light":
        set_appearance_mode("dark")
        app.configure(fg_color='#5D576B')
        
    else:
        set_appearance_mode("light")
        app.configure(fg_color="#F1DEDE")
        
    
def ask():

    if input_bar_text.get().strip() == '':
        start_label = CTkLabel(app, text="Please enter something!", font=("Segoe UI bold" , 21), fg_color='black')
        start_label.place(relx=0.5, rely=0.01, anchor="n")
        app.after(1000, start_label.destroy)
        return
    
    user_input = input_bar_text.get()
    prompt = f"You are a helpful assistant. Answer the following question concisely and clearly:\n\nQuestion: {user_input}\n\nAnswer:"
    response = ai.return_prompt(prompt)

    
    textbox.delete('0.0', 'end')
    textbox.insert('end', response)
    
    x = datetime.datetime.now()
    timestamp = x.strftime('%Y-%m-%d %H:%M:%S')
    
    
    
    try:
        with open(file_path) as rfile:
            history = json.load(rfile)
    except (json.JSONDecodeError, FileNotFoundError):
        history = {}
    
    history[timestamp] = {
        "question": user_input,
        "answer": response
    }
    
    with open(file_path, 'w') as file:
        json.dump(history, file, indent=2)
    
    
    new_button = CTkButton(
    sidebar_frame,
    text=user_input[:25],
    corner_radius=50,
    fg_color='transparent',
    text_color='#5D576B',
    anchor='w',
    width=240,
    font=('Arial bold', 15),
    hover_color="#C6C6C6",
    command=lambda qt=user_input: history_button_click(qt)
    )
    new_button.pack(pady=5)

    
def sound_button_click():
    ai.tts(textbox.get('0.0', 'end'))

"""------------------------ HISTORY MANAGEMENT----------------"""

def history_button_click(question_text):
        
        new_win = CTkToplevel(app)
        new_win.geometry("600x500")
        new_win.title("PyChatAI History")
        new_win.resizable(False, False)
        new_win.transient(app)    
        new_win.grab_set()        
        new_win.focus()
        
        with open(file_path) as rfile:
            data: dict = json.load(rfile)
        
        
        
        for time, questions in reversed(data.items()):
           if questions['question'] == question_text:
            
            text = CTkTextbox(new_win, width=new_win.winfo_width(), height=new_win.winfo_height(), wrap='word', font=('Arial bold', 16))
            text.pack()
            text.insert(0.0, f'[Question]: \n{questions["question"]}\n\n[Answer]: \n{questions["answer"]}')
            text.configure(state='disabled')
            break


def set_history():
    
    
        
    
    with open(file_path) as rfile:
        data: dict = json.load(rfile)
        
        for time, question in reversed(data.items()):
            new_btn = CTkButton(sidebar_frame,command=lambda qt=question['question']: history_button_click(qt), text=question['question'][:25], corner_radius=50, fg_color='transparent', text_color='#5D576B', anchor='w', width=240, font=('Arial bold', 15), hover_color="#C6C6C6", )
            new_btn.pack(pady=5)
            
def clear_history():
   
    with open(file_path, 'w') as wfile:
        json.dump({}, wfile)
    
    for widget in sidebar_frame.winfo_children():
        widget.destroy()
        
    input_bar_text.delete(0, 'end')
    textbox.delete(0.0, 'end')
    

"""------------------------ WIDGET CONFIG --------------------"""

welcome_label_img = CTkImage(light_image=Image.open("assets/Welcome How can I help you.png"), dark_image=Image.open("assets/dark/Welcome How can I help you.png"),size=(480, 32))
sidebar_img = CTkImage(light_image=Image.open('assets/sidebar.png'), size=(258, 620), dark_image=Image.open('assets/dark/sidebar.png'))
theme_icon_img = CTkImage(light_image=Image.open('assets/theme_icon.png'), size=(69,69))
history_img = CTkImage(light_image=Image.open('assets/history.png'), dark_image=Image.open('assets/history.png'), size=(200, 30))
bar_img = CTkImage(light_image=Image.open('assets/bar.png'), dark_image=Image.open('assets/bar.png'), size=(500, 50))
delete_img = CTkImage(light_image=Image.open('assets/delete.png'), size=(50,50))
sound_img = CTkImage(light_image=Image.open('assets/volume.png'), size=(50,50))

welcome_label = CTkLabel(app, image=welcome_label_img, text='')
sidebar_background = CTkLabel(app, image=sidebar_img, text='')
sidebar_frame = CTkScrollableFrame(app, width=230, height=400, fg_color=("#D9D9D9", "#262626"), corner_radius=0)
theme_icon_btn = CTkButton(app, image=theme_icon_img, text='', fg_color=("#D9D9D9", "#262626"), corner_radius=0, width=50, hover_color="#A3A3A3", command=change_theme)
history_label = CTkLabel(app, text='History', fg_color=("#D9D9D9", "#262626"), font=('Arial bold', 36), text_color=('#5D576B', '#F1DEDE'))
input_bar_text = CTkEntry(app, width=440, height=36, placeholder_text='Ask me anything...', fg_color=('#D9D9D9', '#D9D9D9'), corner_radius=100, font=('Arial bold', 18), text_color='black')
input_button = CTkButton(app, command=ask, width=40, height=34, corner_radius=100, font=('Arial bold', 12), fg_color=('#D9D9D9', '#D9D9D9'), text_color='#262626', border_width=1, border_color="#515151", text='>>>')
input_bar_label = CTkLabel(app, text='', image=bar_img)
textbox = CTkTextbox(app, width=480, height=400, border_spacing=20, font=('Arial bold', 16), corner_radius=20, wrap='word')
sound_button = CTkButton(app, width=50, height=50, command=sound_button_click, text='', image=sound_img, fg_color='transparent', hover_color="#A3A3A3")
delete_history_button = CTkButton(app, width=50, height=50, command=clear_history, text='', image=delete_img, fg_color='transparent', hover_color="#A3A3A3")

"""------------------------ WIDGET PACKING --------------------"""

welcome_label.place(x=306, y=60)
sidebar_background.place(x=0, y=0)
sidebar_frame.place(x=0, y=160)
theme_icon_btn.place(x=100, y=20)
history_label.place(x=20, y=100)
input_bar_text.place(x=290, y=125)
input_button.place(x=740, y=125)
input_bar_text.lift()
textbox.place(x=300, y= 180)
sound_button.place(x=800, y=430)
delete_history_button.place(x=800, y=500)

"""------------------------ FINAL MAINLOOP --------------------"""

if __name__ == '__main__':
    set_history()
    app.mainloop()
    
