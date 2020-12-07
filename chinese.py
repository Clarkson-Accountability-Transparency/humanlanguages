import numpy as np
from sklearn.decomposition import PCA
import sys
from wikipedia2vec import Wikipedia2Vec

WORD_PAIRS = [['女人', '男人'], ['女儿', '儿子'], ['母亲', '父亲'], ['女孩', '男孩'], ['皇后', '国王'], ['妻子', '丈夫'], ['女士', '先生']]
WORD_PAIRS_FLAT = ['女人', '男人', '女儿', '儿子', '母亲', '父亲', '女孩', '男孩', '皇后', '国王', '妻子', '丈夫', '女士', '先生']
NEUTRAL_WORDS = ['护士', '教师', '作家', '工程师', '科学家', '经理', '司机', '银行家', '电工', '酒保', '音乐家', '艺术家', '厨师', '制片人', '法官', '喜剧演员', '发明家', '工人', '战士', '记者']

MODEL = "/home/mahonec_/languages/models/zhwiki/ZHWIKI"

def defining_set_direction(defining_sets, n=0):
    matrix = []
    for (w1,w2) in defining_sets:
        center = (w1+w2)/2 #center for covariance to be nice
        matrix.append(w1-center)
        matrix.append(w2-center)
    pca = PCA(n_components=10)
    #print("data matrix is: ")
    #print(matrix)
    pca.fit(matrix)
    print("Explained Variance Ratio: " + str(pca.explained_variance_ratio_)) 
    return pca.components_[n]

def compute_bias_direction(model, pairs, n=0, ransac=False):
    defining_sets = []
    words = []
    for (w1,w2) in pairs:
        try:
            w1 = w1.lower().split()
            w1vec = sum([model.get_word_vector(w) for w in w1])
            w2 = w2.lower().split()
            w2vec = sum([model.get_word_vector(w) for w in w2])
            vector_pair = (w1vec,w2vec)

            defining_sets.append(vector_pair)
            words.append((' '.join(w1),' '.join(w2)))
        except KeyError as e:
            print("Marzieh owes me a dragon")
            print("Error on " + str((w1,w2)))
            pass

    g = defining_set_direction(defining_sets, n)
    return g

def corpus_bias(model, neutral_words, defining_set):
    g = compute_bias_direction(model, defining_set)
    print("Computing bias now")

    # The sum of all word vectors
    total = np.zeros(100);
    count = 0.0

    # The sum of dot products is the dot product of the sum
    for word in neutral_words:
        #if word in model:
        if model.dictionary.get_word(word) is not None:
            total += np.copy(model.get_word_vector(word))
            count += 1.0
        else:
            #print("word " + word + " not in model")
            pass

    # We only need 1 dot product
    total_bias = np.abs(np.dot(total,g)/(np.linalg.norm(total)*np.linalg.norm(g)))
    print(total_bias)

def bias_by_word(model, neutral_words, defining_set, pca):
    g = compute_bias_direction(model, defining_set, pca)
    print("Computing bias now")
    
    # This is much slower because its calculating len(neutral_words) dot products instead of 1
    for word in neutral_words:
        #if word in model:
        if model.dictionary.get_word(word) is not None:
            v = model.get_word_vector(word)
            bias = np.dot(v,g)/(np.linalg.norm(v)*np.linalg.norm(g))
            print(word + "," + str(bias))
        else:
            #print(word + ",NA")
            pass


if __name__ == "__main__":
    wiki2vec = Wikipedia2Vec.load(MODEL)

    bias_by_word(wiki2vec, NEUTRAL_WORDS, WORD_PAIRS, 0)
    bias_by_word(wiki2vec, WORD_PAIRS_FLAT, WORD_PAIRS, 0)
