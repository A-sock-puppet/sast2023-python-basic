import tkinter as tk
from tkinter import messagebox
import argparse
import json
import os
from random import choice
from main import select_article, replace

def get_inputs(hints):
    keys = []
    global labels, entries
    labels, entries = [None]*len(hints), [None]*len(hints)
    for i, hint in enumerate(hints):
        labels[i] = tk.Label(root, text=f"{hint}:")
        labels[i].grid(row=4+i, column=0, padx=5, pady=5)
        entry_value = tk.StringVar()
        entries[i] = tk.Entry(root, textvariable=entry_value)
        entries[i].grid(row=4+i, column=1, padx=5, pady=5)
        keys.append(entry_value)
    return keys

def show_result(article, keys):
    inputs = [entry.get() for entry in keys]
    article_replaced = replace(article['article'], inputs)
    messagebox.showinfo("最终的文章", article_replaced)
    show_result_button.destroy()
    for i in range(len(entries)):
        labels[i].destroy()
        entries[i].destroy()
    submit_button.config(state=tk.ACTIVE)
    file_entry.config(state=tk.NORMAL)
    language_option_menu.config(state=tk.ACTIVE)
    article_entry.config(state=tk.NORMAL)

def submit_answers():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, file_entry.get())

    args = {
        "file": file_path,
        "lang": language_var.get(),
        "uid": int(article_var.get())
    }

    if not os.path.isfile(args['file']):
        messagebox.showerror("File Not Found", "The specified file does not exist.")
        return
    
    language, uid = args['lang'], args['uid']
    if language == '中文': language = 'zh'
    if language == 'English': language = 'en'
    articles = [article for article_group in main_data for article in article_group['articles'] 
                if article_group['language'] == language]
    
    if args["uid"] not in range(len(articles)):
        messagebox.showerror("Index out of Range", f"Available index range: 0 - {len(articles)-1}.")
        return

    article = select_article(args, main_data)
    keys = get_inputs(article['hints'])
    
    file_entry.config(state=tk.DISABLED)
    language_option_menu.config(state=tk.DISABLED)
    article_entry.config(state=tk.DISABLED)
    submit_button.config(state=tk.DISABLED)
    global show_result_button
    show_result_button = tk.Button(root, text="查看结果", command=lambda: show_result(article, keys))
    show_result_button.grid(row=len(article['hints'])+5, columnspan=2, padx=5, pady=10)


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--args', type=json.loads, help='JSON-formatted args from main.py')
    parser.add_argument('--data', type=json.loads, help='JSON-formatted data from main.py')
    args = parser.parse_args()

    if args.args and args.data:
        main_args, main_data = argparse.Namespace(**args.args), args.data

    root = tk.Tk()
    root.title("Word Filling Game")

    file_var = tk.StringVar(value=main_args.file)
    file_label = tk.Label(root, text="题库相对路径：")
    file_label.grid(row=0, column=0, padx=5, pady=5)
    file_entry = tk.Entry(root, textvariable=file_var)
    file_entry.grid(row=0, column=1, padx=5, pady=5)

    if main_args.lang == 'en': main_args.lang = 'English'
    else: main_args.lang = '中文'
    language_var = tk.StringVar(value=main_args.lang)
    language_label = tk.Label(root, text="选择语言：")
    language_label.grid(row=1, column=0, padx=5, pady=5)
    language_option_menu = tk.OptionMenu(root, language_var, '中文', 'English')
    language_option_menu.grid(row=1, column=1, padx=5, pady=5)

    article_var = tk.StringVar(value=main_args.uid)
    article_label = tk.Label(root, text=f"文章序号：")
    article_label.grid(row=2, column=0, padx=5, pady=5)
    article_entry = tk.Entry(root, textvariable=article_var)
    article_entry.grid(row=2, column=1, padx=5, pady=5)

    submit_button = tk.Button(root, text="提交", command=submit_answers)
    submit_button.grid(row=3, column=0, padx=(80, 0), pady=10)

    exit_button = tk.Button(root, text="退出", command=root.destroy)
    exit_button.grid(row=3, column=1, padx=(0, 40), pady=10)

    root.mainloop()
