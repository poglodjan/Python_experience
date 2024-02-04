import random
test_list = [1, 4, 5, 6, 3]

print ("The original list is : " + str(test_list))
 
for i in range(len(test_list)-1, 0, -1):
     
    j = random.randint(0, i + 1)

    test_list[i], test_list[j] = test_list[j], test_list[i]

print ("The shuffled list is : " +  str(test_list))
