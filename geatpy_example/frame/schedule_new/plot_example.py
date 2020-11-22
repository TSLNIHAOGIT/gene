# -*- coding: utf-8 -*-
"""
Created on Thu Aug 11 18:12:37 2016

@author: Eddy_zheng
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np




def plot_example(X,Y,li,wi,N,brake_num=0):

    fig1 = plt.figure()
    ax1 = fig1.add_subplot(111, aspect='equal')


    colour=['red','green','white','yellow','blue','black']
    for i in range(N):
        ax1.add_patch(
                patches.Rectangle(
                    (X[i], Y[i]),   # (x,y)
                    li[i],          # width
                    wi[i],          # height
                    color='black',
                    fill=False
                )
            )
    fig1.savefig('rect_{}.png'.format(brake_num), dpi=90, bbox_inches='tight')

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

    plt.show()
    # fig1.savefig('rect1.png', dpi=90, bbox_inches='tight')

if __name__=='__main__':
    wait_list=[(119.53, 22.5),
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
    wait_list=wait_list[0:6]
    
    
    N=len(wait_list)
    W=34
    L=280
    
    li=np.array([each[0] for each in wait_list])/L
    wi=np.array([each[1] for each in wait_list])/W
    
    X=np.array([129.42922238, 177.63115518, 172.31146189, 168.24637649,
            90.59384038, 132.09799331])/L
    Y=np.array([ 2.61286949, 12.38680287, 14.50734225, 15.76862964,  8.08009241,10.86250473])/W    
    plot_example(X, Y, li, wi,N)