import numpy as np
import pandas as pd


def getdata(filename):
    fileread = open(filename, 'r')
    next(fileread)
    data = []
    users = []
    movies = []
    for line in fileread:
        userid, movieid, rating, timestamp = line.strip().split(',')
        data.append([int(userid), int(movieid), float(rating)])
    for item in data:
        if item[0] not in users:
            users.append(item[0])
        if item[1] not in movies:
            movies.append(item[1])
    user2movie = np.zeros([len(users), len(movies)])
    # 构造用户-电影效用矩阵
    for item in data:
        user2movie[item[0]-1, movies.index(item[1])] = item[2]
    return data, user2movie, len(users), len(movies), movies


def get_k_neighbors(userid, k, user2user, len):
    # userneighbors的形式为[(index, sim),...]
    row = userid - 1
    userneighbors = {}
    for col in range(len):
        if col != row:
            userneighbors[col] = user2user[row, col]
    userneighbors = list(sorted(userneighbors.items(), key=lambda item: item[1], reverse=True))
    return userneighbors[:k]


def recommendation_n_movie(userid, user2movie, user2user, knebs, k, n, lenmovies):
    # 只记录电影序列号
    recom_movies = []  # 记录待推荐电影，即该用户没看的电影的序列[[0, index],...]
    rate_movies = []  # 记录用户已经看的电影打分和序列号[[rate,index], [...], [...]]
    usersum = 0
    row = userid -1
    for col in range(lenmovies):
        if user2movie[row, col] > 0:
            rate_movies.append([user2movie[row, col], col])
            usersum += user2movie[row, col]
        else:
            recom_movies.append([0.0, col])
    div_userrate = usersum / len(rate_movies)
    knebssum = np.zeros(k)
    knebsratenum = np.zeros(k)
    userksimsum = 0
    for i in range(k):
        krow = knebs[i][0]
        userksimsum += user2user[row, krow]
        for j in range(lenmovies):
            if user2movie[krow, j] > 0:
                knebsratenum[i] += 1
                knebssum[i] += user2movie[krow, j]
            # 在此对0不做计算
    for i in range(len(recom_movies)):
        index = recom_movies[i][1]
        temp = 0
        for j in range(k):
            krow = knebs[j][0]
            if user2movie[krow, index] != 0:
                temp += knebs[j][1] * (user2movie[krow, index] - knebssum[j] / knebsratenum[j])
        recom_movies[i][0] = div_userrate + temp / userksimsum
    recom_movies.sort(reverse=True)
    return recom_movies[:n]


def get_movie(filename):
    data = pd.read_csv(filename)
    col_moiveid = data['movieId']
    col_movietitle = data['title']
    col_genres = data['genres']
    movies_title = {}
    movies_genres = {}
    i = 0
    for title in col_movietitle:
        movies_title[int(col_moiveid[i])] = title
        i += 1
    i = 0
    for genres in col_genres:
        movies_genres[int(col_moiveid[i])] = genres
        i += 1
    return movies_title, movies_genres


def recom_test_movie(userid, movieid_index1, movieid_index2, user2movie, user2user, knebs, k, lenmovies):
    recom_movies = [[0.0, movieid_index1], [0.0, movieid_index2]]
    rate_movies = []
    usersum = 0
    row = userid - 1
    for col in range(lenmovies):
        if user2movie[row, col] > 0:
            rate_movies.append([user2movie[row, col], col])
            usersum += user2movie[row, col]
    div_userrate = usersum / len(rate_movies)
    knebssum = np.zeros(k)
    knebsratenum = np.zeros(k)
    userksimsum = 0
    for i in range(k):
        krow = knebs[i][0]
        userksimsum += user2user[row, krow]
        for j in range(lenmovies):
            if user2movie[krow, j] > 0:
                knebsratenum[i] += 1
                knebssum[i] += user2movie[krow, j]
            # 在此对0不做计算
    for i in range(len(recom_movies)):
        index = recom_movies[i][1]
        temp = 0
        for j in range(k):
            krow = knebs[j][0]
            if user2movie[krow, index] != 0:
                temp += knebs[j][1] * (user2movie[krow, index] - knebssum[j] / knebsratenum[j])
        recom_movies[i][0] = div_userrate + temp / userksimsum
    return recom_movies

if __name__ == '__main__':
    data, user2movie, lenusers, lenmovies, movies = getdata("train_set.csv")
    user2user = np.corrcoef(user2movie)  # 获得pearson相似度矩阵
    My_userid = 29  # 选取推荐用户
    k = 30  # 相似邻居数
    n = 10  # 推荐电影数
    knebs = get_k_neighbors(My_userid, k, user2user, lenusers)  # 获取最相似的k个邻居
    recom_n_movie = recommendation_n_movie(My_userid, user2movie, user2user, knebs, k, n, lenmovies)
    movies_title, movies_genres = get_movie("movies.csv")
    for i in range(n):
        index = recom_n_movie[i][1]
        index = movies[index]
        print("{} {} {}".format(i+1, movies_title[index], movies_genres[index]))

    test_data = pd.read_csv('test_set.csv')
    usersid = test_data['userId']
    movieid = test_data['movieId']
    rating = test_data['rating']
    sse = 0
    for i in range(int(len(usersid)/2)):
        knebs = get_k_neighbors(usersid[i*2], 30, user2user, lenusers)  # 获取最相似的k个邻居
        movieid_index1 = movies.index(int(movieid[i*2]))
        movieid_index2 = movies.index(int(movieid[i*2+1]))
        test_rating_list = recom_test_movie(usersid[i*2], movieid_index1, movieid_index2, user2movie, user2user, knebs, 30, lenmovies)
        print("{},{}".format(usersid[i*2], test_rating_list[0][0]))
        print("{},{}".format(usersid[i*2+1], test_rating_list[1][0]))
        sse += pow(test_rating_list[0][0]-float(rating[i*2]), 2)
        sse += pow(test_rating_list[1][0] - float(rating[i*2+1]), 2)
    print("sse:", sse)

