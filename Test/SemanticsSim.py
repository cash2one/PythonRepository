# -*- encoding: utf-8 -*-

# '''
# Author: Eachen Kuang
# Date:  2017.6.4
# Goal: 语义相似度计算
# Other:
# '''
import logging
from gensim import models
from gensim import corpora
import numpy as np
import os
import xlwt
from pprint import pprint
from MedicineSCI.eigenvalue import Innovation

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


#对于每个LDA模型，将所有主题放入一起
#输入一个LDA模型，返回一个包含所有list_topic的list_topics
def model2list_topics(lda_model,num_words=400):
    show = lda_model.show_topics(num_words=num_words, formatted=False)
    dict_show = dict(show)
    # dict_show[i]
    list_topics = []
    for i in range(10):
        print str(i)+'in model2list_topics'
        list_topic = []
        for word in dict(dict_show[i]).iterkeys():
            list_topic.append(str(word).split(' [')[0])
            list_topic = filter_with_list(list_topic) #将得到list进行MH过滤
        list_topics.append(list_topic)
    return list_topics
#end model2list_topics(lda_model,num_words=400)


# 传入一个list，返回一个list
# 得到一个在d2017.b中的共有的list
def filter_with_list(input_list):
    with open('./temp/MH.txt','r')as readMH:
        cor2_MH = set()
        for line in readMH:
            term = str(line).strip()
            cor2_MH.add(term)
        readMH.close()

    # cor1_in = set()
    # for i in input_list:
    #     cor1_in.add(i)
    cor1_in = set(input_list)

    cor3_out = cor1_in & cor2_MH
    return list(cor3_out)
# end filter_with_list(input_list)

def main():

    # 读取lda模型
    lda1 = models.LdaModel.load('./temp/_2000-2001lda_moedel')
    lda2 = models.LdaModel.load('./temp/_2002-2003lda_moedel')
    lda3 = models.LdaModel.load('./temp/_2004-2005lda_moedel')
    lda4 = models.LdaModel.load('./temp/_2006-2007lda_moedel')
    lda5 = models.LdaModel.load('./temp/_2008-2009lda_moedel')
    lda6 = models.LdaModel.load('./temp/_2010-2011lda_moedel')
    lda7 = models.LdaModel.load('./temp/_2012-2013lda_moedel')
    lda8 = models.LdaModel.load('./temp/_2014-2015lda_moedel')
    lda9 = models.LdaModel.load('./temp/_2016-2017lda_moedel')

    # 用列表保存
    LDA_list = []
    LDA_list.append(lda1)
    LDA_list.append(lda2)
    LDA_list.append(lda3)
    LDA_list.append(lda4)
    LDA_list.append(lda5)
    LDA_list.append(lda6)
    LDA_list.append(lda7)
    LDA_list.append(lda8)
    LDA_list.append(lda9)
    # print LDA_list

    ms = Innovation.MSSQL(host="localhost:59318", user="eachen", pwd="123456", db="mydata")
    resultList = ms.ExecQuery("SELECT MH,EN,MN,AN FROM MeshStructure")
    # 用于存放MH-EN，MN，AN的字典
    dic_EN = {}
    dic_MN = {}
    dic_AN = {}
    for (MH, EN, MN, AN) in resultList:
        dic_EN[MH] = EN
        dic_MN[MH] = MN
        dic_AN[MH] = AN

    #初始化模型生成的list  共9个LDA(0,1,2,3,4,5,6,7,8) * 10个topci * list
    list_all = []
    for i in range(9):
        print str(i)+'in main'
        list = model2list_topics(LDA_list[i])
        list_all.append(list)

    print list_all.__len__()
    print list_all[0].__len__()
    print list_all[0][0].__len__()
    print list_all

    # Innovation.inno(,dic_MN, dic_AN, dic_EN)
    wbk = xlwt.Workbook()
    for i in range(8):
        sheet = wbk.add_sheet('sheet'+str(i))
        for j in range(10):
            for k in range(10):
                print str(i)+str(i+1)+'topic'
                print(j, k)
                sim1 = Innovation.inno(list_all[i][j], list_all[i+1][k],dic_MN, dic_AN, dic_EN)
                sheet.write(j+1,k+1, str(sim1))

    wbk.save("topic_evolution_semanticSim.xls")
if __name__ == '__main__':
    main()
