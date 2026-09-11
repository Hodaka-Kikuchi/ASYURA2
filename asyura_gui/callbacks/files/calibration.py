from ...callback_runtime import *

def calibration(env):
    i = env.get('i')
    state = env.get('state')
    with open(state['vfile_path'][0],"r", encoding="utf-8") as f:
        line = f.readlines()
        head = line[31]
        head2 = head.split()
        if "Pt." in head2:
            pass
        else:
            head = line[32]
            head2 = head.split()

        #パラメータは何番目ですか？
        #global No_Pt,No_c2,No_a2,No_mcu,No_e,No_ei,No_D01,No_D02,No_D03,No_D04,No_D05,No_D06,No_D07,No_D08,No_D09,No_D10,No_D11,No_D12,No_D13,No_D14,No_D15,No_D16,No_D17,No_D18,No_D19,No_D20,No_D21,No_D22,No_D23,No_D24
        No_Pt=head2.index('Pt.')
        No_c2=head2.index('c2')
        No_a2=head2.index('a2')
        No_timeact=head2.index('time-act')
        #mcuは最初から読み込まない
        No_e=head2.index('e')
        No_ei=head2.index('ei')
        No_D01=head2.index('D01')
        No_D24=head2.index('D24')

    #リストにあるファイルを順に読み込んでいく
    with open(state['vfile_path'][0],"r", encoding="utf-8") as f:
        #選択ファイルの数値を全て読み込む
        vrdb = np.loadtxt(state['vfile_path'][0], comments='#')

    t_a = vrdb[:,No_timeact-1]
    # time-actが0のデータを検索
    Ind_t0 = np.where(t_a == 0)
    # time-actが0のデータを削除
    vrdb = np.delete(vrdb, Ind_t0, axis=0)

    pt = vrdb[:,No_Pt-1]
    c2 = vrdb[:,No_c2-1]
    a2 = vrdb[:,No_a2-1]

    e = vrdb[:,No_e-1]
    ei = vrdb[:,No_ei-1]
    D_I = vrdb[:,No_D01-1:No_D24]

    #ガウス関数fitting
    def func(x, a, mu, sigma, bg):
        return a*np.exp(-(x-mu)**2/(2*sigma**2))+bg
    #初期値
    #param_ini = [500,0,0.1,0]
    # 1つの図を作成
    fig, ax = plt.subplots(6, 4, sharex=True, sharey=True)
    #fig=plt.figure()
    fit_param = np.zeros((24,4))
    fit_result=np.zeros((3,24))
    for i in range(6):
        for j in range(4):
            """#旧コード
            index = i * 4 + j
            popt, pcov = curve_fit(func, e, D_I[:,index], p0=param_ini, maxfev=1000)
            fitting = func(e, popt[0],popt[1],popt[2],popt[3])
            fit_param[i * 4 + j,:]=[popt[0],popt[1],popt[2],popt[3]]
            #高さ popt[0]
            #中心 popt[1]
            #幅　popt[2]
            #background popt[3]
            #高さ
            #fit_result[0,i]=popt[0]#intensity
            #積分強度
            fit_result[0,i]=popt[0]*2*(2*math.log(2))**(1/2)*abs(popt[2])*(3.1415926535/(4*math.log(2)))**(1/2)#intensity
            fit_result[1,index]=popt[1]#energy transter center
            fit_result[2,index]=2*(2*math.log(2))**(1/2)*abs(popt[2])#FWHM

            ax[i, j].errorbar(e,D_I[:,index],yerr=D_I[:,index]**(1/2), capsize=10, zorder=1,color='k',label='D'+str(index+1))
            ax[i, j].text(0.05,1.05,'I='+str(format(popt[0]*2*(2*math.log(2))**(1/2)*abs(popt[2])*(3.1415926535/(4*math.log(2)))**(1/2), '.1f'))+',Ec='+str(format(popt[1], '.4f'))+',FWHM='+str(format(2*(2*math.log(2))**(1/2)*abs(popt[2]), '.4f')), transform=ax[i, j].transAxes)
            #ax[i, j].text(0.05,1.05,'I='+str(format(popt[0], '.1f'))+',Ec='+str(format(popt[1], '.4f'))+',FWHM='+str(format(2*(2*math.log(2))**(1/2)*abs(popt[2]), '.4f')), transform=ax[i, j].transAxes)
            ax[i, j].plot(e,fitting,'r', zorder=2)
            #ax.set_xlabel('e (meV)')
            #ax.set_ylabel('Intensity (a.u.)')
            ax[i, j].legend()
            """
            index = i * 4 + j
            ydata = D_I[:, index]
            xdata = e

            # ---- 初期値をデータに基づいて設定 ----
            a_init = np.max(ydata)
            mu_init = xdata[np.argmax(ydata)]
            sigma_init = 0.1
            bg_init = np.min(ydata)
            param_ini = [a_init, mu_init, sigma_init, bg_init]

            # ---- フィッティング ----
            popt, pcov = curve_fit(func, xdata, ydata, p0=param_ini, maxfev=1000)
            fitting = func(xdata, *popt)

            # 結果保存
            fit_param[index, :] = popt
            fit_result[0, index] = popt[0] * 2 * (2 * math.log(2))**0.5 * abs(popt[2]) * (math.pi / (4 * math.log(2)))**0.5
            fit_result[1, index] = popt[1]
            fit_result[2, index] = 2 * (2 * math.log(2))**0.5 * abs(popt[2])

            # ---- プロット ----
            ax[i, j].errorbar(xdata, ydata, yerr=np.sqrt(ydata), capsize=10, zorder=1, color='k', label='D'+str(index+1))
            ax[i, j].text(0.05, 1.05,
                        f"Area={fit_result[0, index]:.1f}, Ec={popt[1]:.4f}, FWHM={fit_result[2, index]:.4f}",
                        transform=ax[i, j].transAxes)
            ax[i, j].plot(xdata, fitting, 'r', zorder=2)
            ax[i, j].legend()

    fig.supxlabel('ℏω (meV)')
    fig.supylabel('Intensity (a.u.)')
    plt.tight_layout()
    plt.show()
