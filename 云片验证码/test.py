import random


def get_potions(offset):
    arrays = []
    downtime = random.randint(1, 20)  # 模拟滑块位移的时间差
    buttonx = random.randint(1100, 1154)  # 模拟鼠标按下滑块时的page.X值
    buttony = random.randint(1954, 1990)  # 模拟鼠标按下滑块时的page.Y值
    array1 = [buttonx, buttony, downtime]
    arrays.append(array1)
    for i in range(offset):  # offset是识别出的滑块距离，假设每次移动1px最多有offset个鼠标移动数组
        if arrays[-1][0] <= offset + buttonx:  # 判断滑块移动是否超过了offset
            if arrays[-1][0] <= buttonx + int((offset / 6) * 5):  # 模拟人在滑动最后减速，在此判断是否剩最后的1/6距离，如果是则减速
                arrays.append([
                    arrays[-1][0] + random.choice([2, 3, 4, 5]),
                    buttony + random.choice([1, -1, 2, -2, 0, 0]),
                    arrays[-1][2] + random.randint(1, 20)
                ])

            else:
                arrays.append([
                    arrays[-1][0] + random.choice([1, 1, 1, 0]),
                    buttony + random.choice([1, -1, 2, -2, 0, 0]),
                    arrays[-1][2] + random.randint(1, 20)
                ])
        else:
            break

    # 下面是复现js的逻辑，对鼠标轨迹数组长度判断并处理
    if len(arrays) < 50:
        return arrays

    newarrays = [arrays[0]]
    lastarray = arrays[-1]
    r = int(len(arrays) / 50)

    if r < 2:
        return arrays

    for i in range(1 + r, len(arrays) - 2, r):
        newarrays.append(arrays[i])
    newarrays.append(lastarray)
    return newarrays


if __name__ == '__main__':
    pos = get_potions(259)
    print(pos)