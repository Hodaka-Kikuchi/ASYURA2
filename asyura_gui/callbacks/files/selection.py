from ...callback_runtime import *

def file_select(env):
    Listbox = env.get('Listbox')
    state = env.get('state')
    #idir = 'C:\\python_test'
    filetypes = [("dat file","*.dat")]
    # shared variables are stored in state
    state['file_paths'] += tk.filedialog.askopenfilenames(filetypes=filetypes, multiple=True)
    flnmlst = [os.path.basename(item) for item in state['file_paths']]
    # shared variables are stored in state
    # filstを重複を許す場合
    #flist = list(flnmlst)
    # flistを重複を許さずかつ順番を保持する場合。setコマンドでは順序が無茶苦茶になる。
    state['flist'] = list(dict.fromkeys(flnmlst))
    Listbox.delete(0, tk.END)  # リストボックスの内容をクリア
    for item in state['flist']:
        Listbox.insert(tk.END, item)  # リストボックスにファイル名を追加

def clear(env):
    Listbox = env.get('Listbox')
    state = env.get('state')
    Listbox.delete(0,tk.END)
    state['file_paths'].clear()

def vfile_select(env):
    state = env.get('state')
    vListbox = env.get('vListbox')
    vListbox.delete(0, tk.END)
    #idir = 'C:\\python_test'
    filetypes=[("dat file", "*.dat")]
    # shared variables are stored in state
    state['vfile_path'] = tk.filedialog.askopenfilenames(filetypes = filetypes,multiple = False)
    vflnmlst = [os.path.basename(item) for item in state['vfile_path']]
    #basename = os.path.basename(file_list)
    #input_box.insert(tk.END, flnmlst)
    #ファイル名をリスト化
    # listbox = tk.Listbox(root, flnmlst)
    vflist=list(vflnmlst)
    # Listboxの選択肢
    vListbox.insert(tk.END, vflist)

def vclear(env):
    vListbox = env.get('vListbox')
    vListbox.delete(0,tk.END)
    vfile_path=[]

def sbfile_select(env):
    sbListbox = env.get('sbListbox')
    state = env.get('state')
    #idir = 'C:\\python_test'
    filetypes = [("dat file","*.dat")]
    # shared variables are stored in state
    state['sbfile_paths'] += tk.filedialog.askopenfilenames(filetypes=filetypes, multiple=True)
    sbflnmlst = [os.path.basename(item) for item in state['sbfile_paths']]
    # shared variables are stored in state
    # sbfilstを重複を許す場合
    #sblists = list(sbflnmlst)
    # sbflistを重複を許さずかつ順番を保持する場合。setコマンドでは順序が無茶苦茶になる。
    state['sblists'] = list(dict.fromkeys(sbflnmlst))
    sbListbox.delete(0, tk.END)  # リストボックスの内容をクリア
    for item in state['sblists']:
        sbListbox.insert(tk.END, item)  # リストボックスにファイル名を追加

def sbclear(env):
    sbListbox = env.get('sbListbox')
    state = env.get('state')
    sbListbox.delete(0,tk.END)
    state['sbfile_paths'].clear()
