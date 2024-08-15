import pickle
with open('C:/Users/User/Desktop/New_Batch_Code/Brands/Gorkha Brewery/Gorkha Brewery.pkl','rb') as a:
    details = pickle.load(a)

print(details)
# list1 = [details['line1'],details['line2'],details['line3'],details['line4']]

# line_strings = []
# for j in range(0,3):
#     line_strings.append(list1[j])

# for i in range(1,4):
#     index = 'line' + str(i)
#     print(details[index])