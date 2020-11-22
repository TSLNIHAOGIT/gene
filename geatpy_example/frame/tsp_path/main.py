# # -*- coding: utf-8 -*-
# import geatpy as ea # import geatpy
# import numpy as np
# import matplotlib.pyplot as plt
# from geatpy_example.frame.tsp_path.tsp import TestProblem
#
# if __name__ == '__main__':
#     """===============================瀹炰緥鍖栭棶棰樺�璞�==========================="""
#     problem = TestProblem('att48')        # 鐢熸垚闂��瀵硅薄
#     """=================================绉嶇兢璁剧疆==============================="""
#     Encoding = 'P'                        # 缂栫爜鏂瑰紡
#     NIND = 100                            # 绉嶇兢瑙勬ā
#     Field = ea.crtfld(Encoding, problem.varTypes, problem.ranges, problem.borders) # 鍒涘缓鍖哄煙鎻忚堪鍣�
#     population = ea.Population(Encoding, Field, NIND) # 瀹炰緥鍖栫�缇ゅ�璞★紙姝ゆ椂绉嶇兢杩樻病琚�垵濮嬪寲锛屼粎浠呮槸瀹屾垚绉嶇兢瀵硅薄鐨勫疄渚嬪寲锛�
#     """===============================绠楁硶鍙傛暟璁剧疆============================="""
#     myAlgorithm = ea.soea_SEGA_templet(problem, population) # 瀹炰緥鍖栦竴涓�畻娉曟ā鏉垮�璞★紝澧炲己绮捐嫳淇濈暀鐨勯仐浼犵畻娉曟ā鏉�
#     # 鏈�煭璺�▼涓猴細35225.41062921913
#     # myAlgorithm = ea.soea_EGA_templet(problem, population)
#     # 鏈�煭璺�▼涓猴細60020.228771634494
#     myAlgorithm.MAXGEN = 1000            # 鏈�ぇ杩涘寲浠ｆ暟
#     myAlgorithm.drawing = 1 # 璁剧疆缁樺浘鏂瑰紡锛�锛氫笉缁樺浘锛�锛氱粯鍒剁粨鏋滃浘锛�锛氱粯鍒剁洰鏍囩┖闂磋繃绋嬪姩鐢伙紱3锛氱粯鍒跺喅绛栫┖闂磋繃绋嬪姩鐢伙級
#     """==========================璋冪敤绠楁硶妯℃澘杩涜�绉嶇兢杩涘寲======================="""
#     [population, obj_trace, var_trace] = myAlgorithm.run() # 鎵ц�绠楁硶妯℃澘锛屽緱鍒版渶鍚庝竴浠ｇ�缇や互鍙婅繘鍖栬�褰曞櫒
#     population.save()                     # 鎶婃渶鍚庝竴浠ｇ�缇ょ殑淇℃伅淇濆瓨鍒版枃浠朵腑
#     # 杈撳嚭缁撴灉
#     best_gen = np.argmin(obj_trace[:, 1]) # 璁板綍鏈�紭绉嶇兢鏄�湪鍝�竴浠�
#     best_ObjV = np.min(obj_trace[:, 1])
#     print('鏈�煭璺�▼涓猴細%s'%(best_ObjV))
#     print('鏈�匠璺�嚎涓猴細')
#     best_journey = np.hstack([var_trace[best_gen, :], var_trace[best_gen, 0]])
#     for i in range(len(best_journey)):
#         print(int(best_journey[i]), end = ' ')
#     print()
#     print('鏈夋晥杩涘寲浠ｆ暟锛�s'%(obj_trace.shape[0]))
#     print('鏈�紭鐨勪竴浠ｆ槸绗�%s 浠�%(best_gen + 1))
#     print('璇勪环娆℃暟锛�s'%(myAlgorithm.evalsNum))
#     print('鏃堕棿宸茶繃 %s 绉�%(myAlgorithm.passTime))
#     # 缁樺浘
#     plt.figure()
#     plt.plot(problem.places[best_journey.astype(int), 0], problem.places[best_journey.astype(int), 1], c = 'black')
#     plt.plot(problem.places[best_journey.astype(int), 0], problem.places[best_journey.astype(int), 1], 'o', c = 'black')
#     for i in range(len(best_journey)):
#         plt.text(problem.places[int(best_journey[i]), 0], problem.places[int(best_journey[i]), 1], int(best_journey[i]), fontsize=15)
#     plt.grid(True)
#     plt.xlabel('x鍧愭爣')
#     plt.ylabel('y鍧愭爣')
#     plt.savefig('roadmap.svg', dpi=600, bbox_inches='tight')