max_width = 10
outer_list = list()
test_list = [i for i in range(0, max_width)]
for i in range(0, max_width):
    inner_list = list()
    if i <= int(max_width / 2):
        for j in range(0, i):
            inner_list.append(j)
        if i == int(max_width / 2) and (max_width % 2) == 1:
            inner_list.append(int(max_width / 2))
        for j in range(i - 1, -1, -1):
            inner_list.append(-1 * (j + 1))
    if inner_list:
        outer_list.append(inner_list)
for i in outer_list:
    print(i)
    print('-' * 10)
    for j in i:
        print(f'\t{test_list[j]}')
