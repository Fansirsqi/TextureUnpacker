import sys,os
import tkinter
import tkinter.messagebox
import tkinter.filedialog
import unscript as unpack
from TkinterDnD2 import *
from PIL import Image, ImageTk


def do_unpack(file_path):
    resault = unpack.gen_image(file_path)
    return unpack.get_frames_name(file_path), resault


def get_resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


def drop(event):
    entry_sv.set(event.data)


def tps(sth):
    tkinter.messagebox.showinfo("", sth)


def about():
    entry.grid_remove()
    ex_btn.grid_remove()
    conlose.grid_remove()
    auth_img.grid(row=0, column=2, columnspan=6, padx=70, pady=20)
    back_btn.grid(row=1, column=4, columnspan=2)
    tkinter.messagebox.showinfo("", "Made_BY 依旧归七")


def back():
    entry.grid()
    ex_btn.grid()
    conlose.grid()
    auth_img.grid_remove()
    back_btn.grid_remove()


def back_main_adk():
    entry.grid()
    ex_btn.grid()
    conlose.grid()
    auth_img.grid_remove()
    back_btn.grid_remove()
    askfile()


def add_menu(name, func_name):  # 添加菜单，以及菜单实现的函数名称
    main_menu.add_command(label=f"{name}", command=func_name)


def askfile():
    # 从本地选择一个文件，并返回文件的目录
    filename = tkinter.filedialog.askopenfilename()
    if filename != '':
        entry_sv.set(filename)
    else:
        entry_sv.set('您没有选择任何Plist文件')
    return filename


def outputs(code):
    conlose.insert(tkinter.INSERT, code)


def get_path():  # sourcery skip: assign-if-exp
    if entry_sv.get() == '':
        return tps('请填入正确路径!')
    else:
        return str(entry_sv.get()).split(".")[0]


def click_btn():
    conlose.delete("1.0", "end")
    code, resault = do_unpack(get_path())
    if code is None:
        outputs(resault)
    else:
        outputs(code)


root = TkinterDnD.Tk()
# root.resizable(width=False, height=False)
root.iconbitmap(get_resource_path('Icon.ico'))
root.title('Sprite Cut Tool')


entry_sv = tkinter.StringVar()
# entry_sv.set('您没有选择任何Plist文件')

entry = tkinter.Entry(root, textvar=entry_sv, width=59, fg='#7c7c7c', bd=2)

entry.grid(row=0, column=2, padx=10, pady=2, ipady=7, columnspan=6)

# file_btn = tkinter.Button(
#     root, text='选择文件', relief=tkinter.RAISED,  font=('楷体', 14), command=askfile)
# file_btn.grid(row=1, column=3)


ex_btn = tkinter.Button(
    root, text='分解图片', relief=tkinter.RAISED,  font=('楷体', 14), command=click_btn)
ex_btn.grid(row=1, column=3, columnspan=2)


conlose = tkinter.Text(root, bg="#000", fg='#00ecf7',
                       font=("新宋体", 12),  width=52, height=24)
conlose.grid(row=2, column=0, columnspan=6, padx=10, pady=2)


img_open = Image.open(get_resource_path('head.png'))
img_png = ImageTk.PhotoImage(img_open)

auth_img = tkinter.Label(
    root, text="绿色", image=img_png, bg="#fff", fg='#ffffff')

back_btn = tkinter.Button(
    root, text='返回主界面', relief=tkinter.RAISED,  font=('楷体', 14), width=15, command=back)


main_menu = tkinter.Menu()
add_menu("文件", back_main_adk)
add_menu("关于", about)
root.config(menu=main_menu)

sw = root.winfo_screenwidth()
sh = root.winfo_screenheight()
rh = 440
rw = 500
rx = (sw-rw)//2
ry = (sh-rh)//2
root.geometry(f'{rh}x{rw}+{rx}+{ry}')

entry.drop_target_register(DND_FILES)
entry.dnd_bind('<<Drop>>', drop)
# tkinter.messagebox.showinfo("", "您可以拖入plist文件，请确保和png在同一目录")

root.mainloop()
