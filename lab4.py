# Ввод данных
m = int(input("Введите количество ЛЗП (m): "))
n = int(input("Введите количество ЛПП (n): "))

# Ввод вектора r_i (затраты на заготовку)
r = []
print("Введите затраты на заготовку r_i для каждого ЛЗП:")
for i in range(m):
    r.append(float(input(f"r_{i+1}: ")))

# Ввод вектора b_i (ограничения на заготовку)
b = []
print("Введите ограничения на заготовку b_i для каждого ЛЗП:")
for i in range(m):
    b.append(float(input(f"b_{i+1}: ")))

# Ввод вектора s_j (доход от продажи)
s = []
print("Введите доход от продажи s_j для каждого ЛПП:")
for j in range(n):
    s.append(float(input(f"s_{j+1}: ")))

# Ввод вектора w_j (затраты на переработку)
w = []
print("Введите затраты на переработку w_j для каждого ЛПП:")
for j in range(n):
    w.append(float(input(f"w_{j+1}: ")))

# Ввод вектора d_j (ограничения на производство)
d = []
print("Введите ограничения на производство d_j для каждого ЛПП:")
for j in range(n):
    d.append(float(input(f"d_{j+1}: ")))

# Ввод матрицы c_ij (затраты на транспортировку)
c = []
print("Введите затраты на транспортировку c_ij:")
for i in range(m):
    row = []
    for j in range(n):
        row.append(float(input(f"c_{i+1},{j+1}: ")))
    c.append(row)

# Ввод матрицы t_ij (норматив расхода)
t = []
print("Введите нормативы расхода t_ij:")
for i in range(m):
    row = []
    for j in range(n):
        row.append(float(input(f"t_{i+1},{j+1}: ")))
    t.append(row)

# Формирование целевой функции
# Коэффициенты: (s_j - w_j)/t_ij - r_i - c_ij
c_func = []
for i in range(m):
    for j in range(n):
        coef = (s[j] - w[j]) / t[i][j] - r[i] - c[i][j]
        c_func.append(coef)

# Количество переменных (m * n) и ограничений (m + n)
num_vars = m * n
num_constraints = m + n

# Формирование матрицы ограничений A и вектора правых частей B
A = []
B = []

# Ограничения на заготовку: sum(x_ij) <= b_i
for i in range(m):
    row = [0] * num_vars
    for j in range(n):
        row[i * n + j] = 1
    A.append(row)
    B.append(b[i])

# Ограничения на производство: sum(x_ij / t_ij) <= d_j
for j in range(n):
    row = [0] * num_vars
    for i in range(m):
        row[i * n + j] = 1 / t[i][j]
    A.append(row)
    B.append(d[j])

# Симплекс-метод
# Инициализация симплекс-таблицы
table = []
for i in range(num_constraints):
    row = A[i] + [B[i]]
    table.append(row)
# Добавляем целевую функцию (минимизация, поэтому -c_func)
obj_row = [-x for x in c_func] + [0]
table.append(obj_row)

# Базисные переменные (добавляем слабины)
basis = list(range(num_constraints))

# Основной цикл симплекс-метода
while True:
    # Находим минимальный элемент в строке целевой функции
    pivot_col = 0
    min_val = 0
    for j in range(num_vars + 1):
        if table[num_constraints][j] < min_val:
            min_val = table[num_constraints][j]
            pivot_col = j
    if min_val >= 0:
        break  # Оптимальное решение найдено

    # Находим ведущую строку
    pivot_row = -1
    min_ratio = float('inf')
    for i in range(num_constraints):
        if table[i][pivot_col] > 0:
            ratio = table[i][-1] / table[i][pivot_col]
            if ratio < min_ratio:
                min_ratio = ratio
                pivot_row = i
    if pivot_row == -1:
        print("Задача не имеет решения (неограничена).")
        exit()

    # Нормируем ведущую строку
    pivot = table[pivot_row][pivot_col]
    for j in range(num_vars + 1):
        table[pivot_row][j] /= pivot

    # Обновляем остальные строки
    for i in range(num_constraints + 1):
        if i != pivot_row:
            coef = table[i][pivot_col]
            for j in range(num_vars + 1):
                table[i][j] -= coef * table[pivot_row][j]

    # Обновляем базис
    basis[pivot_row] = pivot_col

# Извлечение решения
solution = [0] * num_vars
for i in range(num_constraints):
    if basis[i] < num_vars:
        solution[basis[i]] = table[i][-1]

# Вывод результата
print("\nОптимальное решение:")
for i in range(m):
    for j in range(n):
        print(f"x_{i+1},{j+1} = {solution[i * n + j]:.2f}")
print(f"Максимальный доход: {-table[num_constraints][-1]:.2f}")