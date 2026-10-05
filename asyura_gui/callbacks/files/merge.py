from ...callback_runtime import *

def mergefile(env):
    i = env.get('i')
    state = env.get('state')
    # 試しにファイルをマージする機能を作成してみたがいまいち。まぁファイル整理はしやすいかな
    # 最初に選んだファイルのディレクトリを取得
    base_dir = os.path.dirname(state['file_paths'][0])

    mf_path = tk.filedialog.asksaveasfilename(
    title = "save as foreground merge data",
    #initialdir = "./", # 自分自身のディレクトリ
    initialdir=base_dir,# 1番目のファイルのディレクトリ
    defaultextension=".dat", filetypes=[("DAT files", "*.dat")])

    for i in range(len(state['file_paths'])):
        #リストにあるファイルを順に読み込んでいく
        with open(state['file_paths'][i],"r", encoding="utf-8") as f:
            # ファイルの特定の行を読み込み、どのパラメータがどの列かを調べる。
            line = f.readlines()
            data = line[31]
            data2 = data.split()

            if "Pt." in data2:
                pass
            else:
                data = line[32]
                data2 = data.split()

            #パラメータは何番目ですか？
            No_Pt=data2.index('Pt.')
            No_c2=data2.index('c2')
            No_a2=data2.index('a2')
            No_timeact=data2.index('time-act')
            #mcuがない場合は読み込まない。もちろんデータも表示されないけどね
            if data.find('mcu')!=-1:
                No_mcu=data2.index('mcu')
            else :
                pass
            No_q=data2.index('q')
            No_h=data2.index('h')
            No_k=data2.index('k')
            No_l=data2.index('l')
            No_T=data2.index('tsample')
            No_e=data2.index('e')
            No_ei=data2.index('ei')
            No_D01=data2.index('D01')
            No_D24=data2.index('D24')
            #選択ファイルの数値を全て読み込む
            rdb = np.loadtxt(state['file_paths'][i], comments='#')
            # データが１次元配列の際に２次元配列に格納
            if len(rdb.shape) == 1:
                rdb = np.expand_dims(rdb, axis=0)
            # 最終的に読み込むのはtime-act,mcu,c2,a2,e,ei,detectorだけだから
            t_a = rdb[:,No_timeact-1].reshape(-1, 1)

            pt = rdb[:,No_Pt-1].reshape(-1, 1)
            c2 = rdb[:,No_c2-1].reshape(-1, 1)
            a2 = rdb[:,No_a2-1].reshape(-1, 1)
            q = rdb[:,No_q-1].reshape(-1, 1)
            h = rdb[:,No_h-1].reshape(-1, 1)
            k = rdb[:,No_k-1].reshape(-1, 1)
            l = rdb[:,No_l-1].reshape(-1, 1)
            T = rdb[:,No_T-1].reshape(-1, 1)
            #mcuがない場合は読み込まない。強制的にmcuが0となり、IntensityはNan値となる。
            if data.find('mcu')!=-1:
                mcu = rdb[:,No_mcu-1].reshape(-1, 1)
            else :
                mcu = np.zeros((len(pt))).reshape(-1, 1)
            e = rdb[:,No_e-1].reshape(-1, 1)
            ei = rdb[:,No_ei-1].reshape(-1, 1)
            D = rdb[:,No_D01-1:No_D24]

            new_rdb = np.hstack((pt,t_a,mcu,D,a2,c2,ei,e,q,h,k,l,T))

            # time-actが0のデータを検索。基本的にファイルの最後の行が0になる。
            if new_rdb[-1,1] == 0:
                new_rdb = np.delete(new_rdb, -1, axis=0)

            if i == 0:
                NEW_rdb=new_rdb
            #databox.extend(Qvector)
            if i > 0:
                NEW_rdb=(np.vstack([NEW_rdb, new_rdb]))

    # 最初のinformationの情報を付け足す。
    with open(state['file_paths'][0],"r", encoding="utf-8") as f:
        # ファイルの特定の行を読み込み、どのパラメータがどの列かを調べる。
        line = f.readlines()
        data = line[31]
        data2 = data.split()            
        if "Pt." in data2:
            lines = line[0:31]
        else:
            lines = line[0:32]
        # headerの作成 
        header = ["Pt. time-act mcu D01 D02 D03 D04 D05 D06 D07 D08 D09 D10 D11 D12 D13 D14 D15 D16 D17 D18 D19 D20 D21 D22 D23 D24 a2 c2 ei e q h k l tsample"]
        with open(mf_path, "w") as f1:
            f1.writelines(lines)
            f1.write(f"# {', '.join(header)}\n")
            # データを文字列に変換して書き込む
            for row in NEW_rdb:
                row_str = ' '.join(map(str, row))
                f1.write(row_str + '\n')            

def mergefile_sb(env):
    i = env.get('i')
    state = env.get('state')
    # 試しにファイルをマージする機能を作成してみたがいまいち。まぁファイル整理はしやすいかな
    # 最初に選んだファイルのディレクトリを取得
    base_dir = os.path.dirname(state['sbfile_paths'][0])

    mf_path = tk.filedialog.asksaveasfilename(
    title = "save as ground merge data",
    #initialdir = "./", # 自分自身のディレクトリ
    initialdir=base_dir,# 1番目のファイルのディレクトリ
    defaultextension=".dat", filetypes=[("DAT files", "*.dat")])

    for i in range(len(state['sbfile_paths'])):
        #リストにあるファイルを順に読み込んでいく
        with open(state['sbfile_paths'][i],"r", encoding="utf-8") as f:
            # ファイルの特定の行を読み込み、どのパラメータがどの列かを調べる。
            line = f.readlines()
            data = line[31]
            data2 = data.split()

            if "Pt." in data2:
                pass
            else:
                data = line[32]
                data2 = data.split()

            #パラメータは何番目ですか？
            sbNo_Pt=data2.index('Pt.')
            sbNo_c2=data2.index('c2')
            sbNo_a2=data2.index('a2')
            sbNo_q=data2.index('q')
            sbNo_h=data2.index('h')
            sbNo_k=data2.index('k')
            sbNo_l=data2.index('l')
            sbNo_T=data2.index('tsample')
            sbNo_timeact=data2.index('time-act')
            #mcuがない場合は読み込まない。もちろんデータも表示されないけどね
            if data.find('mcu')!=-1:
                sbNo_mcu=data2.index('mcu')
            else :
                pass
            sbNo_e=data2.index('e')
            sbNo_ei=data2.index('ei')
            sbNo_D01=data2.index('D01')
            sbNo_D24=data2.index('D24')

            #選択ファイルの数値を全て読み込む
            sbrdb = np.loadtxt(state['sbfile_paths'][i], comments='#')
            # データが１次元配列の際に２次元配列に格納
            if len(sbrdb.shape) == 1:
                sbrdb = np.expand_dims(sbrdb, axis=0)
            # 最終的に読み込むのはtime-act,mcu,c2,a2,e,ei,detectorだけだから
            t_a = sbrdb[:,sbNo_timeact-1].reshape(-1, 1)
            """
            # time-actが0のデータを検索
            Ind_t0 = np.where(t_a == 0)
            # time-actが0のデータを削除
            sbrdb = np.delete(sbrdb, Ind_t0, axis=0)
            """

            pt = sbrdb[:,sbNo_Pt-1].reshape(-1, 1)
            c2 = sbrdb[:,sbNo_c2-1].reshape(-1, 1)
            a2 = sbrdb[:,sbNo_a2-1].reshape(-1, 1)
            q = sbrdb[:,sbNo_q-1].reshape(-1, 1)
            h = sbrdb[:,sbNo_h-1].reshape(-1, 1)
            k = sbrdb[:,sbNo_k-1].reshape(-1, 1)
            l = sbrdb[:,sbNo_l-1].reshape(-1, 1)
            T = sbrdb[:,sbNo_T-1].reshape(-1, 1)
            #mcuがない場合は読み込まない。強制的にmcuが0となり、IntensityはNan値となる。
            if data.find('mcu')!=-1:
                mcu = sbrdb[:,sbNo_mcu-1].reshape(-1, 1)
            else :
                mcu = np.zeros((len(pt))).reshape(-1, 1)
            e = sbrdb[:,sbNo_e-1].reshape(-1, 1)
            ei = sbrdb[:,sbNo_ei-1].reshape(-1, 1)
            D = sbrdb[:,sbNo_D01-1:sbNo_D24]

            new_sbrdb = np.hstack((pt,t_a,mcu,D,a2,c2,ei,e,q,h,k,l,T))

            # time-actが0のデータを検索。基本的にファイルの最後の行が0になる。
            if new_sbrdb[-1,1] == 0:
                new_sbrdb = np.delete(new_sbrdb, -1, axis=0)

            if i == 0:
                NEW_sbrdb=new_sbrdb
            #databox.extend(Qvector)
            if i > 0:
                NEW_sbrdb=(np.vstack([NEW_sbrdb, new_sbrdb]))

    # 最初のinformationの情報を付け足す。
    with open(state['sbfile_paths'][0],"r", encoding="utf-8") as f:
        # ファイルの特定の行を読み込み、どのパラメータがどの列かを調べる。
        line = f.readlines()
        data = line[31]
        data2 = data.split()            
        if "Pt." in data2:
            lines = line[0:31]
        else:
            lines = line[0:32]
        # headerの作成 
        header = ["Pt. time-act mcu D01 D02 D03 D04 D05 D06 D07 D08 D09 D10 D11 D12 D13 D14 D15 D16 D17 D18 D19 D20 D21 D22 D23 D24 a2 c2 ei e q h k l tsample"]
        with open(mf_path, "w") as f1:
            f1.writelines(lines)
            f1.write(f"# {', '.join(header)}\n")
            # データを文字列に変換して書き込む
            for row in NEW_sbrdb:
                row_str = ' '.join(map(str, row))
                f1.write(row_str + '\n')    
