# pip install clevercsv
import clevercsv

df = clevercsv.read_dataframe('data.csv')
# 如果文件不是标准的csv格式，不会报错，而是会自动处理好
print(df.head())