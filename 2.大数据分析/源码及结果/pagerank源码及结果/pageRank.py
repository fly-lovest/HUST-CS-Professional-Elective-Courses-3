import numpy as np

if __name__ == '__main__':
    fileread = open("sent_receive.csv", 'r')
    next(fileread)
    edges_dict = {}
    nodes = []
    for line in fileread:
        line = line.strip()
        num, sent_node, receive_node = line.split(',', 2)
        if (sent_node, receive_node) not in edges_dict.items():
            edges_dict[sent_node] = receive_node
        if sent_node not in nodes:
            nodes.append(sent_node)
        if receive_node not in nodes:
            nodes.append(receive_node)
    print(nodes)  # nodes里为各结点
    print(edges_dict)  # edges_dict里为存在的有向边

    # 创建矩阵M
    N = len(nodes)
    M = np.zeros((N, N))
    for (sent, receive) in edges_dict.items():
        edge_out = nodes.index(sent)
        edge_in = nodes.index(receive)
        M[edge_in, edge_out] = 1

    # 矩阵归一化
    for col in range(N):
        sum_col = sum(M[:, col])
        if sum_col != 0:
            for row in range(N):
                M[row, col] = M[row, col]/sum_col
    print("归一化初始矩阵：\n", M)
    r = np.ones((N, 1))/N
    r_next = np.zeros((N, 1))
    M_1ofN = np.ones((N, N))
    beta = 0.85
    Er = 0.00000001
    er_now = 1.0
    A = beta * M + (1 - beta) * M_1ofN
    k = 0

    while er_now > Er:   # 迭代计算
        r_next = np.dot(A, r)
        sum_col = sum(r_next)
        r_next = r_next / sum_col
        er_now = r_next - r
        er_now = abs(er_now)
        er_now = sum(er_now)
        print(er_now)
        r = r_next
        k += 1

    print("最终矩阵：\n", r, k)

