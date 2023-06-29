from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import pandas as pd

# 简单匹配,返回s1,s2之间的相似度，完全相同返回100
print(fuzz.ratio('四川省','四川'))
print(fuzz.ratio('四川省','四川省'))

# 部分匹配，如果s1是s2的子串，依然返回100
print(fuzz.partial_ratio('四川省','四川省'))
print(fuzz.partial_ratio('四川省','四川'))
print(fuzz.partial_ratio('四川省','西川'))

# fuzz.token_sort_ratio(S1,S2)只比较S1，S2单词是否相同，不考虑词语之间的顺序
# 中文需要加空格
print(fuzz.token_sort_ratio('四 川','川 四'))

# fuzz.token_set_ratio(S1，S2)相比fuzz.token_sort_ratio不考虑词语出现的次数；
print(fuzz.token_set_ratio('四 川','川 四 四'))

# process.extract(S1, ListS,limit=n)，表示从列表ListS中找出Top n与S1最相似的句子;
choices = ["四川省", "成都市", "西川", "四川"]
print(process.extract("四川", choices, limit=3))

# process.extractOne(S1,ListS)，返回最相似的一个
print(process.extractOne("四川", choices))



# 通用模糊匹配函数
def fuzzy_merge(df_1, df_2, key1, key2, threshold=90, limit=2):
    """
    :param df_1: the left table to join
    :param df_2: the right table to join
    :param key1: key column of the left table
    :param key2: key column of the right table
    :param threshold: how close the matches should be to return a match, based on Levenshtein distance
    :param limit: the amount of matches that will get returned, these are sorted high to low
    :return: dataframe with boths keys and matches
    """
    # 匹配参考表
    s = df_2[key2].tolist()

    # 待匹配结果表
    m = df_1[key1].apply(lambda x: process.extract(x, s, limit=limit))

    # 把算出来的结果放到了df_1的matches列
    df_1['matches'] = m

    # 对extractOne方法的完善，提取到的最大匹配度的结果并不一定是我们需要的，所以需要设定一个阈值来评判，这个值可以是90
    # 第一个‘matches'字段返回的数据类型，参考一下这个格式：[('四川省', 90), ('成都市', 0)]
    m2 = df_1['matches'].apply(
        lambda x: [i[0] for i in x if i[1] >= threshold][0] if len([i[0] for i in x if i[1] >= threshold]) > 0 else '')

    # 把最佳的符合条件的匹配信息处理到df_1的matches列
    df_1['matches'] = m2

    return df_1


'''
使用Gensim进行批量模糊匹配
Gensim支持包括TF-IDF，LSA，LDA，和word2vec在内的多种主题模型算法，支持流式训练，并提供了诸如相似度计算，信息检索等一些常用任务的API接口。

如果数据库达到几万级别，如果依然采用编辑距离或fuzzywuzzy暴力遍历计算，预计几个小时也无法计算出结果，但使用NLP神器Gensim仅需几秒钟，即可计算出结果。
'''
import jieba
from gensim import corpora,similarities,models


data = pd.read_csv("配变.csv", encoding="gbk").astype(str)
find = pd.read_csv("用户名.csv", encoding="gbk").astype(str)

# 对原始的文本进行jieba分词，得到用户名称的特征列表
data_split_word = data.name.apply(jieba.lcut)

# 建立语料特征的索引字典，并将文本特征的原始表达转化成词袋模型对应的稀疏向量的表达
# 这样得到了每一个用户名称对应的稀疏向量（这里是bow向量），向量的每一个元素代表了一个词在这个名称中出现的次数。
dictionary = corpora.Dictionary(data_split_word.values)
data_corpus = data_split_word.apply(dictionary.doc2bow)

# 将被查找的数据统一由小写数字转换为大写数字（保持与数据库一致）后，作相同的处理，即可进行相似度批量匹配
trantab = str.maketrans("0123456789", "零一二三四五六七八九")
find_corpus = find.name.apply(
    lambda x: dictionary.doc2bow(jieba.lcut(x.translate(trantab))))

# 构建相似度矩阵
tfidf = models.TfidfModel(data_corpus.to_list())
index = similarities.SparseMatrixSimilarity(
    tfidf[data_corpus], num_features=len(dictionary))

# 同时获取最大的3个结果
result = []
for corpus in find_corpus.values:
    sim = pd.Series(index[corpus])
    result.append(data.name[sim.nlargest(3).index].values)
result = pd.DataFrame(result)
result.rename(columns=lambda i: f"匹配{i + 1}", inplace=True)
result = pd.concat([find, result], axis=1)

result.to_excel('结果.xlsx')