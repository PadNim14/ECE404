import copy
def shift_rows(state_array):
    temp = copy.deepcopy(state_array)
    # print(temp)
    for i in range(1, 4):
        for j in range(4):
            # s0.0 s0,1 s0,2 s0,3
            # s1.1 s1,2 s1,3 s1,0
            # s2.2 s2,3 s2,0 s2,1
            # s3.3 s3,0 s3,1 s3,2
            temp[i][j] = state_array[i][(j + i) % 4]   
            
    return temp 

def inv_shift_rows(state_array):
    temp = copy.deepcopy(state_array)
    for i in range(1, 4):
        for j in range(4):
            # s0.0 s0,1 s0,2 s0,3
            # s1.1 s1,2 s1,3 s1,0
            # s2.2 s2,3 s2,0 s2,1
            # s3.3 s3,0 s3,1 s3,2
            temp[i][j] = state_array[i][(j - i) % 4]   
    return temp 

arr = [[1,2,3,4], [5,6,7,8], [9,10,11,12], [13,14,15,16]]
# print(shift_rows(arr))
print(arr)
print(inv_shift_rows(arr))