1.训练好的种群，可以在下一次初始化时直接调用，如果起那么保存下来的化；
  每一代保存下来的文件都可以查看每个个体染色体的具体值是多少，如果全都是一样的说明每个个体的染色体都找到了同样的最优值
  **（但是问题规模变了，之前的染色体就没法用了，其实每个染色体对应的是决策变量的值，
  如闸室调度，第一次总共25范围0-24，选最优排列的6艘为24,3,1,5,6,3;第二次闸室只剩下18艘范围是0-17，就用从0-17中重新选择6艘的排列了；
  至于如果问题规模相同，但是初始化的顺序是不同的，使用之前的染色体不知到行不行，还需进行测试）

path='./Result'
Chrom_res=pd.read_csv(os.path.join(path,'Chrom.csv'),header=None).to_numpy()
CV_res=pd.read_csv(os.path.join(path,'CV.csv'),header=None).to_numpy()
FitnV_res=pd.read_csv(os.path.join(path,'FitnV.csv'),header=None).to_numpy()
ObjV_res=pd.read_csv(os.path.join(path,'ObjV.csv'),header=None).to_numpy()
Phen_res=pd.read_csv(os.path.join(path,'Phen.csv'),header=None).to_numpy()

# __init__(self, Encoding, Field, NIND, Chrom=None, ObjV=None, FitnV=None, CV=None, Phen=None)
population = ea.Population(Encoding, Field, NIND,
                           Chrom=Chrom_res, ObjV=ObjV_res, FitnV=FitnV_res, CV=CV_res, Phen=Phen_res
                           ) # 实例化种群对象（此时种群还没被初始化，仅仅是完成种群对象的实例化）




2.交叉变异参数设置，
myAlgorithm = ea.soea_SEGA_templet(problem, population)  # 实例化一个算法模板对象#该算法宜设置较大的交叉和变异概率，否则生成的新一代种群中会有越来越多的重复个体。
myAlgorithm.MAXGEN = 10  # 最大进化代数
myAlgorithm.recOper = ea.Xovox(XOVR=0.8)  # 设置交叉算子 __init__(self, XOVR=0.7, Half=False)
myAlgorithm.mutOper = ea.Mutinv(Pm=0.1)  # 设置变异算子
myAlgorithm.drawing = 1  # 设置绘图方式（0：不绘图；1：绘制结果图；2：绘制过程动画）


3.每代的个数和进化的代数之间要有一个权衡，因为交叉和变异是在不同的代之间的
