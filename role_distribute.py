import csv
import os
os.system('clear')
import random

def distribute_roles(num_players):
    if str(num_players) not in player_list:
        raise ValueError(f"Invalid number of players. Must be between 7-15, got {num_players}")
    
    tf_count, wlz_count, minion_count, demon_count = player_list[str(num_players)]

    selected_minion = random.sample(minion_list, minion_count)
    
    if '教父' in selected_minion:
        if wlz_count != 0:        
            change = random.choice([-1, 1])
            wlz_count += change
            tf_count -= change
        else:
            wlz_count += 1
            tf_count -= 1

    selected_tf = random.sample(tf_list, tf_count)
    selected_wlz = random.sample(wlz_list, wlz_count)
    selected_demon = random.sample(demon_list, demon_count)
    
    special_notes = []

    final_roles = selected_tf + selected_wlz + selected_minion + selected_demon
    random.shuffle(final_roles)
    
    # Calculate absent roles
    all_possible_roles = tf_list + wlz_list + minion_list + demon_list
    absent_roles = [role for role in all_possible_roles if role not in final_roles]
 
    # Print role summary
    final_tf_count = sum(1 for role in final_roles if role in tf_list)
    final_wlz_count = sum(1 for role in final_roles if role in wlz_list)
    final_minion_count = sum(1 for role in final_roles if role in minion_list)
    final_demon_count = sum(1 for role in final_roles if role in demon_list)
    
    print(f"\n最终阵营人数:")
    print(f"村民阵营: {final_tf_count}")
    print(f"外来者阵营: {final_wlz_count}")
    print(f"爪牙阵营: {final_minion_count}")
    print(f"恶魔阵营: {final_demon_count}")
    
    print("\n不在场的角色:")
    for role in absent_roles:
        print(f"- {role}")

    valid_roles = [role for role in absent_roles if role not in demon_list and role not in minion_list and role not in ['疯子']]
    disguisers = random.sample(valid_roles, 3)

    return final_roles, special_notes, disguisers


#def evaluate_teams(roles, true_role, tf_list, tf_strength, wlz_list, wlz_strength, minion_list, minion_strength, demon_list, demon_strength):
    # Calculate team scores
#    score = [0] * 4
#    for i in range(len(tf_list)):
#        if tf_list[i] in roles:
#            score[0] += tf_strength[tf_list[i]]
#    if true_role is not None:
#        score[0] += tf_strength[true_role] / 2
#    for i in range(len(wlz_list)):
#        if wlz_list[i] in roles:
#            score[1] += wlz_strength[wlz_list[i]]
#    for i in range(len(minion_list)):
#        if minion_list[i] in roles:
#            score[2] += minion_strength[minion_list[i]]
#    for i in range(len(demon_list)):
#        if demon_list[i] in roles:
#            score[3] += demon_strength[demon_list[i]]
    
#    blue_strength = score[0] + score[1]  # 蓝方实力
#    red_strength = score[2] + score[3]   # 红方实力

#    return blue_strength, red_strength


# Define role lists
tf_list = ['祖母', '水手', '侍女', '驱魔人', '旅店老板', '赌徒', '造谣者', '侍臣', '教授', '吟游诗人', '茶艺师', '和平主义者', '弄臣']
wlz_list = ['莽夫', '修补匠', '疯子', '月之子']
minion_list = ['教父', '刺客', '魔鬼代言人', '主谋']
demon_list = ['僵怖', '沙巴洛斯', '普卡', '珀']

#tf_strength = {'贵族': 3, '舞蛇人': 3, '气球驾驶员': 5, '巡山人': 1, '工程师': 5, '渔夫': 3, '教授': 3, '博学者': 4, '农夫': 0, '食人族': 2, '罂粟种植者': 5}
#wlz_strength = {'酒鬼': 0, '落难少女': -2, '理发师': -1, '魔像': 2}
#minion_strength = {'投毒者': 5, '灵言师': 3, '精神病患者': 6, '麻脸巫婆': 7}
#demon_strength = {'哈迪寂亚': 8, '亡骨魔': 2}


player_list = {
    '7': [5,0,1,1],
    '8': [5,1,1,1], 
    '9': [5,2,1,1],
    '10': [7,0,2,1],
    '11': [7,1,2,1],
    '12': [7,2,2,1],
    '13': [9,0,3,1],
    '14': [9,1,3,1],
    '15': [9,2,3,1]
}

# Test the distribution
try:
    num_players = input('请输入玩家数量 (7-15): ')
#    blue_strength = 999
#    red_strength = 0

#    while 0.8 * blue_strength > red_strength or 0.8 * red_strength > blue_strength:
#        os.system('clear')        
    roles, special_notes, disguisers = distribute_roles(num_players)
#        blue_strength, red_strength = evaluate_teams(roles, true_role, tf_list, tf_strength, wlz_list, wlz_strength, minion_list, minion_strength, demon_list, demon_strength)
    
except Exception as e:
    print(f"发生错误: {e}")


# Display the final result
print(f"\n随机分配的{num_players}个角色:")
for i, role in enumerate(roles, 1):
    print(f"{i}. {role}")

with open('1_roles.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["生存", "醉毒", "技能", "号", "身份"])
    for i, role in enumerate(roles, 1):
        writer.writerow(["存活", "正常", "可用", f"{i:>2}", role])

if special_notes:
    print("\n特殊规则说明：")
    for note in special_notes:
        print(f"- {note}")

print(f"\n红方阵营的伪装身份是：{disguisers[0]}, {disguisers[1]}, {disguisers[2]}\n")
#print(f"蓝方实力：{blue_strength}, 红方实力：{red_strength}")