def twoSum(nums, target)  :
    hashMap = {}
    for i, num in enumerate(nums):
        hashMap[num] = i
    #this populates the hashmap but does it in O(n)
    print(hashMap)

    for i, num in enumerate(nums):
        desired = target - num #the number required so make the target
        if desired in hashMap and hashMap[desired] != i: #make sure the desired is not the same numbner that I have already, aka 4 + 4 = 8, but i cant resumt eh same number
            return i, hashMap[desired]
          

print(twoSum(nums=[2,7,11,15],target=9))



