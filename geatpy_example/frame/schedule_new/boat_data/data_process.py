import pandas as pd
import re
import os
from geatpy_example.frame.schedule_new.Main import main
import numpy as np

def process_data(row):
    L_W = re.split('[,，]', row)
    #     print(row,L_W)
    L, W = L_W
    return pd.Series([L, W])


def get_waitlist(path):
    data = pd.read_excel(path, header=None, sheet_name='Sheet1')
    data=data.drop_duplicates()
    df=data
    df = df.rename(columns={0: 'boat_name'})
    df[['L', 'W']] = df[1].apply(lambda x: process_data(x))
    L = df['L']
    W = df['W']
    boat_name = df['boat_name']
    ind = list(df.index)
    ind_name = {i: n for i, n in zip(ind, boat_name)}
    wait_list = [[float(l), float(w)] for l, w, in zip(L, W)]
    return wait_list,ind_name


def process_res(row):
    print(row)
    #      name_all=[]
    #      name_list=list(row.keys())

    #             name_all.extend(name_list)
    name_all = []
    for k, v in row.items():
        name_all.append(k)

        v_size_str = (str(v[1][0]), str(v[1][1]))
        vs = ','.join(v_size_str)
        name_all.append(vs)
    if len(row) < 6:
        dif_num = 2 * (6 - len(row))
        name_all.extend([''] * dif_num)
    return pd.Series(name_all)
def get_brake_boat(wait_list, L, W,ind_name):
    all_brake_boat=main(wait_list, L, W)
    all_brake_boat_new = {}
    for k, v in all_brake_boat.items():
        brake_boat = v['brake_boat']
        #     print(k,v,'\n')
        brake_boat_new = {ind_name[k0]: v0 for k0, v0 in brake_boat.items()}
        all_brake_boat_new[k] = {'brake_boat': brake_boat_new, 'best_use_rate': v['best_use_rate']}

    print('all_brake_boat_new',all_brake_boat_new)
    ##转化成需要的格式
    ind_series = all_brake_boat_new.keys()
    all_brake_boat_new_series = all_brake_boat_new.values()
    res_df = pd.DataFrame(all_brake_boat_new_series)
    res_df = res_df.sort_values(by='best_use_rate', ascending=False)
    alls = []
    for i in range(12):
        alls.append('name{}'.format(i + 1))
        alls.append('size{}'.format(i + 1))
    # res_df[alls]=
    aa = res_df['brake_boat'].apply(lambda x: process_res(x))
    aa['best_use_rate'] = res_df['best_use_rate']
    return aa
    # columns = ['best_use_rate', 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
    # aa.to_excel('{}.xlsx'.format('data_final_scheduled_sheet3'), index=False, columns=columns)
if __name__=='__main__':
    W = 32.8  # 33.5#32.8  # 34
    L = 264  # 280
    path='scheduled_total.xlsx'
    s_path='save_path'
    wait_list,ind_name=get_waitlist(path)

    filepath, fullflname = os.path.split(path)
    fname, ext = os.path.splitext(fullflname)
    brake_boat_df=get_brake_boat(np.array(wait_list), L, W, ind_name)

    columns = ['best_use_rate', 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
    brake_boat_df.to_excel(s_path+'/result_{}.xlsx'.format(fname), index=False, columns=columns)