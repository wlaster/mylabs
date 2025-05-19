from pulp import LpMaximize, LpProblem, LpVariable, lpSum, value

m = int(input("Введите количество ЛЗП (m): "))
n = int(input("Введите количество ЛПП (n): "))

r = []
print("Введите затраты на заготовку r_i для каждого ЛЗП:")
for i in range(m):
    r.append(float(input(f"r_{i+1}: ")))

b = []
print("Введите ограничения на заготовку b_i для каждого ЛЗП:")
for i in range(m):
    b.append(float(input(f"b_{i+1}: ")))

s = []
print("Введите доход от продажи s_j для каждого ЛПП:")
for j in range(n):
    s.append(float(input(f"s_{j+1}: ")))

w = []
print("Введите затраты на переработку w_j для каждого ЛПП:")
for j in range(n):
    w.append(float(input(f"w_{j+1}: ")))

d = []
print("Введите ограничения на производство d_j для каждого ЛПП:")
for j in range(n):
    d.append(float(input(f"d_{j+1}: ")))

c_trans = []
print("Введите затраты на транспортировку c_ij:")
for i in range(m):
    row = []
    for j in range(n):
        row.append(float(input(f"c_{i+1},{j+1}: ")))
    c_trans.append(row)

t = []
print("Введите нормативы расхода t_ij:")
for i in range(m):
    row = []
    for j in range(n):
        row.append(float(input(f"t_{i+1},{j+1}: ")))
    t.append(row)

model = LpProblem(name="maximize_profit", sense=LpMaximize)

# x[i][j] - объем сырья
x = []
for i in range(m):
    row = []
    for j in range(n):
        var = LpVariable(name=f"x_{i+1}_{j+1}", lowBound=0)
        row.append(var)
    
    x.append(row)

profit = 0

for i in range(m):
    for j in range(n):
        profit_per_unit = ((s[j] - w[j]) / t[i][j]) - r[i] - c_trans[i][j]
        profit += profit_per_unit * x[i][j]

# Добавляем целевую функцию в модель
model += profit

# Ограничение на заготовку
for i in range(m):
    total_sent_from_i = sum(x[i][j] for j in range(n))
    model += total_sent_from_i <= b[i], f"supply_limit_{i+1}"

# Ограничение на производство
for j in range(n):
    total_raw_for_j = sum((1 / t[i][j]) * x[i][j] for i in range(m))
    model += total_raw_for_j <= d[j], f"production_limit_{j+1}"

model.solve()

print("\nСтатус решения:", model.status)
print("Максимальный доход:", value(model.objective))

print("\nОбъемы перевозок:")
for i in range(m):
    for j in range(n):
        print(f"x_{i+1}_{j+1} = {value(x[i][j]):.2f}")