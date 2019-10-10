dword_6020C0=[0x24, 0, 5, 0x36, 0x65, 7, 0x27, 0x26, 0x2D, 1, 3, 0, 0x0D,0x56, 1, 3, 0x65, 3, 0x2D, 0x16, 2, 0x15, 3, 0x65, 0, 0x29,0x44,0x44, 1, 0x44, 0x2B]
off_6020A0='L3t_ME_T3ll_Y0u_S0m3th1ng_1mp0rtant_A_{FL4G}_W0nt_b3_3X4ctly_th4t_345y_t0_c4ptur3_H0wev3r_1T_w1ll_b3_C00l_1F_Y0u_g0t_1t'
s=''
for i in range(len(dword_6020C0)):
    s += off_6020A0[dword_6020C0[i]]
print(len(dword_6020C0))
print(s)
