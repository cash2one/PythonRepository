# 一些小发现

## 2017.7.18
今天在研究gensim中的Corpora的时候，无意中发现了很多不知道的东西。

###
目的：因为之前语料库存储的是，每一行为一篇文章，而我需要获取每一小篇文章作为一个小语料库来预测它所属的主题类别，后来仔细研究bleiCorpora中的代码，终于让我发现了一些端倪。  

在bleiCorpora中，它有这样一个函数，它能够获取存储corpora中的位置之后的一行作为一个document，而我们无法简单获取它的offset
```python
def docbyoffset(self, offset):
    """
    Return the document stored at file position `offset`.
    """
    with utils.smart_open(self.fname) as f:
        f.seek(offset)
        return self.line2doc(f.readline())
```

而其中有个变量为index,它是ndarray类型，它保存了corpora每一行开头的位置。  
因此，配合bleiCorpora中的index，就能轻轻松松地读取每一行。  

```python
bow = corpora.BleiCorpus("./timewindow_in3/corpus_2000-2001-2002.blei")
bow.docbyoffset(bow.index[0]) #获取第一行
bow.docbyoffset(bow.index[1]) #获取第二行
```

这样就能轻轻松松地获得每一行

```python
print bow.length    # None
print bow.fname    #./timewindow_in3/corpus_2000-2001-2002.blei   
print bow.index    #一个ndarray数组
print bow.index.__len__()    #517 长度
print bow.id2word
print bow.__len__()    #517 长度
```
## 2017.8.3

使用`gensim.matutils.corpus2csc`可以将一个corpus转化为一个csc的三元组列表
使用`gensim.matutils.corpus2dense`可以将一个corpus转化为一个dense矩阵
```python
import scipy.sparse
bow = corpora.BleiCorpus("./timewindow_in3/corpus_2000-2001-2002.blei")
scipy_csc_matrix = gensim.matutils.corpus2csc(corpus=bow)
scipy_dence_matrix = gensim.matutils.corpus2dense(corpus=bow, num_terms=bow.id2word.__len__())
print scipy_csc_matrix
print scipy_dence_matrix[0].__len__()
print scipy_csc_matrix.dtype, scipy_csc_matrix.get_shape
```

下面是对于`corpus2dense`的源码解释
```python
def corpus2dense(corpus, num_terms, num_docs=None, dtype=np.float32):
    """
    Convert corpus into a dense np array (documents will be columns). You
    must supply the number of features `num_terms`, because dimensionality
    cannot be deduced from the sparse vectors alone.

    You can optionally supply `num_docs` (=the corpus length) as well, so that
    a more memory-efficient code path is taken.

    This is the mirror function to `Dense2Corpus`.

    """
    if num_docs is not None:
        # we know the number of documents => don't bother column_stacking
        docno, result = -1, np.empty((num_terms, num_docs), dtype=dtype)
        for docno, doc in enumerate(corpus):
            result[:, docno] = sparse2full(doc, num_terms)
        assert docno + 1 == num_docs
    else:
        result = np.column_stack(sparse2full(doc, num_terms) for doc in corpus)
    return result.astype(dtype)
```




