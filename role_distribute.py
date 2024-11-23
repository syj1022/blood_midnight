import csv
import os
os.system('clear')
import random

def get_drunk_disguise(available_roles):
    #available_disguises = [role for role in tf_list if role not in selected_roles and role not in ['失忆者', '罂粟种植者']]
    disguise = random.choice(available_roles)
    return disguise

def distribute_roles(num_players):
    if str(num_players) not in player_list:
        raise ValueError(f"Invalid number of players. Must be between 7-15, got {num_players}")
    
    # Get role counts based on player count
    tf_count, wlz_count, minion_count, demon_count = player_list[str(num_players)]

    # Select demon roles
    selected_demon = random.sample(demon_list, demon_count)
    if '亡骨魔' in selected_demon and wlz_count != 0:
        wlz_count -= 1
        tf_count += 1

    # Adjust logic based on roles like Balloonist, Ranger
    selected_tf = random.sample(tf_list, tf_count)
    selected_wlz = random.sample(wlz_list, wlz_count)
    selected_minion = random.sample(minion_list, minion_count)
    
    special_notes = []

    # Apply Balloonist effect
    if '气球驾驶员' in selected_tf and not ('亡骨魔' in selected_demon and num_players in ['7','10','13']):
        removable_tf = [role for role in selected_tf if role != '气球驾驶员']
        if removable_tf:
            role_to_remove = random.choice(removable_tf)
            selected_tf.remove(role_to_remove)
            available_wlz = [role for role in wlz_list if role not in selected_wlz]
            if available_wlz:
                new_wlz = random.choice(available_wlz)
                selected_wlz.append(new_wlz)
                special_notes.append("注意：由于气球驾驶员在场，一个村民已变成外来者")

    # Apply Ranger effect
    if '巡山人' in selected_tf and '落难少女' not in selected_wlz:
        removable_tf = [role for role in selected_tf if role not in ['巡山人', '气球驾驶员']]
        if removable_tf:
            role_to_remove = random.choice(removable_tf)
            selected_tf.remove(role_to_remove)
            selected_wlz.append('落难少女')
            special_notes.append("注意：由于巡山人在场，一个村民已变成落难少女")
    
    if '失忆者' in selected_tf:
        available_role = [role for role in tf_list if role not in selected_tf and role not in ['失忆者', '气球驾驶员', '巡山人', '农夫', '罂粟种植者']]
        true_role = random.choice(available_role)
        selected_tf[selected_tf.index('失忆者')] = f'失忆者({true_role})'
        checkpoint = True
    else: 
        true_role = None
        checkpoint = False
        
    if '酒鬼' in selected_wlz:
        available_role = [role for role in tf_list if role not in selected_tf and role not in ['失忆者', '农夫'] and role != true_role]
        disguise = get_drunk_disguise(available_role)
        selected_wlz[selected_wlz.index('酒鬼')] = f'酒鬼({disguise})'
    else:
        disguise = None
      
            
    # Add Bone Demon note if present
    if '亡骨魔' in selected_demon:
        special_notes.append("注意：由于亡骨魔在场，一个外来者已变成村民")
    
    final_roles = selected_tf + selected_wlz + selected_minion + selected_demon
    random.shuffle(final_roles)
    
    # Calculate absent roles
    all_possible_roles = tf_list + wlz_list + minion_list + demon_list
    absent_roles = [role for role in all_possible_roles if role != disguise and role != true_role and role not in [r.split('(')[0] for r in final_roles]]
 
    # Print role summary
    final_tf_count = sum(1 for role in final_roles if role.split('(')[0] in tf_list)
    final_wlz_count = sum(1 for role in final_roles if role.split('(')[0] in wlz_list)
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

    valid_roles = [role for role in absent_roles if role not in demon_list and role not in minion_list and role != disguise and role not in ['酒鬼', '失忆者']]
    disguisers = random.sample(valid_roles, 3)

    return final_roles, special_notes, disguisers, true_role


def evaluate_teams(roles, true_role, tf_list, tf_strength, wlz_list, wlz_strength, minion_list, minion_strength, demon_list, demon_strength):
    # Calculate team scores
    score = [0] * 4
    for i in range(len(tf_list)):
        if tf_list[i] in roles:
            score[0] += tf_strength[tf_list[i]]
    if true_role is not None:
        score[0] += tf_strength[true_role] / 2
    for i in range(len(wlz_list)):
        if wlz_list[i] in roles:
            score[1] += wlz_strength[wlz_list[i]]
    for i in range(len(minion_list)):
        if minion_list[i] in roles:
            score[2] += minion_strength[minion_list[i]]
    for i in range(len(demon_list)):
        if demon_list[i] in roles:
            score[3] += demon_strength[demon_list[i]]
    
    blue_strength = score[0] + score[1]  # 蓝方实力
    red_strength = score[2] + score[3]   # 红方实力

    return blue_strength, red_strength


# Define role lists
tf_list = ['贵族', '舞蛇人', '气球驾驶员', '巡山人', '工程师', '渔夫', '教授', '博学者', '失忆者', '农夫', '食人族', '罂粟种植者']
wlz_list = ['酒鬼', '落难少女', '理发师', '魔像']
minion_list = ['投毒者', '灵言师', '精神病患者', '麻脸巫婆']
demon_list = ['哈迪寂亚', '亡骨魔']

tf_strength = {'贵族': 3, '舞蛇人': 3, '气球驾驶员': 5, '巡山人': 1, '工程师': 5, '渔夫': 3, '教授': 3, '博学者': 4, '农夫': 0, '食人族': 2, '罂粟种植者': 5}
wlz_strength = {'酒鬼': 0, '落难少女': -2, '理发师': -1, '魔像': 2}
minion_strength = {'投毒者': 5, '灵言师': 3, '精神病患者': 6, '麻脸巫婆': 7}
demon_strength = {'哈迪寂亚': 8, '亡骨魔': 2}


# Player count configurations
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
    blue_strength = 999
    red_strength = 0

    while 0.8 * blue_strength > red_strength or 0.8 * red_strength > blue_strength:
        os.system('clear')        
        roles, special_notes, disguisers, true_role = distribute_roles(num_players)
        blue_strength, red_strength = evaluate_teams(roles, true_role, tf_list, tf_strength, wlz_list, wlz_strength, minion_list, minion_strength, demon_list, demon_strength)
    
except Exception as e:
    print(f"发生错误: {e}")


# Display the final result
print(f"\n随机分配的{num_players}个角色:")
for i, role in enumerate(roles, 1):
    print(f"{i}. {role}")

with open('1_roles.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    for i, role in enumerate(roles, 1):
        writer.writerow(["正常", "可用", i, role])

if special_notes:
    print("\n特殊规则说明：")
    for note in special_notes:
        print(f"- {note}")

print(f"\n红方阵营的伪装身份是：{disguisers[0]}, {disguisers[1]}, {disguisers[2]}\n")
print(f"蓝方实力：{blue_strength}, 红方实力：{red_strength}")
