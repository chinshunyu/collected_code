# 1. 读取文本文件（.txt）：

# 方法一：**使用open函数读取

with open('file.txt', 'r') as f:
    content = f.read()
    print(content)
# 方法二：**使用readlines函数逐行读取

with open('file.txt', 'r') as f:
    lines = f.readlines()
    for line in lines:
        print(line)
# 方法三：**使用迭代读取每一行

with open('file.txt', 'r') as f:
    for line in f:
        print(line)
# 2. 读取CSV文件：

# 方法一：**使用csv模块的reader方法

import csv
with open('file.csv', 'r') as f:
    reader = csv.reader(f)
    for row in reader:
        print(row)
# 方法二：**使用pandas库读取

import pandas as pd
df = pd.read_csv('file.csv')
print(df)
# 3. 读取JSON文件：

# 方法一：**使用json模块的load方法

import json
with open('file.json', 'r') as f:
    data = json.load(f)
    print(data)
# 方法二：**使用pandas库读取

import pandas as pd
df = pd.read_json('file.json')
print(df)
# 4. 读取Excel文件：

# 方法一：**使用pandas库读取

import pandas as pd
df = pd.read_excel('file.xlsx', sheet_name='Sheet1')
print(df)
# 方法二：**使用xlrd库读取


import xlrd
wb = xlrd.open_workbook('file.xlsx')
sheet = wb.sheet_by_name('Sheet1')
for row in range(sheet.nrows):
    for col in range(sheet.ncols):
        print(sheet.cell(row, col).value)

# 5. 读取XML文件：
import xml.etree.ElementTree as ET

tree = ET.parse('file.xml')
root = tree.getroot()


# 遍历XML文档
for element in root.iter():
    print(element.tag, element.text)

# 6. 读取图片文件：
from PIL import Image

image = Image.open('image.jpg')
image.show()