import gurobipy as gp
from gurobipy import GRB

# Input data 먼저 10개의 예시 데이터 활용할 예정.
pairings = [['F3', 'DeadHead'],['F13', 'DeadHead'],['F13', 'F85', 'DeadHead'], ['F13', 'F36', 'DeadHead'], ['F13', 'F28', 'DeadHead']]
# salary 값 : base_salary, flight_salary, dead head, total == cost?
salary = [[1925, 228.8, 500, 2153.8],[2275,279.5,600,2554.5],[2275, 828.0999999999999, 600, 3617.2666666666664],
          [2275, 578.4999999999999, 600, 4036.8333333333335],[2275, 562.9, 600, 3274.5666666666666]]

# Xi 변수의 값을 나타내는 x 변수를 초기화합니다.
x = [1,1,1,1,1, 1,1,1,1,1]

# cost 값 저장
c = []

# 최적화 모델 생성
model = gp.Model('Crew_Pairing')

# 변수 추가 - model 내 addVar() 메소드를 활용하여 변수들을 지정해줍니다.
# 현재 수식 내 objective function에서 활용하는 변수는
# 1. cost (=Cp) 
# 2. Xp 
# 이며, 이때 Xp는 slackness 값에 따라 값이 변합니다. 

# cost 추가
for j in salary:
    c[j] = model.addVar( vtype=GRB.CONTINUOUS, name='c_%s' % j)

# x 변수 추가
for j in x:
    x[j] = model.addVar(vtype=GRB.CONTINUOUS, name='x_%s' % j)


# objective function 설정
# 각 인덱스 별로 Xp와 Cp의 값을 곱한 것의 합을 구하는 함수입니다.
obj = quicksum(x[i]* c[i] for i in range(10), GRB.MINIMIZE)
#해당 값을 setObjective obj함수로 설정합니다. 
model.setObjective(obj, GRB.MINIMIZE)

# slackness 변수 지정
slackness = 1

# column generation
# 실제 loop를 통해서 최적 값을 구하여 slackness를 기반으로 새로운 pairing 및 Xp를 수정합니다.
# (미완성)
while not slackness <= 0:
    # 모델 최적화
    model.optimize()

    # 1. Xp 값 로드 -> model에서 optimize하면 값이 도출?
    # x 변수의 값을 가져옵니다.
    new_cols = []
    for j in x:
        # model 내 'x' 속성 값을 load 해서 이를 새로운 new_cols로 로드 진행하기
        col = model.getAttr('x', x[j])
        new_cols.append((j, col))
    
    # 새로운 new_cols로부터 dual variables을 가져옵니다.
    pi = model.getAttr('Pi', model.getConstrs())



    #---여기서부터 미완성---------------------------------------------------
    # subproblem 선언
    # deadhead 여부에 따른 적용 여부 확인
    subproblem_model = gp.Model('Crew_Pairing_Subproblem')
    
    # subproblem 변수를 추가
    for i in range():
        subproblem_model.addVar(obj=0, vtype=GRB.CONTINOUS, name='y_%d' % i)

   
    # subproblem 제약조건을 추가
    for i in nodes:
        subproblem_model.addConstr(gp.quicksum(new_cols[j][1][i] * subproblem_model.getVarByName('y_%d' % j) for j in range(len(new_cols))) >= 1, name='Cover_%s' % i)
    
    # subproblem solver
    subproblem_model.optimize()
    
    # subproblem에서 나온 최적해 로드
    reduced_cost = subproblem_model.ObjVal

    # slackness 계산
    slackness = gp.quicksum( reduced_cost[i] * x[i] for i in range(len(new_cols)));

    # 결론 확인
    # slackness가 0보다 작으면 새로운 column을 추가합니다.
    if slackness < 0:
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
    #---미완성---------------------------------------------------
# 최적해 출력



##----------------------------------before code-----------------------------
# Variables
#z = m.addVar(vtype=GRB.CONTINUOUS, name='z')  # objective function 값
#y = m.addVars(len(x_values), vtype=GRB.BINARY, name='y')  # 각 pairing이 선택되는지 여부

# Define the objective function
# setObjective()함수 Gurobi 모델에서 목적 함수를 설정


# Constraints
#for i in range(len(x_values[0])):
#    m.addConstr(quicksum(y[p] * x_values[p][i] for p in range(len(x_values))) == 1, name='leg_{}'.format(i+1))

"""
# Column Generation Loop
while True:
    m.optimize()
    

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
"""