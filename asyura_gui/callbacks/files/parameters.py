from ...callback_runtime import *

def save_param(env):
    csv = env.get('csv')
    txt1 = env.get('txt1')
    txt10 = env.get('txt10')
    txt11 = env.get('txt11')
    txt12 = env.get('txt12')
    txt13 = env.get('txt13')
    txt14 = env.get('txt14')
    txt15 = env.get('txt15')
    txt2 = env.get('txt2')
    txt3 = env.get('txt3')
    txt4 = env.get('txt4')
    txt5 = env.get('txt5')
    txt6 = env.get('txt6')
    txt9 = env.get('txt9')
    txt_ref_a2 = env.get('txt_ref_a2')
    txt_ref_c2 = env.get('txt_ref_c2')
    txt_ref_ef = env.get('txt_ref_ef')
    txt_ref_ei = env.get('txt_ref_ei')
    txt_ref_h = env.get('txt_ref_h')
    txt_ref_k = env.get('txt_ref_k')
    txt_ref_l = env.get('txt_ref_l')
    txt_ref_rx = env.get('txt_ref_rx')
    txt_ref_ry = env.get('txt_ref_ry')
    txt_ul = env.get('txt_ul')
    txt_vl = env.get('txt_vl')

    # ========================= 
    # GUIから値を取得 
    # ========================= 

    la = float(txt1.get()) 
    lb = float(txt2.get()) 
    lc = float(txt3.get()) 

    lal = float(txt4.get()) 
    lbe = float(txt5.get()) 
    lga = float(txt6.get()) 

    N_mcu = float(txt15.get()) 

    # scattering plane U 
    u1 = float(txt9.get()) 
    u2 = float(txt10.get()) 
    u3 = float(txt11.get()) 
    u_l = txt_ul.get() 

    # scattering plane V 
    v1 = float(txt12.get()) 
    v2 = float(txt13.get()) 
    v3 = float(txt14.get()) 
    v_l = txt_vl.get() 

    # ========================= 
    # Reference peak 
    # ========================= 

    ref_h = float(txt_ref_h.get()) 
    ref_k = float(txt_ref_k.get()) 
    ref_l = float(txt_ref_l.get()) 
    ref_c2 = float(txt_ref_c2.get()) 
    ref_a2 = float(txt_ref_a2.get()) 
    ref_ry = float(txt_ref_ry.get()) 
    ref_rx = float(txt_ref_rx.get()) 
    ref_ei = float(txt_ref_ei.get()) 
    ref_ef = float(txt_ref_ef.get()) 

    # ========================= 
    # 保存するパラメータ 
    # ========================= 

    param = [ 
        la,       # 0 
        lb,       # 1 
        lc,       # 2 
        lal,      # 3 
        lbe,      # 4 
        lga,      # 5 
        N_mcu,    # 6 

        u1,       # 7 
        u2,       # 8 
        u3,       # 9 
        u_l,      # 10 

        v1,       # 11 
        v2,       # 12 
        v3,       # 13 
        v_l,      # 14 

        ref_h,    # 15 
        ref_k,    # 16 
        ref_l,    # 17 
        ref_c2,   # 18 
        ref_a2,   # 19
        ref_rx,   # 20  
        ref_ry,   # 21 
        ref_ei,   # 22 
        ref_ef,   # 23 
    ] 

    # ========================= 
    # 保存先 
    # ========================= 

    filename = tk.filedialog.asksaveasfilename( 
        title="save as parameter file", 
        filetypes=[ 
            ("CSV", "*.csv") 
        ], 
        initialdir="./", 
        defaultextension=".csv", 
    ) 

    # キャンセルされた場合 
    if not filename: 
        return 

    # ========================= 
    # CSVへ保存 
    # ========================= 

    with open( 
        filename, 
        "w", 
        newline="", 
        encoding="utf-8" 
    ) as csvfile: 

        writer = csv.writer(csvfile) 
        writer.writerow(param)

def initialize_param(env):
    state = env.get('state')
    txt1 = env.get('txt1')
    txt10 = env.get('txt10')
    txt11 = env.get('txt11')
    txt12 = env.get('txt12')
    txt13 = env.get('txt13')
    txt14 = env.get('txt14')
    txt2 = env.get('txt2')
    txt3 = env.get('txt3')
    txt4 = env.get('txt4')
    txt5 = env.get('txt5')
    txt6 = env.get('txt6')
    txt9 = env.get('txt9')
    txt_ref_a2 = env.get('txt_ref_a2')
    txt_ref_c2 = env.get('txt_ref_c2')
    txt_ref_ef = env.get('txt_ref_ef')
    txt_ref_ei = env.get('txt_ref_ei')
    txt_ref_h = env.get('txt_ref_h')
    txt_ref_k = env.get('txt_ref_k')
    txt_ref_l = env.get('txt_ref_l')
    txt_ref_rx = env.get('txt_ref_rx')
    txt_ref_ry = env.get('txt_ref_ry')

    # ===================================================== 
    # SPICE .ini ファイルを選択 
    # ===================================================== 

    ini_path = filedialog.askopenfilename( 
        title="SPICE ini file を選択", 
        filetypes=[ 
            ("INI files", "*.ini"), 
            ("All files", "*.*"), 
        ], 
    ) 

    # キャンセルされた場合 
    if not ini_path: 
        return 

    # ===================================================== 
    # ini ファイルを読み込む 
    # ===================================================== 

    config = configparser.ConfigParser() 

    config.read( 
        ini_path, 
        encoding="utf-8", 
    ) 

    # ===================================================== 
    # Lattice parameters 
    # 
    # a, b, c, alpha, beta, gamma 
    # ===================================================== 

    lattice_str = config["Data"]["LatticeParams"] 

    # "..." が付いていても除去 
    lattice_str = lattice_str.strip('"') 

    lattice = [ 
        float(x) 
        for x in lattice_str.split(",") 
    ] 

    if len(lattice) != 6: 
        raise ValueError( 
            "LatticeParams must contain " 
            "a,b,c,alpha,beta,gamma" 
        ) 

    a, b, c, alpha, beta, gamma = lattice 

    # ===================================================== 
    # Peak1
    #
    # h, k, l, a2, c2, mu, nu, ei, ef
    # ===================================================== 

    peak1_str = config["Data"]["Peak1"] 
    peak1_str = peak1_str.strip('"') 

    peak1 = [ 
        float(x) 
        for x in peak1_str.split(",") 
    ] 

    if len(peak1) < 9: 
        raise ValueError( 
            "Peak1 must contain "
            "h,k,l,a2,c2,mu,nu,ei,ef."
        ) 

    ref_h  = peak1[0] 
    ref_k  = peak1[1] 
    ref_l  = peak1[2] 
    ref_a2 = peak1[3] 
    ref_c2 = peak1[4] 
    ref_rx = peak1[5] 
    ref_ry = peak1[6] 
    ref_ei = peak1[7] 
    ref_ef = peak1[8] 

    # ===================================================== 
    # GUIへ反映 
    # ===================================================== 

    def set_entry(entry, value): 
        entry.delete(0, tk.END) 
        entry.insert(0, str(value)) 

    # lattice parameters 
    set_entry(txt1, a) 
    set_entry(txt2, b) 
    set_entry(txt3, c) 
    set_entry(txt4, alpha) 
    set_entry(txt5, beta) 
    set_entry(txt6, gamma) 

    # reference peak 
    set_entry(txt_ref_h, ref_h) 
    set_entry(txt_ref_k, ref_k) 
    set_entry(txt_ref_l, ref_l) 
    set_entry(txt_ref_c2, ref_c2) 
    set_entry(txt_ref_a2, ref_a2) 
    set_entry(txt_ref_ry, ref_ry) 
    set_entry(txt_ref_rx, ref_rx) 
    set_entry(txt_ref_ei, ref_ei) 
    set_entry(txt_ref_ef, ref_ef)

    #散乱面１の読み込み 
    with open(state['file_paths'][0],"r", encoding="utf-8") as f: 
        sv1 = f.readlines()[15] 
        SV1 = sv1.split() 

    #散乱面２の読み込み 
    with open(state['file_paths'][0],"r", encoding="utf-8") as f: 
        sv2 = f.readlines()[16] 
        SV2 = sv2.split() 

    txt9.delete(0,tk.END) 
    txt9.insert(0,SV1[5]) 
    txt10.delete(0,tk.END) 
    txt10.insert(0,SV1[6]) 
    txt11.delete(0,tk.END) 
    txt11.insert(0,SV1[7]) 

    txt12.delete(0,tk.END) 
    txt12.insert(0,SV2[5]) 
    txt13.delete(0,tk.END) 
    txt13.insert(0,SV2[6]) 
    txt14.delete(0,tk.END) 
    txt14.insert(0,SV2[7]) 

def load_param(env):
    csv = env.get('csv')
    txt1 = env.get('txt1')
    txt10 = env.get('txt10')
    txt11 = env.get('txt11')
    txt12 = env.get('txt12')
    txt13 = env.get('txt13')
    txt14 = env.get('txt14')
    txt15 = env.get('txt15')
    txt2 = env.get('txt2')
    txt3 = env.get('txt3')
    txt4 = env.get('txt4')
    txt5 = env.get('txt5')
    txt6 = env.get('txt6')
    txt9 = env.get('txt9')
    txt_ref_a2 = env.get('txt_ref_a2')
    txt_ref_c2 = env.get('txt_ref_c2')
    txt_ref_ef = env.get('txt_ref_ef')
    txt_ref_ei = env.get('txt_ref_ei')
    txt_ref_h = env.get('txt_ref_h')
    txt_ref_k = env.get('txt_ref_k')
    txt_ref_l = env.get('txt_ref_l')
    txt_ref_rx = env.get('txt_ref_rx')
    txt_ref_ry = env.get('txt_ref_ry')
    txt_ul = env.get('txt_ul')
    txt_vl = env.get('txt_vl')

    filetypes = [ 
        ("CSV file", "*.csv") 
    ] 

    pfile_path = tk.filedialog.askopenfilename( 
        title="load parameter file", 
        filetypes=filetypes, 
    ) 

    if not pfile_path: 
        return 

    with open( 
        pfile_path, 
        newline="", 
        encoding="utf-8" 
    ) as f: 

        csvreader = csv.reader(f) 
        row = next(csvreader, None) 

    if row is None: 
        raise ValueError( 
            "Parameter file is empty." 
        ) 

    def set_entry(entry, value): 
        entry.delete(0, tk.END) 
        entry.insert(0, str(value)) 

    # =========================
    # lattice
    # =========================

    set_entry(txt1, row[0]) 
    set_entry(txt2, row[1]) 
    set_entry(txt3, row[2]) 
    set_entry(txt4, row[3]) 
    set_entry(txt5, row[4]) 
    set_entry(txt6, row[5]) 

    # =========================
    # mcu
    # =========================

    set_entry(txt15, row[6]) 

    # =========================
    # scattering plane U
    # =========================

    set_entry(txt9, row[7]) 
    set_entry(txt10, row[8]) 
    set_entry(txt11, row[9]) 
    set_entry(txt_ul, row[10]) 

    # =========================
    # scattering plane V
    # =========================

    set_entry(txt12, row[11]) 
    set_entry(txt13, row[12]) 
    set_entry(txt14, row[13]) 
    set_entry(txt_vl, row[14]) 

    # =========================
    # Reference peak
    #
    # row[15] ref_h
    # row[16] ref_k
    # row[17] ref_l
    # row[18] ref_c2
    # row[19] ref_a2
    # row[20] ref_ry
    # row[21] ref_rx
    # row[22] ref_ei
    # row[23] ref_ef
    # =========================

    set_entry(txt_ref_h, row[15]) 
    set_entry(txt_ref_k, row[16]) 
    set_entry(txt_ref_l, row[17]) 
    set_entry(txt_ref_c2, row[18]) 
    set_entry(txt_ref_a2, row[19])
    set_entry(txt_ref_rx, row[20])
    set_entry(txt_ref_ry, row[21])
    set_entry(txt_ref_ei, row[22])
    set_entry(txt_ref_ef, row[23])
