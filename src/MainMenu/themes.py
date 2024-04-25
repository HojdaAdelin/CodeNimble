import tkinter as tk
import customtkinter as ct

def dark_theme(menu_bar, cascade1, cascade2, 
               cascade3, cascade4, cascade5, cascade6,
               drop1, drop2, drop3, drop4, drop5, drop6,
               status, text):

    menu_bar.configure(bg_color="#333333")
    cascade1.configure(hover_color="#4d4d4d", text_color="white")
    cascade2.configure(hover_color="#4d4d4d", text_color="white")
    cascade3.configure(hover_color="#4d4d4d", text_color="white")
    cascade4.configure(hover_color="#4d4d4d", text_color="white")
    cascade5.configure(hover_color="#4d4d4d", text_color="white")
    cascade6.configure(hover_color="#4d4d4d", text_color="white")
    drop1.configure(fg_color="#333333", text_color="white",hover_color="#4d4d4d", bg_color="#333333")
    drop2.configure(fg_color="#333333", text_color="white",hover_color="#4d4d4d", bg_color="#333333")
    drop3.configure(fg_color="#333333", text_color="white",hover_color="#4d4d4d", bg_color="#333333")
    drop4.configure(fg_color="#333333", text_color="white",hover_color="#4d4d4d", bg_color="#333333")
    drop5.configure(fg_color="#333333", text_color="white",hover_color="#4d4d4d", bg_color="#333333")
    drop6.configure(fg_color="#333333", text_color="white",hover_color="#4d4d4d", bg_color="#333333")
    status.configure(bg="#333333")
    status.status_label.configure(bg="#333333", fg="white")
    text.text.configure(bg="#2b2b2b", foreground="white",insertbackground='white',selectbackground="#4d4d4d")
    text.scrollbar.configure(fg_color="#2b2b2b", button_color="#5c5c5c", button_hover_color="#858585")
    text.scrollhor.configure(fg_color="#2b2b2b", button_color="#5c5c5c", button_hover_color="#858585")
    text.numberLines.configure(bg='#333333')

def light_theme(menu_bar, cascade1, cascade2, 
               cascade3, cascade4, cascade5, cascade6,
               drop1, drop2, drop3, drop4, drop5, drop6,
               status, text, win):
    
    menu_bar.configure(bg_color="white")
    cascade1.configure(hover_color="#ebebeb", text_color="black")
    cascade2.configure(hover_color="#ebebeb", text_color="black")
    cascade3.configure(hover_color="#ebebeb", text_color="black")
    cascade4.configure(hover_color="#ebebeb", text_color="black")
    cascade5.configure(hover_color="#ebebeb", text_color="black")
    cascade6.configure(hover_color="#ebebeb", text_color="black")
    drop1.configure(fg_color="white", text_color="black",hover_color="#ebebeb", bg_color="white")
    drop2.configure(fg_color="white", text_color="black",hover_color="#ebebeb", bg_color="white")
    drop3.configure(fg_color="white", text_color="black",hover_color="#ebebeb", bg_color="white")
    drop4.configure(fg_color="white", text_color="black",hover_color="#ebebeb", bg_color="white")
    drop5.configure(fg_color="white", text_color="black",hover_color="#ebebeb", bg_color="white")
    drop6.configure(fg_color="white", text_color="black",hover_color="#ebebeb", bg_color="white")
    status.configure(bg="white")
    status.status_label.configure(bg="white", fg="black")
    text.text.configure(bg="#f0f0f0", foreground="black",insertbackground='black',selectbackground="#d6d6d6")
    text.scrollbar.configure(fg_color="#f0f0f0", button_color="#b0b0b0", button_hover_color="#cccccc")
    text.scrollhor.configure(fg_color="#f0f0f0", button_color="#b0b0b0", button_hover_color="#cccccc")
    text.numberLines.configure(bg='white')
    

def blue_theme():
    pass