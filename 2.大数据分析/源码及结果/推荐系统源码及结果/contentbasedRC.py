import numpy as np
import pandas as pd
import math
from sklearn.metrics.pairwise import cosine_similarity


def get_data(filename):
    data = pd.read_csv(filename)
    col_movieid = data['movieId']
    col_title = data['title']
    col_genres = data['genres']
    genres = []
    movies = []
    movie_title = []  # 形式为[['title'],[]]
    movie_genres = []  # 形式为[['genre','genre',...], ...]
    for id in col_movieid:
        movies.append(int(id))
    for title in col_title:
        movie_title.append(title)
    for line in col_genres:
        line = line.strip().split('|')
        movie_genres.append(line)
        for genre in line:
            if genre not in genres:
                genres.append(genre)
    return movie_title, movie_genres, movies, genres


# 构造TF_IDF特征矩阵
def get_TF_IDF(lenmoive, lengenres, movie_genres, genres):
    TF_IDF = np.zeros((lenmoive, lengenres))
    genresnum = np.zeros(lengenres)
    for i in range(lenmoive):
        for genre in movie_genres[i]:
            TF_IDF[i, genres.index(genre)] = 1 / len(movie_genres[i])
            genresnum[genres.index(genre)] += 1
    for col in range(lengenres):
        idf = math.log(lenmoive / genresnum[col])
        TF_IDF[:, col] = TF_IDF[:, col] * idf
    return TF_IDF


def get_user2movie(filename, movies):
    fileread = open(filename, 'r')
    next(fileread)
    data = []
    users = []
    for line in fileread:
        userid, movieid, rating, timestamp = line.strip().split(',')
        data.append([int(userid), int(movieid), float(rating)])
    for item in data:
        if item[0] not in users:
            users.append(item[0])
    user2movie = np.zeros([len(users), len(movies)])
    # 构造用户-电影效用矩阵
    for item in data:
        user2movie[item[0] - 1, movies.index(item[1])] = item[2]
    return user2movie, len(users)


def recom_k_movie(userid, k, user2movie, movies, CosSim):
    recom_movies = []  # 记录待推荐电影，即该用户没看的电影的序列[[0, index],...]
    rate_movies = []  # 记录用户已经看的电影打分和序列号[[rate,index], [...], [...]]
    row = userid - 1
    for col in range(len(movies)):
        if user2movie[row, col] > 0:
            rate_movies.append([user2movie[row, col], col])
        else:
            recom_movies.append([0.0, col])
    for i in range(len(recom_movies)):
        rec = recom_movies[i][1]
        simsum = 0.0
        sim_rating = 0.0
        for j in range(len(rate_movies)):
            rate = rate_movies[j][1]
            simsum += CosSim[rate, rec]
            sim_rating += CosSim[rate, rec] * rate_movies[j][0]
        if simsum != 0.0:
            recom_movies[i][0] = sim_rating / simsum
    recom_movies.sort(reverse=True)
    return recom_movies[:k]


def recom_test_movie(userid, movieid_index1, movieid_index2, user2movie, CosSim):
    recom_movies = [[0.0, movieid_index1], [0.0, movieid_index2]]  # 记录待推荐电影，即该用户没看的电影的序列[[0, index],...]
    rate_movies = []  # 记录用户已经看的电影打分和序列号[[rate,index], [...], [...]]
    row = userid - 1
    for col in range(len(movies)):
        if user2movie[row, col] > 0:
            rate_movies.append([user2movie[row, col], col])
    for i in range(len(recom_movies)):
        rec = recom_movies[i][1]
        simsum = 0.0
        sim_rating = 0.0
        for j in range(len(rate_movies)):
            rate = rate_movies[j][1]
            simsum += CosSim[rate, rec]
            sim_rating += CosSim[rate, rec] * rate_movies[j][0]
        if simsum != 0.0:
            recom_movies[i][0] = sim_rating / simsum
    return recom_movies


if __name__ == '__main__':
    movie_title, movie_genres, movies, genres = get_data("movies.csv")
    TF_IDF = get_TF_IDF(len(movies), len(genres), movie_genres, genres)
    CosSim = cosine_similarity(TF_IDF)
    My_userid = 29  # 推荐用户
    k = 10  # 推荐电影数
    user2movie, lenuser = get_user2movie("train_set.csv", movies)
    recom_k_movies = recom_k_movie(My_userid, k, user2movie, movies, CosSim)
    for i in range(k):
        index = recom_k_movies[i][1]
        print("{} {} {} {}".format(i + 1, movie_title[index], movie_genres[index], recom_k_movies[i][0]))

    test_data = pd.read_csv('test_set.csv')
    usersid = test_data['userId']
    movieid = test_data['movieId']
    rating = test_data['rating']
    sse = 0
    for i in range(int(len(usersid) / 2)):
        movieid_index1 = movies.index(int(movieid[i * 2]))
        movieid_index2 = movies.index(int(movieid[i * 2 + 1]))
        test_rating_list = recom_test_movie(usersid[i*2], movieid_index1, movieid_index2, user2movie, CosSim)
        print("{},{}".format(usersid[i * 2], test_rating_list[0][0]))
        print("{},{}".format(usersid[i * 2 + 1], test_rating_list[1][0]))
        sse += pow(test_rating_list[0][0] - float(rating[i * 2]), 2)
        sse += pow(test_rating_list[1][0] - float(rating[i * 2 + 1]), 2)
    print("sse:", sse)


