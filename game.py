import csv
import re
import random

night = input('这是第几晚？')

with open(night + '_roles.csv', mode='r', encoding='utf-8') as file:
    reader = csv.reader(file)
    data = list(reader)

if night != '1':
    with open(str(int(night)-1)+'_lynch.csv', mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        lynched = list(reader)
else:
    lynched = ''

tf_list = ['贵族', '舞蛇人', '气球驾驶员', '巡山人', '工程师', '渔夫', '教授', '博学者', '失忆者', '农夫', '食人族', '罂粟种植者']
wlz_list = ['酒鬼', '落难少女', '理发师', '魔像']
minion_list = ['投毒者', '灵言师', '精神病患者', '麻脸巫婆']
demon_list = ['哈迪寂亚', '亡骨魔']
poison_bool = False
death_list = []
reborn_list = []

print("读取的角色信息:")
for row in data:
    print(f"{row[0]}, {row[1]}, {row[2]}, {row[3]}")

def get_index(data, role):
    for index, row in enumerate(data):
        if row[-1] == role:
            return int(index)
    return None

def get_amnesiac(data):
    for index, row in enumerate(data):
        if '失忆者' in ''.join(row):
            return int(index)
    return None

print('\n')

if get_index(data, '食人族') != None:
    if len(lynched) > 0:
        c = input(f"（说书人）{get_index(data, '食人族')+1}号食人族吃了{lynched[0][-1]}！")
    else:
        c = input(f"（说书人）{get_index(data, '食人族')+1}号食人族无技能！")

if get_index(data, '罂粟种植者') != None and data[get_index(data, '罂粟种植者')][0] != '死亡' and data[get_index(data, '罂粟种植者')][0] != '中毒':
    y = input(f"（说书人）{get_index(data, '罂粟种植者') + 1}号罂粟种植者在场哦，不能不能不能给红方阵营建群！")
else:
    y = input(f"（说书人）罂粟种植者不在场哦，记得要给红方阵营建群！")

if get_amnesiac(data) != None and data[get_amnesiac(data)][0] != '死亡' and night != '1':
    guess = input(f'{get_amnesiac(data)+1}号失忆者猜对自己是谁了吗？(y/n) ')
    if guess == 'y':
        for row in data:
            for i, element in enumerate(row):
                if '失忆者' in element:
                    match = re.search(r'失忆者\((.*?)\)', element)
                    if match:
                        name_in_parentheses = match.group(1)  # Extract the name
                        row[i] = f"{name_in_parentheses}"

if get_index(data, '工程师') != None and data[get_index(data, '工程师')][0] != '死亡' and data[get_index(data, '工程师')][1] == '可用':
    action = input(f"{get_index(data, '工程师')+1}号工程师行动吗？(y/n) ")
    if action == 'y':
        data[get_index(data, '工程师')][1] = '不可'
        who = input(' - 选择爪牙还是恶魔？(m/d) ')
        if who == 'd':
            change = input(' - 把他变成亡骨魔还是哈迪寂亚？(w/h) ')
            for index, row in enumerate(data):
                if row[-1] == '亡骨魔' or row[-1] == '哈迪寂亚':
                    if change == 'w' and data[get_index(data, '工程师')][0] != '中毒':
                        row[-1] = '亡骨魔'
                    elif change == 'h' and data[get_index(data, '工程师')][0] != '中毒':
                        row[-1] = '哈迪寂亚'
        elif who == 'm':
            roles_to_check = ['投毒者', '麻脸巫婆', '精神病患者', '灵言师']
            matching_rows = []
            for index, row in enumerate(data):
                if row[-1] in roles_to_check:
                    matching_rows.append(index + 1)
            roles_to_change = input(f' - 输入{len(matching_rows)}个爪牙角色(td/wp/jsb/ly) ')
            roles_input = roles_to_change.split()
            dict = {'td': '投毒者', 'wp': '麻脸巫婆', 'jsb': '精神病患者', 'ly': '灵言师'}
            random.shuffle(roles_input)
            
            if data[get_index(data, '工程师')][0] != '中毒':
                for i in range(len(matching_rows)):
                    data[matching_rows[i]-1][-1] = dict[roles_input[i]]

if get_index(data, '投毒者') != None and data[get_index(data, '投毒者')][0] != '死亡':
    poison = input(f"{get_index(data, '投毒者')+1}号投毒者选择谁下毒？")
    data[int(poison)-1][0] = '中毒'
    poison_bool = True

if get_index(data, '舞蛇人') != None and data[get_index(data, '舞蛇人')][0] != '死亡':
    dance = input(f"{get_index(data, '舞蛇人')+1}号舞蛇人选择舞谁？")
    if data[int(dance)-1][-1] not in demon_list or data[get_index(data, '舞蛇人')][0] == '中毒':
        print(' - 无事发生！')
    else:
        data[get_index(data, '舞蛇人')][-1] = data[int(dance)-1][-1]
        data[int(dance)-1][0] = '中毒'
        print(f' - 舞蛇人成为了{data[int(dance)-1][-1]}！')
        data[int(dance)-1][-1] = '蓝方恶魔'

if get_index(data, '麻脸巫婆') != None and night != '1' and data[get_index(data, '麻脸巫婆')][0] != '死亡':
    decoct = input(f"{get_index(data, '麻脸巫婆')+1}号麻脸巫婆选择熬谁？")
    char = input(' - 把他变成谁？')
    if get_index(data, char) == None and not any(char in ''.join(row) for row in data):
        if char != '落难少女' and data[get_index(data, '麻脸巫婆')][0] != '中毒':
            data[int(decoct)-1][-1] = char
        elif char == '落难少女' and data[get_index(data, '麻脸巫婆')][0] != '中毒':
            decoct = input('（说书人）选择把谁变成落难少女：')
            data[int(decoct)-1][-1] = char

if get_index(data, '灵言师') != None and night == '1':
    word = input(f"（说书人）告诉{get_index(data, '灵言师')+1}号灵言师关键词！")

if get_index(data, '亡骨魔') != None and night != '1':
    bone_kill = input(f"{get_index(data, '亡骨魔')+1}号亡骨魔请选择要杀死的玩家：")
    if data[int(bone_kill)-1][-1] not in minion_list and data[get_index(data, '亡骨魔')][0] != '中毒':
        if data[int(bone_kill)-1][0] != '死亡':
            death_list.append(int(bone_kill))
            data[int(bone_kill)-1][0] = '死亡'
    elif data[int(bone_kill)-1][-1] in minion_list and data[get_index(data, '亡骨魔')][0] != '中毒':
        if data[int(bone_kill)-1][0] != '死亡':
            death_list.append(int(bone_kill))  
            data[int(bone_kill)-1][0] = '死亡'
        toxic = input('（说书人）选择让谁中毒：')
        data[int(toxic)-1][0] = '中毒'

if get_index(data, '哈迪寂亚') != None and night != '1':
    hd_kill = input(f"{get_index(data, '哈迪寂亚')+1}号哈迪寂亚请选择三名杀死的玩家：").split()
    print(' - 欢迎来到血肉牢笼！')
    survive_1 = input(f' - 请{hd_kill[0]}号点头表示生与死(y/n) ')
    survive_2 = input(f' - 请{hd_kill[1]}号点头表示生与死(y/n) ')
    survive_3 = input(f' - 请{hd_kill[2]}号点头表示生与死(y/n) ')

    survive = [survive_1, survive_2, survive_3]
    if all(s == 'y' for s in survive):
        for person in hd_kill:
            if data[get_index(data, '哈迪寂亚')][0] != '中毒':
                if data[int(hd_kill[0])-1][0] != '死亡':
                    death_list.append(int(hd_kill[0]))
                if data[int(hd_kill[1])-1][0] != '死亡':
                    death_list.append(int(hd_kill[1]))
                if data[int(hd_kill[2])-1][0] != '死亡':
                    death_list.append(int(hd_kill[2]))  
                data[int(hd_kill[0])-1][0] = '死亡'
                data[int(hd_kill[1])-1][0] = '死亡'
                data[int(hd_kill[2])-1][0] = '死亡'
    else:
        if data[get_index(data, '哈迪寂亚')][0] != '中毒':
            for i, s in enumerate(survive):
                if s == 'n':
                    if data[int(hd_kill[i])-1][0] != '死亡':
                        death_list.append(int(hd_kill[i]))
                    data[int(hd_kill[i])-1][0] = '死亡'
                else:
                    if data[int(hd_kill[i])-1][0] == '死亡':
                        reborn_list.append(int(hd_kill[i]))
                    data[int(hd_kill[i])-1][0] = '正常'


if get_index(data, '理发师') != None and data[get_index(data, '理发师')][1] == '可用':
    if data[get_index(data, '理发师')][0] == '死亡':
        exchange = input(f"{get_index(data, '理发师')+1}号理发师已死亡，请恶魔选择两名玩家交换角色：").split()
        role_1 = data[int(exchange[0])-1][-1]
        role_2 = data[int(exchange[1])-1][-1]
        data[get_index(data, '理发师')][1] = '不可'
        if data[get_index(data, '理发师')][0] != '中毒':
            data[int(exchange[0])-1][-1] = role_2
            data[int(exchange[1])-1][-1] = role_1

if get_index(data, '教授') != None and data[get_index(data, '教授')][0] != '死亡' and data[get_index(data, '教授')][1] == '可用' and night != '1':
    save = input(f"{get_index(data, '教授')+1}号教授要复活玩家吗？(y/n) ")
    if save == 'y':
        data[get_index(data, '教授')][1] = '不可'
        who_save = input(' - 要复活谁？')
        if data[get_index(data, '教授')][0] != '中毒':
            if data[int(who_save)-1][0] == '死亡':
                reborn_list.append(int(who_save))
            data[int(who_save)-1][0] = '正常'
            data[int(who_save)-1][1] = '可用'

if get_index(data, '农夫') != None and data[get_index(data, '农夫')][1] == '可用' and night != '1':
    if data[get_index(data, '农夫')][0] == '死亡':
        die = input(f"{get_index(data, '农夫')+1}号农夫是死在晚上吗？(y/n) ")
        if die == 'y' and data[get_index(data, '农夫')][0] != '中毒':
            data[get_index(data, '农夫')][1] = '不可'
            change = input('（说书人）选择一名玩家变成农夫：')
            data[int(change)-1][-1] = '农夫'

if get_index(data, '巡山人') != None and data[get_index(data, '巡山人')][0] != '死亡' and data[get_index(data, '巡山人')][1] == '可用':
    ranger = input(f"{get_index(data, '巡山人')+1}号巡山人要猜谁是落难少女吗？(y/n) ")
    if ranger == 'y':
        data[get_index(data, '巡山人')][1] = '不可'
        who_ranger = input(' - 要猜谁？')
        if data[int(who_ranger)-1][-1] == '落难少女':
            avail = tf_list.copy()
            for index, row in enumerate(data):
                if '(' in row[-1] and ')' in row[-1]:
                    base_role = row[-1].split('(')[1].strip(')')
                    base_role_before = row[-1].split('(')[0].strip()
                    if base_role_before in avail and base_role_before != '酒鬼':
                        avail.remove(base_role_before)
                    if base_role in avail:
                        avail.remove(base_role)
                else:
                    base_role = row[-1]
                if base_role in avail:
                    avail.remove(base_role)
            if data[get_index(data, '巡山人')][0] != '中毒':
                if '失忆者' in avail:
                    avail.remove('失忆者')
                data[int(who_ranger)-1][-1] = random.choice(avail)
                print(f' - {int(who_ranger)}号变成了{data[int(who_ranger)-1][-1]}！')
            else:
                print(' - 无事发生！')
        else:
            print(' - 无事发生！')

if get_index(data, '贵族') != None and night == '1':
    if data[get_index(data, '贵族')][0] == '正常':
        a = input(f"（说书人）请告诉{get_index(data, '贵族')+1}号贵族正确信息哦！")
    elif data[get_index(data, '贵族')][0] == '中毒':
        a = input(f"（说书人）请告诉{get_index(data, '贵族')+1}号贵族错误信息哦！")

if get_index(data, '气球驾驶员') != None and data[get_index(data, '气球驾驶员')][0] != '死亡':
    if data[get_index(data, '贵族')][0] == '正常':
        balloon = input(f"（说书人）请告诉{get_index(data, '气球驾驶员')+1}号气球驾驶员正确信息哦！")
    elif data[get_index(data, '贵族')][0] == '中毒':
        balloon = input(f"（说书人）请告诉{get_index(data, '气球驾驶员')+1}号气球驾驶员错误信息哦！")

print("\n更新后的角色信息:")
for row in data:
    print(', '.join(row))

print('\n')
print('今晚死亡的玩家是：', death_list)
print('今晚复活的玩家是：', reborn_list)

if get_index(data, '渔夫') != None and data[get_index(data, '渔夫')][1] == '可用' and data[get_index(data, '渔夫')][0] != '死亡':
    fisher = input('（说书人）渔夫要问信息吗？(y/n) ')
    if fisher == 'y':
        data[get_index(data, '渔夫')][1] = '不可'
        if data[get_index(data, '渔夫')][0] == '正常':
            f = input(f"（说书人）告诉{get_index(data, '渔夫')+1}号渔夫正确信息哦！")
        elif data[get_index(data, '渔夫')][0] == '中毒':
            f = input(f"（说书人）告诉{get_index(data, '渔夫')+1}号渔夫错误信息哦！")

if get_index(data, '博学者') != None and data[get_index(data, '博学者')][0] != '死亡':
    if data[get_index(data, '博学者')][0] == '正常':
        b = input(f"（说书人）告诉{get_index(data, '博学者')+1}号博学者正确信息哦！")
    elif data[get_index(data, '博学者')][0] == '中毒':
        b = input(f"（说书人）告诉{get_index(data, '博学者')+1}号博学者错误信息哦！")

if get_index(data, '精神病患者') != None and data[get_index(data, '精神病患者')][0] != '死亡':
    jsb = input('（说书人）精神病要砍人吗？(y/n) ')
    if jsb == 'y':
        who_jsb = input(' - 谁被砍死了？')
        data[int(who_jsb)-1][0] = '死亡'

if get_index(data, '魔像') != None and data[get_index(data, '魔像')][1] == '可用':    
    statue = input('（说书人）魔像有撞死人吗？(y/n) ')
    if statue == 'y':
        who_statue = input(' - 谁被撞死了？')
        data[int(who_statue)-1][0] = '死亡'
        data[get_index(data, '魔像')][1] = '不可'

lynch = input('（说书人）有人被处决了？(y/n) ')
if lynch == 'y':
    who_lynch = input('（说书人）谁被处决了？')
    data[int(who_lynch)-1][0] = '死亡'

if poison_bool == True:
    if data[int(poison)-1][0] == '中毒':
        data[int(poison)-1][0] = '正常'

print("\n更新后的角色信息:")
for row in data:   
    print(', '.join(row))

with open(str(int(night)+1) + '_roles.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    for row in data:
        writer.writerow(row)

if lynch == 'y':
    with open(str(int(night)) + '_lynch.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(data[int(who_lynch)-1])
