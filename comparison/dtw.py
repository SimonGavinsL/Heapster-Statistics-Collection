import math
import pandas


def dtw_distance(list_s, list_t):
    dtw = [[math.inf for x in range(len(list_t) + 1)] for y in range(len(list_s) + 1)]
    dtw[0][0] = 0

    for i in range(len(list_s)):
        for j in range(len(list_t)):
            cost = abs(list_s[i] - list_t[j])
            dtw[i + 1][j + 1] = cost + min(dtw[i][j + 1],   # insertion
                                           dtw[i + 1][j],   # deletion
                                           dtw[i][j])       # match

    return dtw[len(list_s)][len(list_t)]


df = pandas.read_csv('graphs45.csv')

