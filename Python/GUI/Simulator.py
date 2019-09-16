#!/usr/bin/python3
# -*- coding:utf-8 -*-

import threading
import select
import time
import tkinter
from tkinter import *
from tkinter.messagebox import showinfo
from tkinter.ttk import *
from tkinter import messagebox

import UDP                               # E19 UDP module

LOCAL_MODE = True
DEBUG_MODE = True
ENABLE_THREAD = True


class Simulator_GUI:

    def __init__(self, window, sock):

        # Assign to self
        self.window = window
        self.sock = sock

        # global variables
        self.message = ["\n"]           # init message in console
        self.F = ("Helvetica", 16)      # Font of big words
        self.sF = ("Helvetica", 8)      # Font of hardware address
        self.hwbg = '#F8F8FF'           # Change color of HW text box
        self.defbg = '#C0C0C0'          # Default color
        self.ON = "#FFD700"             # When LED is on
        self.OFF = "#F0F0F0"            # When LED is off
        self.thread_quit_flag = False   # Easy to do clean up work

        # Draw the GUI
        self.init_GUI()     # setting [title && geometry]
        self.add_menu()     # Adding  [main menu && About us]
        self.add_panel()    # Adding  [frame for panel && console].
        self.add_console()  # Adding  [Message console]
        self.add_seeting()  # Adding  [Slave Configuration]

        # Read init state
        self.states = {}    # initial the state of the panel
        self.init_state()   # Generate the init state of the panel

        # Start running UDP
        if ENABLE_THREAD:
            receiver_thread = threading.Thread(target=self.reciver)
            receiver_thread.start()

        # When GUI about to quit, take over and run close_callback()
        window.protocol("WM_DELETE_WINDOW", self.close_callback)

        # Start the GUI
        window.mainloop()


    """====================== INIT ======================"""

    def init_GUI(self):

        # Set title
        self.window.title("This is a cool name : THE Emulator :D")

        # centralize the windows
        width_limit = (self.window.winfo_screenwidth() - 800) / 2
        height_limit = (self.window.winfo_screenheight() - 740) / 2
        self.window.geometry("800x740+{0:.0f}+{1:.0f}".format(width_limit, height_limit))

        # Fix the width and height
        self.window.resizable(False, False)


    """======================Draw the GUI======================"""

    def add_menu(self):

        # create a Top menu
        menubar = Menu(self.window)

        # create main menu
        mainmenu = Menu(menubar, tearoff=False)
        mainmenu.add_command(label='Testing', command=self.Menu_testing)
        mainmenu.add_separator()
        mainmenu.add_command(label='Exit', command=self.close_callback)
        menubar.add_cascade(label='Menu', menu=mainmenu)

        # create "About us"
        menubar.add_command(label='About us', command=self.Menu_about_us)

        # Start the menu
        self.window.config(menu=menubar)


    def add_console(self):

        # Adding labelFrame with hw:200*800
        self.console_frame = Labelframe(self.window, text="Message Console").place(x=10, y=400, height=210, width=800)

        # Adding message
        self.console_message = Message(self.console_frame, text = "\n\n\n\n\n\n\n\n\n", width=780)
        self.console_message.place(in_=self.console_frame, x=20, y=420)


    def add_seeting(self):

        # Basic grid start from x=20, y=620
        x_variable = 20
        y_variable = 620

        # Draw the label
        Label(self.panel_frame, text="Button Slave").place(x=x_variable+100, y=y_variable)
        Label(self.panel_frame, text="LED Slave").place(x=x_variable+200, y=y_variable)
        Label(self.panel_frame, text="Other Slave").place(x=x_variable+300, y=y_variable)
        Label(self.panel_frame, text="Board Type").place(x=x_variable, y=y_variable+30)
        Label(self.panel_frame, text="Borad Number").place(x=x_variable, y=y_variable+60)

        # Entrys: types
        self.but_type = Text(self.panel_frame, width=7, height=1, background=self.hwbg)
        self.but_type.insert(END, "0")
        self.but_type.place(x=x_variable+100, y=y_variable+30)
        self.led_type = Text(self.panel_frame, width=7, height=1, background=self.hwbg)
        self.led_type.insert(END, "0")
        self.led_type.place(x=x_variable+200, y=y_variable+30)
        self.oth_type = Text(self.panel_frame, width=7, height=1, background=self.hwbg)
        self.oth_type.insert(END, "0")
        self.oth_type.place(x=x_variable+300, y=y_variable+30)

        # Entrys: numbers
        self.but_numb = Text(self.panel_frame, width=7, height=1, background=self.hwbg)
        self.but_numb.insert(END, "0")
        self.but_numb.place(x=x_variable+100, y=y_variable+60)
        self.led_numb = Text(self.panel_frame, width=7, height=1, background=self.hwbg)
        self.led_numb.insert(END, "0")
        self.led_numb.place(x=x_variable+200, y=y_variable+60)
        self.oth_numb = Text(self.panel_frame, width=7, height=1, background=self.hwbg)
        self.oth_numb.insert(END, "0")
        self.oth_numb.place(x=x_variable+300, y=y_variable+60)


    def add_panel(self):

        # Adding Frame with frame hw:600*800
        self.panel_frame = tkinter.Frame(height=380, width=800, bg=self.defbg).pack(fill=BOTH, side=TOP, padx=15, pady=15)

        # 7 segs and potentionmeter
        self.add_7seg_potentionmeters()

        # Dials
        self.add_dials()

        # LEDs
        self.add_leds()

        # Buttons
        self.add_buttons()


    def add_7seg_potentionmeters(self):

        # Widget distance: {50}50{100}150{50}50{100}
        y_variable = 30

        Label(self.panel_frame, text="7 Seg: ").place(x=50, y=y_variable)
        self.seven_segs_L = Text(self.panel_frame, width=5, height=1)
        self.seven_segs_L.insert(END, "0")
        self.seven_segs_L.place(x=100, y=y_variable)

        Label(self.panel_frame, text="Potentionmeter: ").place(x=200, y=y_variable)
        self.poten_L = tkinter.Label(self.panel_frame, text='0', width=5, height=1)
        self.poten_L.place(x=300, y=y_variable)

        Label(self.panel_frame, text="Potentionmeter: ").place(x=450, y=y_variable)
        self.poten_R = tkinter.Label(self.panel_frame, text='0', width=5, height=1)
        self.poten_R.place(x=550, y=y_variable)

        Label(self.panel_frame, text="7 Seg: ").place(x=650, y=y_variable)
        self.seven_segs_R = Text(self.panel_frame, width=5, height=1)
        self.seven_segs_R.insert(END, "0")
        self.seven_segs_R.place(x=700, y=y_variable)

        # Hardware address
        HW_label = Label(self.panel_frame, text="HW addr: ", background=self.defbg, font=self.sF).place(x=25, y=y_variable+32)
        self.seven_segs_L_addr = Text(self.panel_frame, width=4, height=1, background=self.hwbg)
        self.seven_segs_L_addr.insert(END, "0")
        self.seven_segs_L_addr.place(x=100, y=y_variable+30)

        self.poten_L_addr = Text(self.panel_frame, width=4, height=1, background=self.hwbg)
        self.poten_L_addr.insert(END, "0")
        self.poten_L_addr.place(x=300, y=y_variable+30)

        self.poten_R_addr = Text(self.panel_frame, width=4, height=1, background=self.hwbg)
        self.poten_R_addr.insert(END, "0")
        self.poten_R_addr.place(x=550, y=y_variable+30)

        self.seven_segs_R_addr = Text(self.panel_frame, width=4, height=1, background=self.hwbg)
        self.seven_segs_R_addr.insert(END, "0")
        self.seven_segs_R_addr.place(x=700, y=y_variable+30)


    def add_dials(self):

        y_variable = 130

        Label(self.panel_frame, text="Dial 1", font=self.F).place(x=150, y= 100)
        Label(self.panel_frame, text="Dial 2", font=self.F).place(x=550, y= 100)

        self.dial_L = Text(self.panel_frame, width=20, height=3)
        self.dial_L.insert(END, "0")
        self.dial_L.place(x=100, y=y_variable)
        self.dial_R = Text(self.panel_frame, width=20, height=3)
        self.dial_R.insert(END, "0")
        self.dial_R.place(x=500, y=y_variable)

        # Apply button
        self.apply = tkinter.Button(self.panel_frame, text="Send to Panel", height=1, width=12, relief=GROOVE, font=self.F, command=self.Apply_button_handler)
        self.apply.place(x=310, y=y_variable)

        # Hardware address
        Label(self.panel_frame, text="HW addr: ", background=self.defbg, font=self.sF).place(x=25, y=y_variable+60)
        self.dial_L_addr = Text(self.panel_frame, width=4, height=1, background=self.hwbg)
        self.dial_L_addr.insert(END, "0")
        self.dial_L_addr.place(x=100, y=y_variable+60)

        self.dial_R_addr = Text(self.panel_frame, width=4, height=1, background=self.hwbg)
        self.dial_R_addr.insert(END, "0")
        self.dial_R_addr.place(x=500, y=y_variable+60)


    def add_leds(self):

        y_variable = 230
        self.led_21_L = tkinter.Label(self.panel_frame, text="State 1")
        self.led_21_L.place(x=30, y=y_variable)
        self.led_22_L = tkinter.Label(self.panel_frame, text="State 2")
        self.led_22_L.place(x=80, y=y_variable)

        self.led_switch_L = tkinter.Label(self.panel_frame, text="1_pos")
        self.led_switch_L.place(x=150, y=y_variable)

        self.led_1_L_flag = 0
        self.led_1_L = tkinter.Label(self.panel_frame, text="LED 1")
        self.led_1_L.place(x=220, y=y_variable)
        self.led_2_L_flag = 0
        self.led_2_L = tkinter.Label(self.panel_frame, text="LED 2")
        self.led_2_L.place(x=260, y=y_variable)
        self.led_3_L_flag = 0
        self.led_3_L = tkinter.Label(self.panel_frame, text="LED 3")
        self.led_3_L.place(x=300, y=y_variable)
        self.led_4_L_flag = 0
        self.led_4_L = tkinter.Label(self.panel_frame, text="LED 4")
        self.led_4_L.place(x=340, y=y_variable)

        # Symmetrical
        self.led_1_R_flag = 0
        self.led_1_R = tkinter.Label(self.panel_frame, text="LED 1")
        self.led_1_R.place(x=400, y=y_variable)
        self.led_2_R_flag = 0
        self.led_2_R = tkinter.Label(self.panel_frame, text="LED 2")
        self.led_2_R.place(x=440, y=y_variable)
        self.led_3_R_flag = 0
        self.led_3_R = tkinter.Label(self.panel_frame, text="LED 3")
        self.led_3_R.place(x=480, y=y_variable)
        self.led_4_R_flag = 0
        self.led_4_R = tkinter.Label(self.panel_frame, text="LED 4")
        self.led_4_R.place(x=520, y=y_variable)

        self.led_switch_R = tkinter.Label(self.panel_frame, text="1_pos")
        self.led_switch_R.place(x=600, y=y_variable)

        self.led_21_R = tkinter.Label(self.panel_frame, text="State 2")
        self.led_21_R.place(x=665, y=y_variable)
        self.led_22_R = tkinter.Label(self.panel_frame, text="State 1")
        self.led_22_R.place(x=715, y=y_variable)

        # Hardware Address
        self.led_21_L_addr = Text(self.panel_frame, width=4, height=1, background=self.hwbg)
        self.led_21_L_addr.insert(END, "0")
        self.led_21_L_addr.place(x=30, y=y_variable+30)
        self.led_22_L_addr = Text(self.panel_frame, width=4, height=1, background=self.hwbg)
        self.led_22_L_addr.insert(END, "0")
        self.led_22_L_addr.place(x=80, y=y_variable+30)

        self.led_switch_L_addr = Text(self.panel_frame, width=4, height=1, background=self.hwbg)
        self.led_switch_L_addr.insert(END, "0")
        self.led_switch_L_addr.place(x=150, y=y_variable+30)

        self.led_1_L_addr = Text(self.panel_frame, width=4, height=1, background=self.hwbg)
        self.led_1_L_addr.insert(END, "0")
        self.led_1_L_addr.place(x=220, y=y_variable+30)
        self.led_2_L_addr = Text(self.panel_frame, width=4, height=1, background=self.hwbg)
        self.led_2_L_addr.insert(END, "0")
        self.led_2_L_addr.place(x=260, y=y_variable+30)
        self.led_3_L_addr = Text(self.panel_frame, width=4, height=1, background=self.hwbg)
        self.led_3_L_addr.insert(END, "0")
        self.led_3_L_addr.place(x=300, y=y_variable+30)
        self.led_4_L_addr = Text(self.panel_frame, width=4, height=1, background=self.hwbg)
        self.led_4_L_addr.insert(END, "0")
        self.led_4_L_addr.place(x=340, y=y_variable+30)

        # Symmetrical
        self.led_1_R_addr = Text(self.panel_frame, width=4, height=1, background=self.hwbg)
        self.led_1_R_addr.insert(END, "0")
        self.led_1_R_addr.place(x=400, y=y_variable+30)
        self.led_2_R_addr = Text(self.panel_frame, width=4, height=1, background=self.hwbg)
        self.led_2_R_addr.insert(END, "0")
        self.led_2_R_addr.place(x=440, y=y_variable+30)
        self.led_3_R_addr = Text(self.panel_frame, width=4, height=1, background=self.hwbg)
        self.led_3_R_addr.insert(END, "0")
        self.led_3_R_addr.place(x=480, y=y_variable+30)
        self.led_4_R_addr = Text(self.panel_frame, width=4, height=1, background=self.hwbg)
        self.led_4_R_addr.insert(END, "0")
        self.led_4_R_addr.place(x=520, y=y_variable+30)

        self.led_switch_R_addr = Text(self.panel_frame, width=4, height=1, background=self.hwbg)
        self.led_switch_R_addr.insert(END, "0")
        self.led_switch_R_addr.place(x=600, y=y_variable+30)

        self.led_21_R_addr = Text(self.panel_frame, width=4, height=1, background=self.hwbg)
        self.led_21_R_addr.insert(END, "0")
        self.led_21_R_addr.place(x=665, y=y_variable+30)
        self.led_22_R_addr = Text(self.panel_frame, width=4, height=1, background=self.hwbg)
        self.led_22_R_addr.insert(END, "0")
        self.led_22_R_addr.place(x=715, y=y_variable+30)

    def add_buttons(self):

        y_variable = 305

        # 2 pos switch
        self.pos_L = IntVar()
        self.switch_1_L = tkinter.Radiobutton(self.panel_frame, text="State 1", variable=self.pos_L, value=0, command=self.Switch_2_L)
        self.switch_1_L.place(x=50, y=y_variable)
        self.switch_2_L = tkinter.Radiobutton(self.panel_frame, text="State 2", variable=self.pos_L, value=1, command=self.Switch_2_L)
        self.switch_2_L.place(x=50, y=y_variable+25)

        # 1 pos switch
        self.switch_L_flag = 1
        self.switch_L = tkinter.Button(self.panel_frame, text="OFF", height=1, width=4, relief=RAISED, command=self.Switch_L)
        self.switch_L.place(x=150, y=y_variable)

        # buttons
        self.button_1_L = tkinter.Button(self.panel_frame, text="1", height=1, width=4, command=self.but_1_L)
        self.button_1_L.place(x=220, y=y_variable)
        self.button_2_L = tkinter.Button(self.panel_frame, text="2", height=1, width=4, command=self.but_2_L)
        self.button_2_L.place(x=260, y=y_variable)
        self.button_3_L = tkinter.Button(self.panel_frame, text="3", height=1, width=4, command=self.but_3_L)
        self.button_3_L.place(x=300, y=y_variable)
        self.button_4_L = tkinter.Button(self.panel_frame, text="4", height=1, width=4, command=self.but_4_L)
        self.button_4_L.place(x=340, y=y_variable)

        # buttons
        self.button_1_R = tkinter.Button(self.panel_frame, text="1", height=1, width=4, command=self.but_1_R)
        self.button_1_R.place(x=400, y=y_variable)
        self.button_2_R = tkinter.Button(self.panel_frame, text="2", height=1, width=4, command=self.but_2_R)
        self.button_2_R.place(x=440, y=y_variable)
        self.button_3_R = tkinter.Button(self.panel_frame, text="3", height=1, width=4, command=self.but_3_R)
        self.button_3_R.place(x=480, y=y_variable)
        self.button_4_R = tkinter.Button(self.panel_frame, text="4", height=1, width=4, command=self.but_4_R)
        self.button_4_R.place(x=520, y=y_variable)

        # 1 pos switch
        self.switch_R_flag = 1
        self.switch_R = tkinter.Button(self.panel_frame, text="OFF", height=1, width=4, relief=RAISED, command=self.Switch_R)
        self.switch_R.place(x=600, y=y_variable)

        # 2 pos switch
        self.pos_R = IntVar()
        self.switch_1_R = tkinter.Radiobutton(self.panel_frame, text="State 1", variable=self.pos_R, value=0, command=self.Switch_2_R)
        self.switch_1_R.place(x=680, y=y_variable)
        self.switch_2_R = tkinter.Radiobutton(self.panel_frame, text="State 2", variable=self.pos_R, value=1, command=self.Switch_2_R)
        self.switch_2_R.place(x=680, y=y_variable+25)


        # Hardware Address

        self.switch_1_L_addr = Text(self.panel_frame, width=4, height=1, background=self.hwbg)
        self.switch_1_L_addr.insert(END, "0")
        self.switch_1_L_addr.place(x=50, y=y_variable+60)

        self.switch_L_addr = Text(self.panel_frame, width=4, height=1, background=self.hwbg)
        self.switch_L_addr.insert(END, "0")
        self.switch_L_addr.place(x=150, y=y_variable+60)

        self.button_1_L_addr = Text(self.panel_frame, width=4, height=1, background=self.hwbg)
        self.button_1_L_addr.insert(END, "0")
        self.button_1_L_addr.place(x=220, y=y_variable+60)
        self.button_2_L_addr = Text(self.panel_frame, width=4, height=1, background=self.hwbg)
        self.button_2_L_addr.insert(END, "0")
        self.button_2_L_addr.place(x=260, y=y_variable+60)
        self.button_3_L_addr = Text(self.panel_frame, width=4, height=1, background=self.hwbg)
        self.button_3_L_addr.insert(END, "0")
        self.button_3_L_addr.place(x=300, y=y_variable+60)
        self.button_4_L_addr = Text(self.panel_frame, width=4, height=1, background=self.hwbg)
        self.button_4_L_addr.insert(END, "0")
        self.button_4_L_addr.place(x=340, y=y_variable+60)

        self.button_1_R_addr = Text(self.panel_frame, width=4, height=1, background=self.hwbg)
        self.button_1_R_addr.insert(END, "0")
        self.button_1_R_addr.place(x=400, y=y_variable+60)
        self.button_2_R_addr = Text(self.panel_frame, width=4, height=1, background=self.hwbg)
        self.button_2_R_addr.insert(END, "0")
        self.button_2_R_addr.place(x=440, y=y_variable+60)
        self.button_3_R_addr = Text(self.panel_frame, width=4, height=1, background=self.hwbg)
        self.button_3_R_addr.insert(END, "0")
        self.button_3_R_addr.place(x=480, y=y_variable+60)
        self.button_4_R_addr = Text(self.panel_frame, width=4, height=1, background=self.hwbg)
        self.button_4_R_addr.insert(END, "0")
        self.button_4_R_addr.place(x=520, y=y_variable+60)

        self.switch_R_addr = Text(self.panel_frame, width=4, height=1, background=self.hwbg)
        self.switch_R_addr.insert(END, "0")
        self.switch_R_addr.place(x=600, y=y_variable+60)

        self.switch_1_R_addr = Text(self.panel_frame, width=4, height=1, background=self.hwbg)
        self.switch_1_R_addr.insert(END, "0")
        self.switch_1_R_addr.place(x=680, y=y_variable+60)


    """======================Detect the event and react======================"""


    """------ Buttons ------"""
    def Apply_button_handler(self):

        # Testing part: gather data and print out to console
        if DEBUG_MODE:
            v_seg_L = str(self.seven_segs_L.get("1.0",END)).strip()
            v_seg_R = str(self.seven_segs_R.get("1.0",END)).strip()
            v_dial_L = str(self.dial_L.get("1.0",END)).strip()
            v_dial_R = str(self.dial_R.get("1.0",END)).strip()
            data_list = [v_seg_L, v_seg_R, v_dial_L, v_dial_R]
            data_name = ["Left 7Seg", "Right 7Seg", "Left Dial", "Right Dial"]
            for num in range(len(data_list)):
                self.Update_message("{0:<10}: {1:<3}\n".format(data_name[num], data_list[num]))

        # It's time to send the UDP
        self.sender()

    def but_1_L(self, send_flag=True):
        self.led_1_L_flag = self.LED_toggle(self.led_1_L, self.led_1_L_flag)
        if send_flag:
            self.sender()
    def but_2_L(self, send_flag=True):
        self.led_2_L_flag = self.LED_toggle(self.led_2_L, self.led_2_L_flag)
        if send_flag:
            self.sender()
    def but_3_L(self, send_flag=True):
        self.led_3_L_flag = self.LED_toggle(self.led_3_L, self.led_3_L_flag)
        if send_flag:
            self.sender()
    def but_4_L(self, send_flag=True):
        self.led_4_L_flag = self.LED_toggle(self.led_4_L, self.led_4_L_flag)
        if send_flag:
            self.sender()
    def but_1_R(self, send_flag=True):
        self.led_1_R_flag = self.LED_toggle(self.led_1_R, self.led_1_R_flag)
        if send_flag:
            self.sender()
    def but_2_R(self, send_flag=True):
        self.led_2_R_flag = self.LED_toggle(self.led_2_R, self.led_2_R_flag)
        if send_flag:
            self.sender()
    def but_3_R(self, send_flag=True):
        self.led_3_R_flag = self.LED_toggle(self.led_3_R, self.led_3_R_flag)
        if send_flag:
            self.sender()
    def but_4_R(self, send_flag=True):
        self.led_4_R_flag = self.LED_toggle(self.led_4_R, self.led_4_R_flag)
        if send_flag:
            self.sender()


    """------ LEDs ------"""
    def LED_toggle(self, item, flag):

        if (flag % 2) == 0:
            item.config(bg=self.ON)
            self.Update_message("LED ON\n")
        else:
            item.config(bg=self.OFF)
            self.Update_message("LED OFF\n")
        flag = (1 + flag) % 2
        return flag


    """------ Switchs ------"""
    def Switch_L(self, send_flag=True):

        self.switch_L_flag += 1
        if(self.switch_L_flag % 2 == 0):
            self.switch_L['relief']=SUNKEN
            self.led_switch_L['bg']=self.ON
            self.switch_L['text']="ON"
        else:
            self.switch_L['relief']=RAISED
            self.led_switch_L['bg']=self.OFF
            self.switch_L['text']="OFF"
        self.switch_L_flag = self.switch_L_flag % 2 
        if send_flag:
            self.sender()

    def Switch_R(self, send_flag=True):

        self.switch_R_flag += 1
        if(self.switch_R_flag % 2 == 0):
            self.switch_R['relief']=SUNKEN
            self.led_switch_R['bg']=self.ON
            self.switch_R['text']="ON"
        else:
            self.switch_R['relief']=RAISED
            self.led_switch_R['bg']=self.OFF
            self.switch_R['text']="OFF"
        self.switch_R_flag = self.switch_R_flag % 2 
        if send_flag:
            self.sender()

    def Switch_2_R(self, send_flag=True):

        if self.pos_R.get() == 1:
            self.led_21_R.config(bg=self.ON)
            self.led_22_R.config(bg=self.OFF)
        else:
            self.led_21_R.config(bg=self.OFF)
            self.led_22_R.config(bg=self.ON)
        if send_flag:
            self.sender()
    def Switch_2_L(self, send_flag=True):

        if self.pos_L.get() == 1:
            self.led_22_L.config(bg=self.ON)
            self.led_21_L.config(bg=self.OFF)
        else:
            self.led_22_L.config(bg=self.OFF)
            self.led_21_L.config(bg=self.ON)
        if send_flag:
            self.sender()


    """------ Menus ------"""

    def Menu_testing(self):
        self.Update_message("Testing\n")

    def Menu_about_us(self):
        showinfo(title="About us", message="This is E19")

    def close_callback(self):
        self.thread_quit_flag = True        # Clean up work for UDP Thread
        tkinter.messagebox.showinfo('~~~~~Hello World~~~~~',"GUESS WHAT! I am about to quit!!")
        self.window.destroy()               # Quit GUI


    """====================== Update ======================"""
    def Update_message(self, new_message=None):

        # Adding new message into self
        if new_message:
            self.message += [new_message]

        # when adding new line, remove old \n
        while("\n" in self.message):
            self.message.remove("\n")

        # Clear buffer limit the length to 10
        if(len(self.message) > 11):
            self.message = self.message[-11:]
        else:
            self.message += ["\n"] * (len(self.message)-11)

        # Convert list into string
        total_message = ""
        for line in self.message:
            total_message += line

        # Update the message
        self.console_message.configure(text=total_message)


    def Update_state_from_packet(self, packet):
        """Update self.state based on packet"""
        for key, value in self.states.items():
            if int(value.board_add) == int(packet.board_add):
                self.Update_message("match!\n")
                self.states[key].state = value[1],packet.state # update the state
                break
        return 0


    def Update_states_from_GUI(self):
        """TODO: Update state's structure into new dir with class"""

        states = {}
        
        states["seg_L"] = (self.seven_segs_L_addr.get("1.0",END).strip(), int(self.seven_segs_L.get("1.0",END).strip()))
        states["seg_R"] = (self.seven_segs_R_addr.get("1.0",END).strip(), int(self.seven_segs_R.get("1.0",END).strip()))

        states["dial_L"] = (self.dial_L_addr.get("1.0",END).strip(), int(self.dial_L.get("1.0",END).strip()))
        states["dial_R"] = (self.dial_R_addr.get("1.0",END).strip(), int(self.dial_R.get("1.0",END).strip()))

        states["pot_L"] = (self.poten_L_addr.get("1.0",END).strip(),self.poten_L['text'])
        states["pot_R"] = (self.poten_R_addr.get("1.0",END).strip(),self.poten_R['text'])

        states["pos_2L"] = (self.poten_L_addr.get("1.0",END).strip(), self.pos_L.get())
        states["pos_2R"] = (self.poten_R_addr.get("1.0",END).strip(), self.pos_R.get())

        states["pos_1L"] = (self.switch_L_addr.get("1.0",END).strip(), self.switch_L_flag)
        states["pos_1R"] = (self.switch_R_addr.get("1.0",END).strip(), self.switch_R_flag)

        states["led_1L"] = (self.led_1_L_addr.get("1.0",END).strip(), self.led_1_L_flag)
        states["led_2L"] = (self.led_2_L_addr.get("1.0",END).strip(), self.led_2_L_flag)
        states["led_3L"] = (self.led_3_L_addr.get("1.0",END).strip(), self.led_3_L_flag)
        states["led_4L"] = (self.led_4_L_addr.get("1.0",END).strip(), self.led_4_L_flag)
        states["led_1R"] = (self.led_1_R_addr.get("1.0",END).strip(), self.led_1_R_flag)
        states["led_2R"] = (self.led_2_R_addr.get("1.0",END).strip(), self.led_2_R_flag)
        states["led_3R"] = (self.led_3_R_addr.get("1.0",END).strip(), self.led_3_R_flag)
        states["led_4R"] = (self.led_4_R_addr.get("1.0",END).strip(), self.led_4_R_flag)

        return states


    def Update_GUI(self):
        """Update GUI based on new self.states"""

        self.seven_segs_L.delete('1.0', END)
        self.seven_segs_L.insert(END, self.states["seg_L"].state)
        self.seven_segs_R.delete('1.0', END)
        self.seven_segs_R.insert(END, self.states["seg_R"].state)

        self.dial_L.delete('1.0', END)
        self.dial_L.insert(END, self.states["dial_L"].state)
        self.dial_R.delete('1.0', END)
        self.dial_R.insert(END, self.states["dial_R"].state)

        self.poten_L['text'] = self.states["pot_L"].state
        self.poten_R['text'] = self.states["pot_R"].state

        """TODO: BUTTON %% LED"""
        


    """====================== States ======================"""
    def init_state(self):
        """ Contain all states:

        {seg_L, seg_R, dial_L, dial R, pot_L, pot_R pos_2L, pos_2R, pos_1L, pos_1R, 
        led_1L, led_2L, led_3L, led_4L, led_1R, led_2R, led_3R, led_4R
        but_1L, but_2L, but_3L, but_4L, but_1R, but_2R, but_3R, but_4R}

        states = {hardware_name:(board_type, board_num, board_addr, state)}"""

        self.states = {"seg_L":UDP.UDP_packet(0,0,0), "seg_R":UDP.UDP_packet(0,0,0), \
                       "dial_L":UDP.UDP_packet(0,0,0), "dial_R":UDP.UDP_packet(0,0,0), \
                       "pot_L":UDP.UDP_packet(0,0,0), "pot_R":UDP.UDP_packet(0,0,0), \
                       "pos_2L":UDP.UDP_packet(0,0,0), "pos_2R":UDP.UDP_packet(0,0,0), \
                       "pos_1L":UDP.UDP_packet(0,0,0), "pos_1R":UDP.UDP_packet(0,0,0),\
                       "led_1L":UDP.UDP_packet(0,0,0), "led_2L":UDP.UDP_packet(0,0,0), "led_3L":UDP.UDP_packet(0,0,0), "led_4L":UDP.UDP_packet(0,0,0), \
                       "led_1R":UDP.UDP_packet(0,0,0), "led_2R":UDP.UDP_packet(0,0,0), "led_3R":UDP.UDP_packet(0,0,0), "led_4R":UDP.UDP_packet(0,0,0), \
                       "but_1L":UDP.UDP_packet(0,0,0), "but_1L":UDP.UDP_packet(0,0,0), "but_1L":UDP.UDP_packet(0,0,0), "but_1L":UDP.UDP_packet(0,0,0), \
                       "but_1R":UDP.UDP_packet(0,0,0), "but_1R":UDP.UDP_packet(0,0,0), "but_1R":UDP.UDP_packet(0,0,0), "but_1R":UDP.UDP_packet(0,0,0)}

    """====================== UDP operation ======================"""
    def reciver(self):

        while not self.thread_quit_flag:
            ready = select.select([self.sock], [], [], 0.1)
            packet_list = []
            if ready[0]:
                data, _ = self.sock.recvfrom(30)        # buffer size is 1024 bytes
                packet_list = self.decode_packet(data)  # Get packet from received data
                self.states = self.Update_states_from_GUI()
                for packet in packet_list:
                    if DEBUG_MODE:
                        self.Update_message(str(packet)+'\n')
                    self.Update_state_from_packet(packet)           # Update self.states based on packet
                self.Update_GUI()                       # Update GUI based on new self.states
        return 0


    def sender(self):

        # Check the changging state
        udp_packet_list = self.generate_packet()

        if len(udp_packet_list) != 0:  # 
            for packet in udp_packet_list:
                try:
                    self.sock.sendto(packet, (UDP.UDP_MASTER_IP, UDP.UDP_MASTER_PORT))
                    self.Update_message("UDP Sent to master!\n")
                except Exception as e:
                    self.Update_message("{0} | {1}\n".format(e.message, e.args))
                if DEBUG_MODE:
                    print(packet)


    def generate_packet(self):
        """TODO: generate new packet based on old state and new GUI"""
        # Read new state
        new_states = self.Update_states_from_GUI()  # Read from GUI to self.states
        difference_states = {}                      # Empty for whatever changed
        packet_list = []                            # Store all UDP message 

        # Compate with old state
        for component in self.states.keys():
            print(component, type(self.states[component]))
            if self.states[component].state != new_states[component].state:
                difference_states[component].state = new_states[component].state

        # Assign new state to old state
        self.states = new_states

        """ TODO: Construct based on 'difference_states'"""
        for key, value in difference_states.items():
            break

        return packet_list


    def decode_packet(self, data):
        packet_list = []
        index = 1

        # decode what we got into packet.
        for index in range(len(data)):
            data_slices = data[index*3:index*3+3]
            if data_slices != b'' and data_slices != b"\x00\x00\x00":
                packet = UDP.UDP_packet(data_slices[0], data_slices[1], data_slices[2])
                packet_list.append(packet)
        return packet_list


if __name__=="__main__":
    sock = UDP.init_UDP_connection(LOCAL_MODE)
    window = Tk()
    Simulator_GUI(window, sock)