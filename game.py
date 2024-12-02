import csv
import re
import random

night = input('这是第几晚？')

with open(night + '_roles.csv', mode='r', encoding='utf-8') as file:
    reader = csv.reader(file)
    data = list(reader)

if night != '1':
    with open(str(int(night)-1)+'_lynch.csv', mode='r', encoding='utf-8') as file:
        reader = list(csv.reader(file))
        if len(reader) == 0 or (len(reader) == 1 and all(cell == '' for cell in reader[0])):
            lynched = None
        else:
            lynched = list(reader)[0]


tf_list = ['祖母', '水手', '侍女', '驱魔人', '旅店老板', '赌徒', '造谣者', '侍臣', '教授', '吟游诗人', '茶艺师', '和平主义者', '弄臣']
wlz_list = ['莽夫', '修补匠', '疯子', '月之子']
minion_list = ['教父', '刺客', '魔鬼代言人', '主谋']
demon_list = ['僵怖', '沙巴洛斯', '普卡', '珀']

sn_info = [False] * len(data)
qmr_bool = False
death_list = []
kill_list= []
reborn_list = []

def get_index(role):
    for index, row in enumerate(data):
        if row[-1] == role:
            return int(index)
    return None

#教父能力
def get_wlz():
    wlz_avail = []
    for index, row in enumerate(data):
        if row[-1] in wlz_list:
            wlz_avail.append(row[-1])
    return '、'.join(wlz_avail)

#检查醉酒
def check_dizzy(role):
    if '醉' not in data[get_index(role)][1] and '毒' not in data[get_index(role)][1]:
        return False
    else:
        return True

#确保不覆盖长久醉酒        
def check_dizzy_priority(index):
    if index is not None:
        return data[index][1] != '醉02' and data[index][1] != '醉03' and data[index][1] != '毒卡'
    return False

#检查莽夫能力发动
def check_mf(index, role):
    if data[index][-1] == '莽夫' and data[index][2] != '不可':
        data[index][2] = '不可'
        if not check_dizzy('莽夫'):
            if role in tf_list or role in wlz_list:
                mf = input(' - 莽夫现在属于善良阵营！')
                if '莽夫' in minion_list:
                    minion_list.remove('莽夫')
                    wlz_list.append('莽夫')
            elif role in minion_list or role in demon_list:
                mf = input(' - 莽夫现在属于邪恶阵营！')
                if '莽夫' in wlz_list:
                    wlz_list.remove('莽夫')
                    minion_list.append('莽夫')
            if check_dizzy_priority(index):
                role_index = get_index(role)
                if role_index is not None:
                    data[role_index][1] = '醉01'
                    return data[role_index][1]
    return None

#检查在场并且生存
def check_alive(role):
    if get_index(role) != None and data[get_index(role)][0] != '死亡' and data[get_index(role)][0] != '沙巴': 
        return True
    else:
        return False

#检查是否可杀
def check_killable(index):
    #if data[index][0] != '无敌' or data[index][0] != '不杀' or (data[index][0] == '无敌' and '醉' in data[index][1]) or (data[index][0] == '无敌' and '毒' in data[index][1]):
    if (data[index][0] != '无敌' and data[index][0] != '不杀') or (data[index][0] == '无敌' and ('醉' in data[index][1] or '毒' in data[index][1])):
        return True
    else:
        False

#检查弄臣的护身符
def check_amulet(index):
    if data[index][-1] == '弄臣' and data[index][2] == '可用' and not check_dizzy('弄臣'):
        return True
    else:
        return False
    
#玩家状态从白天恢复
for index, row in enumerate(data):
    if data[index][0] in ['无敌', '不处', '不杀']:
        if data[index][-1] == '僵怖' and data[index][2] == '不可':
            data[index][0] = '假死'
        else:
            data[index][0] = '存活'

        
    if data[index][1] in ['醉01', '毒01']:
        data[index][1] = '正常'
        
    elif data[index][1] == '醉02':
        data[index][1] = '醉01'

    elif data[index][1] == '醉03':
        data[index][1] = '醉02'

#重置莽夫技能
if get_index('莽夫') is not None:
    data[get_index('莽夫')][2] = '可用'
    
print("读取的角色信息:")
for row in data:
    print(f"{row[0]}, {row[1]}, {row[2]}, {row[3]}, {row[4]}")



print('\n')
 


### 不处=不会被处决； 不杀=晚上不会被杀死；无敌=不会死
if check_alive('茶艺师'):
    if not check_dizzy('茶艺师'):
        data_length = len(data)
        tea_index = get_index('茶艺师')
        
        for i in range(1, 15):
            prev_index = (tea_index - i) % data_length
            if prev_index == 0:
                continue
            if data[prev_index][0] != '死亡' and data[prev_index][0] != '垂死' and data[prev_index][0] != '假死':
                break

        for j in range(1, 15):
            next_index = (tea_index + j) % data_length
            if next_index == 0:
                continue
            if data[next_index][0] != '死亡' and data[next_index][0] != '垂死' and data[prev_index][0] != '假死':
                break
        
        if (data[prev_index][-1] not in demon_list and 
            data[prev_index][-1] not in minion_list and 
            data[next_index][-1] not in demon_list and 
            data[next_index][-1] not in minion_list):
                
            data[prev_index][0] = '无敌'
            data[next_index][0] = '无敌'
            
    
if night == '1': 
    if check_alive('疯子'):
        fz = input(f'（说书人）{get_index("疯子")}号疯子在场哦，记得要建两个群！')
    
    if check_alive('水手'):
        sn_info[get_index('水手')] = True
        data[get_index('水手')][0] = '无敌'
        ss = input(f'{get_index("水手")}号水手选择和谁喝酒？')
        check_mf(int(ss), '水手')
        ss_who = input(' - （说书人）选择让谁醉酒？')
        if check_dizzy_priority(int(ss_who)):
            data[int(ss_who)][1] = '醉01'
        
        
    if check_alive('侍臣'):  
        sn_info[get_index('侍臣')] = True
        sc = input(f'{get_index("侍臣")}号侍臣要选择身份吗？(y/n) ')
        if sc == 'y':
            data[get_index('侍臣')][2] = '不可'
            sc_who = input(' - 选择哪个身份呢？')
            if get_index(sc_who) != None:
                check_mf(get_index(sc_who), '侍臣')
                if not check_dizzy('侍臣'):
                    data[get_index(sc_who)][1] = '醉03'
        
            
    if check_alive('教父'):
        sn_info[get_index('教父')] = True
        if not check_dizzy('教父'):
            jf = input(f'（说书人）告诉{get_index("教父")}号教父外来者是{get_wlz()}！')
        else:
            jf = input(f'（说书人）告诉{get_index("教父")}号教父外来者是除{get_wlz()}以外的身份！')
        
        
    if check_alive('魔鬼代言人'):
        sn_info[get_index('魔鬼代言人')] = True
        mgdyr = input(f'{get_index("魔鬼代言人")}号魔鬼代言人选择守谁？')
        check_mf(int(mgdyr), '魔鬼代言人')
        if not check_dizzy('魔鬼代言人'):
            data[int(mgdyr)][0] = '不处'
        
        
    if check_alive('普卡'):
        sn_info[get_index('普卡')] = True
        pk = input(f'{get_index("普卡")}号普卡选择毒谁？')
        check_mf(int(pk), '普卡')
        if not check_dizzy('普卡'):
            data[int(pk)][1] = '毒卡'
        
     
    if check_alive('祖母'):
        sn_info[get_index('祖母')] = True
        granny = input(f'（说书人）告诉{get_index("祖母")}号祖母孙子/孙女是几号？')
        if not check_dizzy('祖母'):
            granny_who = input(' - （说书人）告诉祖母正确信息！')
        else:
            granny_who = input(' - （说书人）告诉祖母错误信息！')
        data[get_index('祖母')][-1] = f"{data[get_index('祖母')][-1]}{int(granny)}"
        
        
    if check_alive('侍女'):
        sn_info[get_index('侍女')] = True
        sn = input(f'{get_index("侍女")}号侍女选择哪两位玩家？').split()
        check_mf(int(sn[0]), '侍女')
        check_mf(int(sn[1]), '侍女')
        indices = [int(index) for index in sn]
        true_count = sum(sn_info[i] for i in indices)
        if not check_dizzy('侍女'):
            sn_result = input(f' - 侍女的信息是：{true_count}')
        else:
            sn_result_fake = random.choice([x for x in [0, 1, 2] if x not in true_count])
            sn_result = input(f' - 侍女的信息是：{sn_result_fake}')

else:
    if check_alive('水手'):
        sn_info[get_index('水手')] = True
        ss = input(f'{get_index("水手")}号水手选择和谁喝酒？')
        check_mf(int(ss), '水手')
        if not check_dizzy('水手'):
            data[get_index('水手')][0] = '无敌'            
            ss_who = input(' - （说书人）选择让谁醉酒？')
            if check_dizzy_priority(int(ss_who)):
                data[int(ss_who)][1] = '醉01'
        
        
    if check_alive('旅店老板'):
        sn_info[get_index('旅店老板')] = True
        ldlb = input(f'{get_index("旅店老板")}号旅店老板选择保护哪两位玩家？').split()
        ldlb = [int(i) for i in ldlb]
        check_mf(ldlb[0], '旅店老板')
        check_mf(ldlb[1], '旅店老板')
        if not check_dizzy('旅店老板'):
            for i in range(len(ldlb)):
                data[ldlb[i]][0] = '不杀'
            ldlb_dizzy = input(' - （说书人）选择让谁醉酒？')
            if check_dizzy_priority(int(ldlb_dizzy)):
                data[int(ldlb_dizzy)][1] = '醉01'
        
        
    if check_alive('侍臣') and data[get_index('侍臣')][2] != '不可':  
        sn_info[get_index('侍臣')] = True
        sc = input(f'{get_index("侍臣")}号侍臣要选择身份吗？(y/n) ')
        if sc == 'y':
            data[get_index('侍臣')][2] = '不可'
            sc_who = input(' - 选择哪个身份呢？')
            if get_index(sc_who) != None:
                check_mf(get_index(sc_who), '侍臣')
                if not check_dizzy('侍臣'):
                    data[get_index(sc_who)][1] = '醉03'
        

    if check_alive('赌徒'):
        sn_info[get_index('赌徒')] = True
        dt = input(f'{get_index("赌徒")}号赌徒猜对了吗？(y/n) ')
        if dt != 'y':
            if not check_dizzy('赌徒'):
                data[get_index('赌徒')][0] = '死亡'
                death_list.append(get_index('赌徒'))
        
        
    if check_alive('魔鬼代言人'):
        sn_info[get_index('魔鬼代言人')] = True
        mgdyr = input(f'{get_index("魔鬼代言人")}号魔鬼代言人选择守谁？')
        check_mf(int(mgdyr), '魔鬼代言人')
        if not check_dizzy('魔鬼代言人'):
            data[int(mgdyr)][0] = '不处'
            

    if check_alive('疯子'):
        sn_info[get_index('疯子')] = True
        fz = input(f'{get_index("疯子")}号疯子选择目标：')
        fz_tell_demon = input(' - （说书人）告诉真恶魔疯子选了谁哦！')
        
        
    if check_alive('驱魔人'):
        sn_info[get_index('驱魔人')] = True
        qmr = input(f'{get_index("驱魔人")}号驱魔人选择驱谁？')
        check_mf(int(qmr), '驱魔人')
        if not check_dizzy('驱魔人'):
            if data[int(qmr)][-1] in demon_list:
                qmr_yes = input(' - （说书人）告诉恶魔他被驱魔了！')
                qmr_bool = True
        
            
    if check_alive('僵怖'):
        if lynched == None:
            if not qmr_bool:
                sn_info[get_index('僵怖')] = True
                zombie = input(f'{get_index("僵怖")}号僵怖选择要杀死的玩家：')
                check_mf(int(zombie), '僵怖')
                if not check_dizzy('僵怖'):
                    if check_killable(int(zombie)):
                        if check_amulet(int(zombie)):
                            data[int(zombie)][2] = '不可'
                        else:
                            data[int(zombie)][0] = '死亡'
                            death_list.append(int(zombie))
                            kill_list.append(int(zombie))


    if check_alive('普卡'):
        if not qmr_bool:
            sn_info[get_index('普卡')] = True
            for index, row in enumerate(data):
                if row[1] == '毒卡':
                    if check_killable(index):
                        if check_amulet(index):
                            row[2] = '不可'
                            row[1] = '正常'
                        else:
                            row[0] = '死亡'
                            row[1] = '正常'
                            death_list.append(index)
                            kill_list.append(index)
            pk = input(f'{get_index("普卡")}号普卡选择毒谁？')
            if not check_dizzy('普卡'):
                data[int(pk)][1] = '毒卡'
        
     
    if check_alive('沙巴洛斯'):
        if not qmr_bool:
            sn_info[get_index('沙巴洛斯')] = True
            sbls = input(f'{get_index("沙巴洛斯")}号沙巴洛斯选择杀哪两人？').split()
            sbls = [int(i) for i in sbls]
            check_mf(sbls[0], '沙巴洛斯')
            check_mf(sbls[1], '沙巴洛斯')
            if not check_dizzy('沙巴洛斯'):
                for index, row in enumerate(data):
                    if row[0] == '沙巴':
                        reborn = input(f'（说书人）要让{index}号玩家被反刍吗？(y/n) ')
                        if reborn == 'y':
                            row[0] = '存活'
                            reborn_list.append(index)
                        else:
                            if check_amulet(index):
                                row[2] = '不可'
                            else:
                                row[0] = '死亡'
                for i in range(len(sbls)):
                    if check_killable(sbls[i]):
                        if check_amulet(sbls[i]):
                            data[sbls[i]][2] = '不可'
                        else:
                            data[sbls[i]][0] = '沙巴'
                        death_list.append(sbls[i])
                        kill_list.append(sbls[i])
            elif check_dizzy('沙巴洛斯'):
                for index, row in enumerate(data):
                    if row[0] == '沙巴':
                        row[0] = '死亡'
                

    if check_alive('珀'):
        if not qmr_bool:
            sn_info[get_index('珀')] = True
            if data[get_index('珀')][2] != '不可':
                po = input(f'{get_index("珀")}号珀选择杀几个人(0-1)？')
                if po == '0':
                    data[get_index('珀')][2] = '不可'
                elif po == '1':
                    po_kill = input(' - 选择杀谁？')
                    check_mf(int(po_kill), '珀')
                    if not check_dizzy('珀'):
                        if check_killable(int(po_kill)):
                            if check_amulet(int(po_kill)):
                                data[int(po_kill)][2] = '不可'
                            else:
                                data[int(po_kill)][0] = '死亡'
                                death_list.append(int(po_kill))
                                kill_list.append(int(po_kill))
            elif data[get_index('珀')][2] == '不可':
                data[get_index('珀')][2] = '可用'
                po_kill = input(f'{get_index("珀")}号珀选择杀哪三人？').split()
                po_kill = [int(i) for i in po_kill]
                check_mf(int(po_kill[0]), '珀')
                check_mf(int(po_kill[1]), '珀')
                check_mf(int(po_kill[2]), '珀')
                if not check_dizzy('珀'):
                    for i in range(len(po_kill)):
                        if check_killable(int(po_kill[i])):
                            if check_amulet(int(po_kill[i])):
                                data[int(po_kill[i])][2] = '不可'
                            else:
                                data[int(po_kill[i])][0] = '死亡'
                                death_list.append(int(po_kill[i]))
                                kill_list.append(int(po_kill[i]))

                    
    if check_alive('刺客') and data[get_index('刺客')][2] != '不可':
        sn_info[get_index('刺客')] = True
        ck = input(f'{get_index("刺客")}号刺客想要杀人吗？(y/n) ')
        if ck == 'y':
            ck_who = input(' - 选择刺杀谁？')
            if not check_dizzy('刺客'):
                data[int(ck_who)][0] = '死亡'
                death_list.append(int(ck_who))
            data[get_index('刺客')][2] = '不可'
            
    if check_alive('教父'):
        if lynched != None:
            if lynched[-1] in wlz_list:
                sn_info[get_index('教父')] = True
                godfather = input(f'{get_index("教父")}号教父选择要杀的人：')
                if not check_dizzy('教父'):
                    if check_killable(int(godfather)):
                        if check_amulet(int(godfather)):
                            data[int(godfather)][2] = '不可'
                        else:
                            data[int(godfather)][0] = '死亡'
                            death_list.append(int(godfather))
    
            
    if check_alive('教授') and data[get_index('教授')][2] != '不可':
        sn_info[get_index('教授')] = True
        prof = input(f'{get_index("教授")}号教授今天要复活人吗？(y/n) ')
        if prof == 'y':
            prof_who = input(f' - 他要复活谁？')
            data[get_index('教授')][2] = '不可'
            if not check_dizzy('教授'):
                data[int(prof_who)][0] = '存活'
                data[int(prof_who)][2] = '可用'
                reborn_list.append(int(prof_who))
                
    if check_alive('造谣者'):
        zyz = input(f'{get_index("造谣者")}号造谣者白天的谣言正确吗？(y/n) ')
        if zyz == 'y':
            if not check_dizzy('造谣者'):
                zyz_who = input(' - （说书人）选择让谁死？')
                data[int(zyz_who)][0] = '死亡'
                death_list.append(int(zyz_who))
            
    if check_alive('修补匠'):
        tinker = input(f'（说书人）{get_index("修补匠")}号修补匠今天让他活吗？(注意一下修补匠醉毒状态以及邻座有没有茶艺师)(y/n) ')
        if tinker != 'y':
            if not check_dizzy('修补匠'):
                data[get_index('修补匠')][0] = '死亡'
                death_list.append(get_index('修补匠'))
            
    if get_index('月之子') != None and data[get_index('月之子')][0] == '垂死':
        yzz = input(f'（说书人）{get_index("月之子")}号月之子选的是几号玩家？')
        if not check_dizzy('月之子'):
            if check_killable(int(yzz)):
                if check_killable(int(yzz)):
                    if check_amulet(int(yzz)):
                        data[int(yzz)][2] = '不可'
                    else:
                        if data[int(yzz)][-1] in [tf_list, wlz_list]:
                            data[int(yzz)][0] = '死亡'
                            death_list.append(int(yzz))
        data[get_index('月之子')][0] = '死亡'
        
    number = 99
    for index, row in enumerate(data):
        joined_row = ''.join(row)
        if '祖母' in joined_row:
            match = re.search(r'祖母(\d+)', joined_row)
            if match:
                number = match.group(1)
            R = row
            I = index
    if int(number) in kill_list:
        if not check_dizzy(R[-1]):
            data[I][0] = '死亡'
            death_list.append(I)
            
            
    if check_alive('侍女'):
        sn_info[get_index('侍女')] = True
        sn = input(f'{get_index("侍女")}号侍女选择哪两位玩家？').split()
        indices = [int(index) for index in sn]
        true_count = sum(sn_info[i] for i in indices)
        if not check_dizzy('侍女'):
            sn_result = input(f' - 侍女的信息是：{true_count}')
        else:
            sn_result_fake = random.choice([x for x in range(3) if x != true_count])
            sn_result = input(f' - 侍女的信息是：{sn_result_fake}')
             


if get_index('月之子') in death_list:
    data[get_index('月之子')][0] = '垂死'

print("\n更新后的角色信息:")
for row in data:
    print(', '.join(row))

print('\n')
print('今晚死亡的玩家是：', death_list)
print('今晚复活的玩家是：', reborn_list)



if check_alive('和平主义者') and not check_dizzy('和平主义者'):
    double_check = input(f'（说书人）{get_index("和平主义者")}号和平主义者在场哦！考虑一下处决是否有效！')
lynch = input('（说书人）有人被处决了？(y/n) ')
if lynch == 'y':
    who_lynch = input(' - 谁被处决了？')
    if data[int(who_lynch)][-1] == '弄臣' and data[int(who_lynch)][2] != '不可':
        data[int(who_lynch)][2] = '不可'
        lynch = 'n'
        a = input('今晚没有人被处决！')
    elif data[int(who_lynch)][0] not in ['不处', '无敌']:
        if data[int(who_lynch)][-1] not in ['月之子', '僵怖']:
            data[int(who_lynch)][0] = '死亡'
        elif data[int(who_lynch)][-1] == '月之子':
            data[int(who_lynch)][0] = '垂死'
        elif data[int(who_lynch)][-1] == '僵怖':
            if data[int(who_lynch)][0] == '假死':
                data[int(who_lynch)][0] = '死亡'
            else:
                data[int(who_lynch)][0] = '假死'
                data[int(who_lynch)][2] = '不可'
        a = input(f'今晚被处决的玩家是：{int(who_lynch)}')
        if data[int(who_lynch)][-1] in demon_list and data[int(who_lynch)][0] == '死亡':
            if check_alive('主谋'):
                b = input('恶魔死亡！进入主谋日！')
            else:
                b = input('游戏结束！善良阵营获胜！')
        
        if check_alive('吟游诗人') and data[int(who_lynch)][-1] in minion_list and not check_dizzy('吟游诗人'):
            for i in range(1, len(data)):
                if data[i][1] == '正常' or data[i][1] == '醉01':
                    data[i][1] = '醉02'
    else:
        lynch = 'n'
        a = input('今晚没有人被处决！')
else:
    
    a = input('今晚没有人被处决！')



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
        writer.writerow(data[int(who_lynch)])
else:
    with open(f"{int(night)}_lynch.csv", mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow('')
        
        