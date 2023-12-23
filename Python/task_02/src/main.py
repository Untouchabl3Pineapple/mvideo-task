def get_friends(friends_list):
    friends_dict = dict()

    for couple in friends_list:
        for user in couple:
            if user in friends_dict:
                friends_dict[user] += 1
            elif len(couple) == 2:
                friends_dict[user] = 1
            else:
                friends_dict[user] = 0

    return friends_dict


a = [
    [2, 3],
    [3, 4],
    [5],
    [2, 6],
    [2, 4],
    [6, 1],
]  # {2: 3, 3: 2, 4: 2, 5: 0, 6: 2, 1: 1}
b = [[1, 2], [3], [8], [6, 2]]  # {1: 1, 2: 2, 3: 0, 8: 0, 6: 1}


print(get_friends(a))
print(get_friends(b))
