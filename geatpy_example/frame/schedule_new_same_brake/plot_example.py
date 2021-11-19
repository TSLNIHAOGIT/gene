# -*- coding: utf-8 -*-
"""
Created on Thu Aug 11 18:12:37 2016

@author: Eddy_zheng
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
def build_plot_para(brake_boat):
    X = []
    Y = []
    li = []
    wi = []
    N = len(brake_boat)
    for k, v in brake_boat.items():
        li.append(v[1][0])
        wi.append(v[1][1])
        X.append(v[0][0])
        Y.append(v[0][1])
    return np.array(X), np.array(Y), np.array(li), np.array(wi), N

def plot_example(X, Y, li, wi, N, brake_num=0):
    fig1 = plt.figure()
    ax1 = fig1.add_subplot(111, aspect='equal')
    # ax1 = plt.subplot(111)
    # 设置坐标轴范围，不然默认就是0-1之间x是（0,280），y是（0,34）
    ax1.axis([0, 280, 0, 34])

    colour = ['red', 'green', 'white', 'yellow', 'blue', 'black']
    for i in range(N):
        ax1.add_patch(
            patches.Rectangle(
                (X[i], Y[i]),  # (x,y)
                li[i],  # width
                wi[i],  # height
                color='black',
                fill=False
            )
        )

    # fig1.savefig('rect_{}.png'.format(brake_num), dpi=90, bbox_inches='tight')
    plt.show()
    # ax1.add_patch(
    #
    #     patches.Rectangle(
    #         (0.1, 0.1),   # (x,y)
    #         0.5,          # width
    #         0.5,          # height
    #     )
    #
    # )
    #
    #
    # ax1.add_patch(
    #     patches.Rectangle(
    #         (0.7, 0.7),   # (x,y)
    #         0.5,          # width
    #         0.5,          # height
    #     )
    # )
    # plt.gcf().set_size_inches(18, 10)
    # plt.show()
    # fig1.savefig('rect1.png', dpi=90, bbox_inches='tight')


if __name__ == '__main__':
    wait_list = [(119.53, 22.5),
                 (99.3, 16.92),
                 (85.5, 16.3),
                 (110, 17.2),
                 (110, 19.22),
                 (119.53, 22.5),
                 (99.3, 16.92),
                 (99.3, 16.92),
                 (85.5, 16.3),
                 (110, 17.2),
                 (110, 17.2),
                 (119.53, 22.5)]
    wait_list = wait_list[0:6]

    N = len(wait_list)
    W = 34
    L = 280

    # li=np.array([each[0] for each in wait_list])/L
    # wi=np.array([each[1] for each in wait_list])/W
    #
    # X=np.array([129.42922238, 177.63115518, 172.31146189, 168.24637649,
    #         90.59384038, 132.09799331])/L
    # Y=np.array([ 2.61286949, 12.38680287, 14.50734225, 15.76862964,  8.08009241,10.86250473])/W
    ##############################

    ##绘制单个闸室的图
    # # 判断是否有问题
    # brake_boat = {
    #     16: [(0, 0), (93.87, 16.06)],
    #     10: [(93.87, 0), (92.92, 22.13)],
    #     18: [(0, 16.06), (91.66, 17.91)],
    #     7: [(186.79000000000002, 0), (92.96, 21.72)]
    # }
    #
    # X = []
    # Y = []
    # li = []
    # wi = []
    # N = len(brake_boat)
    # for k, v in brake_boat.items():
    #     li.append(v[1][0])
    #     wi.append(v[1][1])
    #     X.append(v[0][0])
    #     Y.append(v[0][1])
    # plot_example(np.array(X), np.array(Y), np.array(li), np.array(wi), N)

    ##绘制多个闸室的图
    all_brake_boat={'0':
        {'brake_boat': {22: [(0, 0), (87.0, 15.0)], 38: [(0, 15.0), (93.0, 14.0)], 20: [(87.0, 0), (85.0, 14.0)],
                          26: [(93.0, 15.0), (75.0, 14.0)], 62: [(172.0, 0), (92.0, 15.0)],
                          49: [(168.0, 15.0), (92.0, 17.0)]}},
                    '1': {
        'brake_boat': {53: [(0, 0), (130.0, 17.0)], 59: [(0, 17.0), (78.0, 14.0)], 5: [(130.0, 0), (130.0, 17.0)],
                       23: [(78.0, 17.0), (92.0, 15.0)], 55: [(170.0, 17.0), (87.0, 15.0)]}},
                    '2': {
        'brake_boat': {57: [(0, 0), (105.0, 17.0)], 17: [(0, 17.0), (92.0, 15.0)], 63: [(105.0, 0), (75.0, 13.0)],
                       19: [(92.0, 17.0), (85.0, 15.0)], 48: [(177.0, 17.0), (87.0, 15.0)],
                       40: [(180.0, 0), (80.0, 14.0)]}}}
    all_brake_boat ={
        0: {'brake_boat': {55: [(0, 0), (87.0, 15.0)], 53: [(0, 15.0), (130.0, 17.0)], 23: [(87.0, 0), (92.0, 15.0)],
                        21: [(130.0, 15.0), (130.0, 17.0)], 19: [(179.0, 0), (85.0, 15.0)]},
         'best_use_rate': 0.8802521008403361}, 1: {
        'brake_boat': {7: [(0, 0), (92.0, 15.0)], 5: [(0, 15.0), (130.0, 17.0)], 37: [(130.0, 15.0), (130.0, 16.0)],
                       30: [(92.0, 0), (92.0, 15.0)], 40: [(184.0, 0), (80.0, 14.0)]},
        'best_use_rate': 0.8581932773109243}, 2: {
        'brake_boat': {62: [(0, 0), (92.0, 15.0)], 64: [(0, 15.0), (80.0, 14.0)], 34: [(80.0, 15.0), (92.0, 17.0)],
                       65: [(172.0, 15.0), (90.0, 17.0)], 58: [(92.0, 0), (85.0, 14.0)],
                       22: [(177.0, 0), (87.0, 15.0)]}, 'best_use_rate': 0.8496848739495798}}

    for brake_num,e_brake_boat in all_brake_boat.items():


        X, Y, li_e, wi_e, N_e=build_plot_para(e_brake_boat['brake_boat'])
        plot_example(X, Y, li_e, wi_e,N_e)