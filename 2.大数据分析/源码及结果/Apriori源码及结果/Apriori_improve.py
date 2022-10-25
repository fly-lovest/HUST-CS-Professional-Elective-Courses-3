import pandas as pd

def L_print(filename, support_items):
    file_L = open(filename, 'w')
    file_L.write('{},\t{}\n'.format("frequent-itemsets", "support"))
    for l in support_items:
        file_L.write('{},\t{}\n'.format(list(l), support_items[l]))
    file_L.write('total:{}'.format(len(support_items)))
    print('{} Done\n'.format(filename))


def rule_print(filename, rule_list):
    file_rule = open(filename, 'w')
    file_rule.write("-------------rule-------------\n")
    for r in rule_list:
        file_rule.write('{} ==> {}: {}\n'.format(list(r[0]), list(r[1]), r[2]))
    file_rule.write('total:{}'.format(len(rule_list)))
    print('ALL Done\n')

def create_C1(items):
    C1 = set()
    for item in items:
        for good in item:
            if good not in C1:
                good_set = frozenset([good])
                C1.add(good_set)
    return C1


def filter(items, Ck, min_support, support_items, itemsNum):
    Lk = set()
    item_counter = {}
    for item in items:
        for c in Ck:
            if c.issubset(item):
                if c not in item_counter:
                    item_counter[c] = 1
                else:
                    item_counter[c] += 1
    for c in item_counter:
        if item_counter[c] / itemsNum >= min_support:
            Lk.add(c)
            support_items[c] = item_counter[c] / itemsNum
    return Lk


def is_k_sub_Apriori(temp_item, Lk):
    for item in temp_item:
        sub_item = temp_item - frozenset([item])
        if sub_item not in Lk:
            return False
    return True


def constructor(Lk, k, len_Lk):
    Ck1 = set()
    list_Lk = list(Lk)
    list_Lk.sort()
    for i in range(len_Lk):
        for j in range(i+1, len_Lk):
            # 连接策略：Apriori算法假定项集中的项按照字典序排序。
            # 定理：如果Lk中某两个的元素（项集）itemset1和itemset2的前(k-1)个项是相同的，
            # 则称itemset1和itemset2是可连接的。
            itemset1 = list(list_Lk[i])[0:k - 1]
            itemset2 = list(list_Lk[j])[0:k - 1]
            if itemset1 == itemset2:
                Ck1_temp_item = list_Lk[i] | list_Lk[j]
                # 剪枝策略：任何非频繁的(k-1)项集都不是频繁k项集的子集。
                # 若上述Ck1_temp_item中的存在k项子集不在Lk内，则将Ck1_temp_item剪掉
                if is_k_sub_Apriori(Ck1_temp_item, Lk):
                    Ck1.add(Ck1_temp_item)
    return Ck1


def creat_rule(L1, L2, L3, support_items_L1, support_items_L2, support_items_L3, min_confidence):
    rule_list = []
    # 寻找3阶项集中的关联规则
    for itemk3 in L3:
        for itemk2 in L2:
            if itemk2.issubset(itemk3):
                conf = support_items_L3[itemk3] / support_items_L2[itemk2]
                rule = [itemk2, itemk3-itemk2, conf]
                if conf >= min_confidence and rule not in rule_list:
                    rule_list.append(rule)
        for itemk1 in L1:
            if itemk1.issubset(itemk3):
                conf = support_items_L3[itemk3] / support_items_L1[itemk1]
                rule = [itemk1, itemk3-itemk1, conf]
                if conf >= min_confidence and rule not in rule_list:
                    rule_list.append(rule)
    # 寻找2阶项集中的关联规则
    for itemk2 in L2:
        for itemk1 in L1:
            if itemk1.issubset(itemk2):
                conf = support_items_L2[itemk2] / support_items_L1[itemk1]
                rule = [itemk1, itemk2-itemk1, conf]
                if conf >= min_confidence and rule not in rule_list:
                    rule_list.append(rule)
    return rule_list

if __name__ == "__main__":
    min_support = 0.005
    min_confidence = 0.5
    data = pd.read_csv("Groceries.csv")
    # 处理数据
    data_item = data['items']
    list_item = data_item.values.tolist()
    final_list = []
    for item in list_item:
        item = item.strip('{').strip('}').split(',')
        goods = []
        for good in item:
            goods.append(good)
        final_list.append(goods)
    items = final_list
    items_num = float(len(items))
    support_items_L1 = {}
    support_items_L2 = {}
    support_items_L3 = {}
    # C1和L1创建过程
    C1 = create_C1(items)
    L1 = filter(items, C1, min_support, support_items_L1, items_num)
    L_print("L1.txt", support_items_L1)
    # C2和L2创建过程
    C2 = constructor(L1, 1, len(L1))
    L2 = filter(items, C2, min_support, support_items_L2, items_num)
    L_print("L2.txt", support_items_L2)
    # C3和L3创建过程
    C3 = constructor(L2, 2, len(L2))
    L3 = filter(items, C3, min_support, support_items_L3, items_num)
    L_print("L3.txt", support_items_L3)
    # 生成关联规则
    list_rule = creat_rule(L1, L2, L3, support_items_L1, support_items_L2, support_items_L3, min_confidence)
    rule_print("rule.txt", list_rule)

