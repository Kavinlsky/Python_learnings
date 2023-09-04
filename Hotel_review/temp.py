# data = ['negative' 'positive' 'negative' 'positive' 'negative' 'negative' 'positive' 'negative' 'positive' 'negative']
#
# datas=''.join(data)
#
# for i in range(0,len(datas),8):
#     data=datas[i:i+8]
#     print(data)



# print(data[0])
#
# data_str = 'negativepositivenegativepositivenegativenegativepositivenegativepositivenegative'
#
# # Insert commas to split the string into individual elements
# data_with_commas = [data_str[i:i+8] for i in range(0, len(data_str), 8)]
#
# print(data_with_commas)

queries=['rooms are worst i am not satisfied ', 'The ambients was good', 'The service was not satisfied', 'Food Was nice', 'AC not working ', 'rooms are worst i am not satisfied ', 'The ambients was good', 'The service was not satisfied', 'Food Was nice', 'AC not working ']
predictions=['negative' 'positive' 'negative' 'positive' 'negative' 'negative' 'positive' 'negative' 'positive' 'negative']


predicted_results=[]
results=''.join(predictions)

for i in range(0,len(results),8):
    result=results[i:i+8]
    predicted_results.append(result)


for queries,prediction in zip(queries,predicted_results):
    print(queries,"-----",prediction)