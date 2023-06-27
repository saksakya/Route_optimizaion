import pulp as pp


class Route(object):
    """徒歩での最適な移動の経路を検索

    Args:
        object (_type_): _description_
    """
    def __init__(self, dm):
        self.dm = dm
        self.N = len(dm)
        self.BigM = 10**4
    
    
    def return_start(self):
        """各地を巡回して、スタート地点に戻る場合の最適巡回路
        """
        problem = pp.LpProblem('opt_route',pp.LpMinimize)
        
        #何度も使うので、簡略化
        N = self.N
        
        # 変数の定義 (Memo binary:0or1 continuous:low:1~up:nまでの連続値)
        x = [[pp.LpVariable("x(%s,%s)"%(i, j), cat="Binary") for i in range(N)] for j in range(N)]
        u = [pp.LpVariable("u(%s)"%(i), cat="Continuous", lowBound=1.0, upBound=(N)) for i in range(N)]

        #print(x)
        #print(u)

        # 目的条件(距離の総和)
        objective = pp.lpSum(self.dm[i][j] * x[i][j] for i in range(N) for j in range(N) if i != j)
        problem += objective

        # 制約条件1(制約条件1と2で各地点1回ずつしか通らない条件)
        for i in range(N):
            problem += pp.lpSum(x[i][j] for j in range(N) if i != j) == 1

        # 制約条件2
        for i in range(N):
            problem += pp.lpSum(x[j][i] for j in range(N) if i != j) == 1

        # 制約条件3(MTZ制約)
        for i in range(N):
            for j in range(1,N):
                if i != j:
                    problem += u[i] + 1.0 - self.BigM * (1.0 - x[i][j]) <= u[j]
                    
        # print(problem)
        
        # 最適化の実行
        status = problem.solve()

        # 結果の把握
        # print("Status: {}".format(pp.LpStatus[status]))
        # print("Optimal Value [a.u.]: {}".format(objective.value()))

        # for i in range(N):
        #     for j in range(N):
        #         if i != j:
        #             print("x[%d][%d]:%f" % (i,j,x[i][j].value()))

        # for i in range(len(u)):
        #     print("u[%d] %f" % (i,u[i].value()))
        
        # 変更後の順番を記録した変数を戻り値とする。
        ru = []
        for i in range(len(u)):
            ru.append(int(u[i].value() - 1))

        return ru
    
    
    def start_to_end(self):
        """各地を巡回して、スタートからゴールへ向かう場合の最適巡回路
        """
        #上記との差異：0はスタート地点のため、(x,0)はなし、最終はゴールのため(n,x)からの移動はなし
        problem = pp.LpProblem('opt_route',pp.LpMinimize)
        
        #何度も使うので、簡略化
        N = self.N
        
        # 変数の定義 (Memo binary:0or1 continuous:low:1~up:nまでの連続値)
        x = [[pp.LpVariable("x(%s,%s)"%(i, j), cat="Binary") for i in range(N)] for j in range(N)]
        u = [pp.LpVariable("u(%s)"%(i), cat="Continuous", lowBound=1.0, upBound=(N)) for i in range(N)]

        # print(x)
        # print(u)

        # 目的条件(距離の総和) 
        objective = pp.lpSum(self.dm[i][j] * x[i][j] for i in range(N - 1) for j in range(1,N) if i != j)
        problem += objective

        # 制約条件1(制約条件1と2で各地点1回ずつしか通らない条件)
        for i in range(N - 1):
            problem += pp.lpSum(x[i][j] for j in range(1,N) if i != j) == 1

        # 制約条件2
        for i in range(1,N):
            problem += pp.lpSum(x[j][i] for j in range(N - 1) if i != j) == 1

        # 制約条件3
        problem += pp.lpSum(x[0][4]) == 0

        # 制約条件4(MTZ制約)
        for i in range(N):
            for j in range(1,N):
                if i != j:
                    problem += u[i] + 1.0 - self.BigM * (1.0 - x[i][j]) <= u[j]
                    
        # print(problem)
        
        # 最適化の実行
        status = problem.solve()

        # 結果の把握
        # print("Status: {}".format(pp.LpStatus[status]))
        # print("Optimal Value [a.u.]: {}".format(objective.value()))

        # for i in range(N - 1):
        #     for j in range(1,N):
        #         if i != j:
        #             print("x[%d][%d]:%f" % (i,j,x[i][j].value()))

        # for i in range(len(u)):
        #     print("u[%d] %f" % (i,u[i].value()))
        
        # 変更後の順番を記録した変数を戻り値とする。
        ru = []
        for i in range(len(u)):
            ru.append(int(u[i].value() - 1))

        return ru