# -*- coding: utf-8 -*-
''' 
 @Author: liyi
 @Date  : 
 @Desc  :
'''

from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfpage import PDFTextExtractionNotAllowed
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.layout import *
from pdfminer.converter import PDFPageAggregator
from shutil import copyfile
from tqdm import tqdm
import tkinter
import tkinter.messagebox
import tkinter as tk
from tkinter import ttk
from tkinter import *

import threading
import argparse
import os
import pkg_resources.py2_warn

def cate(load_path, keywords, mode, save_path, category, win):

    new_win = None
    canvas = None
    fill_line = None
    if win != None:
        new_win = Toplevel(win)
        new_win.title(category+'分类进度')
        new_win.geometry('300x20')
        canvas = Canvas(new_win, width=300, height=20, bg="white")
        canvas.place(x=0, y=0)
        fill_line = canvas.create_rectangle(0, 0, 300, 20, width=0, fill="green")

    pdfs = os.listdir(load_path)
    n = 300 / len(pdfs)
    for pdf in tqdm(pdfs):
        with open(load_path + pdf, 'rb') as fp:
            parser = PDFParser(fp)
            document = PDFDocument(parser)
            if not document.is_extractable:
                raise PDFTextExtractionNotAllowed
            else:
                # 创建一个PDF资源管理器对象来存储共赏资源
                rsrcmgr = PDFResourceManager()
                # 设定参数进行分析
                laparams = LAParams()
                # 创建一个PDF设备对象
                # device=PDFDevice(rsrcmgr)
                device = PDFPageAggregator(rsrcmgr, laparams=laparams)
                # 创建一个PDF解释器对象
                interpreter = PDFPageInterpreter(rsrcmgr, device)

                flag = False

                for page in PDFPage.create_pages(document):
                    interpreter.process_page(page)
                    # # 接受该页面的LTPage对象
                    layout = device.get_result()  # return text image line curve
                    for x in layout:
                        if isinstance(x, LTText):
                            text = x.get_text()
                            isin = is_in(keywords, text, mode)
                            if isin:
                                copy(load_path, pdf, save_path, category)
                                flag = True
                                break
                    if flag:
                        break

        if new_win != None and canvas != None and fill_line != None:
            n = n + 300 / len(pdfs)
            canvas.coords(fill_line, (0, 0, n, 20))
            new_win.update()
    if new_win != None:
        new_win.destroy()


def is_in(keywords, text, mode):

    isin = False
    if mode == 'or':
        for keyword in keywords:
            if keyword in text:
                isin = True
                break

    if mode == 'and':
        for keyword in keywords:
            if keyword in text:
                isin = True
                continue
            else:
                isin = False
                break

    return isin


def copy(load_path, pdf, save_path, category):
    if os.path.exists(save_path + category):
        pass
    else:
        os.mkdir(save_path + category)
    copyfile(load_path + pdf, save_path + category + '/' + pdf)

def error(e):
    tk.messagebox.showwarning(title='error', message=e)

def main(load_path, save_path):

    win = Tk()
    win.title('pdf文档关键词分类')
    win.geometry('450x120')

    l1 = Label(win, text='关键词(以|分隔)')
    l1.grid(column=0, row=0)
    e1 = Entry(win, show=None, font=('Times New Roman', 14))
    e1.grid(column=1, row=0)

    l2 = Label(win, text='类别名称')
    l2.grid(column=0, row=1)
    e2 = Entry(win, show=None, font=('Times New Roman', 14))
    e2.grid(column=1, row=1)

    l3 = Label(win, text='分类模式')
    l3.grid(column=0, row=2)
    modes = StringVar()
    c = ttk.Combobox(win, textvariable=modes)
    c['values'] = ('or', 'and')
    c.grid(column=1, row=2)

    def hit():
        if e1.get() == '' or e2.get() == '' or c.get() == '':
            error('parameters can not be empty')
        else:
            keywords = list(e1.get().split('|'))
            category = e2.get()
            mode = c.get()
            try:
                threading.Thread(target=cate, name='new cate thread', args=[load_path, keywords, mode, save_path, category, win]).start()
            except Exception as e:
                error(e)

    b = Button(win, text='分吧!', font=('Times New Roman', 12), width=10, height=1, command=hit)
    b.grid(column=3, row=4)

    win.mainloop()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='根据关键词对pdf文档进行分类')
    parser.add_argument('--keywords',
                        type=str,
                        nargs='+',
                        help='关键词, 多个关键词以|间隔')
    parser.add_argument('--category',
                        type=str,
                        help='类别名称')
    parser.add_argument('--mode',
                        type=str,
                        default='or',
                        help='匹配关键词规则, or:匹配任意关键词, and:匹配所有关键词')
    parser.add_argument('--load_path',
                        type=str,
                        help='文档原始路径, 默认./documents',
                        default='./documents/')
    parser.add_argument('--save_path',
                        type=str,
                        help='分类文档存储路径, 默认./categories',
                        default='./categories/')
    args = parser.parse_args()

    #cate(args.load_path, args.keywords, args.mode, args.save_path, args.category, None)

    main(args.load_path, args.save_path)