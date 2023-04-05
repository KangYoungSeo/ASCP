import gurobipy as gp
from gurobipy import GRB

# Inputdata
# 예시 데이터 확인
pairings = [['F3', 'DeadHead'],['F13', 'DeadHead'],['F13', 'F85', 'DeadHead'], ['F13', 'F36', 'DeadHead'], ['F13', 'F28', 'DeadHead']]
# salary 값 : base_salary, flight_salary, dead head, total == cost?
salary = [[1925, 228.8, 500, 2153.8],[2275,279.5,600,2554.5],[2275, 828.0999999999999, 600, 3617.2666666666664],
          [2275, 578.4999999999999, 600, 4036.8333333333335],[2275, 562.9, 600, 3274.5666666666666]]


# 10개 기준으로 제공


# Xi 변수의 값을 나타내는 x 변수를 초기화합니다.
x = {1,1,1,1,1, 1,1,1,1,1}

# 최적화 모델 생성
model = gp.Model('Crew_Pairing')

# 변수 추가
for j in salary:
     x[i] = model.addVar(obj=c[i]* , vtype=GRB.INTEGER, name='x_%s' % i)


# 제약조건을 추가합니다.
for j in flights:
    model.addConstr(gp.quicksum(f[i, j] for i in nodes) == 1, name='Assign_%s' % j)

# objective function 선정
m.setObjective( quicksum( salary[i][2] * x[i] for i in range(1)), GRB.MAXIMIZE )
m.setObjective(z, GRB.MINIMIZE)
model.obje

# slackness 결과
slackness = 1

# column generation
while not slackness <= 0:
    # 모델 최적화 =
    model.optimize()
    
    # x 변수의 값을 가져옵니다.
    new_cols = []
    for j in x:
        # model 내 'x' 속성 값을 load 해서 이를 새로운 new_cols에 적용
        col = model.getAttr('x', x[:, j]) #특정 변수나 제약 조건을 확인해볼 수 있음.
        new_cols.append((j, col))
    


    # subproblem 선언
    subproblem_model = gp.Model('Crew_Pairing_Subproblem')
    
    # subproblem 변수를 추가합니다.
    for i in range(len(new_cols)):
        subproblem_model.addVar(obj=0, vtype=GRB.BINARY, name='y_%d' % i)

   
    # subproblem 제약조건을 추가합니다.
    for i in nodes:
        subproblem_model.addConstr(gp.quicksum(new_cols[j][1][i] * subproblem_model.getVarByName('y_%d' % j) for j in range(len(new_cols))) >= 1, name='Cover_%s' % i)
    
    # subproblem solver
    subproblem_model.optimize()
    
    # subproblem에서 나온 최적해 로드
    reduced_cost = subproblem_model.ObjVal
    


    # 결론 확인
    # reduced cost가 0보다 작으면 새로운 column을 추가합니다.
    if reduced_cost < 0:
        new_column = []
        for j in range(len(new_cols)):
            if subproblem_model.getVarByName('y_%d' % j).x > 0:
                new_column.append(new_cols[j][0])
        c[new_column] = calculate_cost(new_column)
        for j in flights:
            f[new_column, j] = model.addVar(obj=c[new_column, j], vtype=GRB.INTEGER, name='f_%s_%s' % (new_column, j))
        model.update()
        model.addConstr(gp.quicksum(f[new_column, j] for j in flights) == 1, name='Assign_%s' % new_column)
    else:
        break

# 최적해 출력



##----------------------------------before code-----------------------------
# Variables
z = m.addVar(vtype=GRB.CONTINUOUS, name='z')  # objective function 값
y = m.addVars(len(x_values), vtype=GRB.BINARY, name='y')  # 각 pairing이 선택되는지 여부

# Define the objective function
# setObjective()함수 Gurobi 모델에서 목적 함수를 설정


# Constraints
for i in range(len(x_values[0])):
    m.addConstr(quicksum(y[p] * x_values[p][i] for p in range(len(x_values))) == 1, name='leg_{}'.format(i+1))


# Column Generation Loop
while True:
    m.optimize()
    
    # Get dual variables
    pi = m.getAttr('Pi', m.getConstrs())
    
    # Add new column
    new_column = Column()
    for i in range(len(x_values)):
        new_column.addTerms(pi[i], y[i])
    z_coeff = sum(pi[i] * cost[i] for i in range(len(cost)))
    new_column.addTerms(1.0, z)
    
    # Add new variable to the model
    var = m.addVar(obj=z_coeff, vtype=GRB.CONTINUOUS, name='new_var', column=new_column)
    

    # Solve LP Relaxation
    m.optimize()

    # Check for optimality
    if m.objVal == 0:
        break
    elif m.objVal >= 0:
    
    # Check for integrality
    if all(y[p].X > 0.99 for p in range(len(x_values))):
        break
    
    # Add new variable to the restricted master problem
    y.append(m.addVar(vtype=GRB.BINARY, name='y_{}'.format(len(y))))
    for i in range(len(x_values[0])):
        m.addConstr(y[-1] * x_values[-1][i] == quicksum(y[p] * x_values[p][i] for p in range(len(x_values)-1)), name='leg_{}_{}'.format(len(y), i+1))