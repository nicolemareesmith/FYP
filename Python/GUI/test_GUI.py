# -*- coding: cp936 -*-

from tkinter import *
root = Tk()
#�Բ�ͬ����ɫ�������frame
for fm in ['red','blue','yellow','green','white','black']:
    #ע���������Frame�ķ��������������ؼ��ķ�����ͬ����һ����������root
    Frame(height = 20,width = 400,bg = fm).pack()
root.mainloop()
#��Ӳ�ͬ��ɫ��Frame����С��Ϊ20*400
'''2.��Frame�����Widget'''
# -*- coding: cp936 -*-
from Tkinter import *
root = Tk()
fm = []
#�Բ�ͬ����ɫ�������frame
for color in ['red','blue']:
    #ע���������Frame�ķ��������������ؼ��ķ�����ͬ����һ����������root
    fm.append(Frame(height = 200,width = 400,bg = color))
#�������Frame�����һ��Label
Label(fm[1],text = 'Hello label').pack()
fm[0].pack()
fm[1].pack()
root.mainloop()
#Label����ӵ������Frame���ˣ�������rootĬ�ϵ����Ϸ���
#�󲿷ֵķ�������gm,��������gmʱ�ٽ���
'''3.Tk8.4�Ժ�Frame�������һ��LabelFrame�������Title��֧��'''
from Tkinter import *
root = Tk()
for lf in ['red','blue','yellow']:
    #����ʹ��text����ָ��Frame��title
    LabelFrame(height = 200,width = 300,text = lf).pack()
root.mainloop()