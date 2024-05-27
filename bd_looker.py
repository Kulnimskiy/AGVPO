

def main():
    values = get_values()
    unknown = int(input("Сколько неправильных?: "))
    target = float(input("Сумма: "))
    #target = 451643567
    slack = 10
    print(values)
    combos = []
    find_combo([], unknown, 1, values, target, slack, combos)
    print()
    if not combos:
        print("Нет совпадений")
        return
    for combo in combos:
        for element in combo:
            print(f"{values[element]} \t", end="")
        print(f" = {sum([values[i] for i in combo])}")


def get_values():
    values = []
    path = "C:\\Users\\User\\Desktop\\АГВ Проекты\\Поиск ошибок в БД\\numbers.txt"
    with open(path, "r") as file:
        for row in file.readlines():
            row = row.strip('\n').replace(",", ".")
            values.append(float(row))
    if not values:
        raise ValueError("Нет значений в файлике 'numbers.txt' или самого файлика ")
    return values


def find_combo(indices: list, limit: int, cut_depth: int, values: list, trgt: float, slack, combos:list):
    for i in values:
        index = values.index(i)
        if index in indices:
            continue
        if cut_depth == limit:
            indices.append(index)
            #print(indices)
            #print("in")
            s = sum(values) - sum([values[i] for i in indices])
            #print(s)
            if s < trgt + slack and s > trgt - slack:
                combos.append(indices.copy())
                print(indices, "got it------------------------------")
            indices.remove(index)
        else:
            indices.append(index)
            #print(indices, "skip")
            some_combo = find_combo(indices, limit, cut_depth + 1, values, trgt, slack, combos)
            indices.remove(index)

if __name__ == "__main__":
    while True:
        main()
