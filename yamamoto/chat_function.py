import tkinter as tk

# ボタンが押されたらリストボックスに、Entryの中身を追加
def addList(text, listbox, entry):
    mysay = 'you: ' + text
    print(mysay)
    listbox.insert(tk.END, mysay)
    Seri = 'Seri: ' + talk(text)
    entry.delete(0, tk.END)
    addRep(Seri)

def addRep(Seri):
    listbox.insert(tk.END, Seri)

def talk(say):
    if say == 'end':
        return('ではまた')
    else:
        response = model.generate_content(say)
        assistant_response = response.text
        return(assistant_response)