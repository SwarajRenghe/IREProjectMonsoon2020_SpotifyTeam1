# Python code t get difference of two lists
# Using set()
# def Diff(li1, li2):
# 	return (list(list(set(li1)-set(li2)) + list(set(li2)-set(li1))))

def Diff(li1, li2):
    li_dif = [i for i in li1 + li2 if i not in li1 or i not in li2]
    return li_dif

# Driver Code
li1 = [10, 15, 20, 25, 30, 35, 40]
li2 = [25, 40, 35]
print(Diff(li1, li2))
