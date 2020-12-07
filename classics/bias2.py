import numpy as np
from sklearn.decomposition import PCA
from gensim.models import Word2Vec

def dimension_reducation(defining_words, words_to_reduce):
    defining_vectors = []
    
    for w in defining_set:
        try:
            defining_vectors.append(model.wv[w])
        except KeyError as e:
            print("This word is missing: " + str(w) + str(e))

    center = sum(defining_vectors) / len(defining_vectors)
    matrix = [(center - w) for w in defining_vectors]

    pca = PCA(n_components=2)
    pca.fit(matrix)

    x = pca.transform(words_to_reduce)
    print(x)
    

def defining_set_direction(defining_vectors, n=0):
    center = sum(defining_vectors) / len(defining_vectors)
    matrix = [(center - w) for w in defining_vectors]

    pca = PCA(n_components=2)
    #print("data matrix is: ")
    #print(matrix)
    pca.fit(matrix)
    #print("Explained Variance Ratio: " + str(pca.explained_variance_ratio_)) 
    #print(pca.components_[n])
    return pca.components_[n]


def compute_bias_direction(model, defining_set, n=0):
    defining_vectors = []
    
    for w in defining_set:
        try:
            defining_vectors.append(model.wv[w])
        except KeyError as e:
            print("This word is missing: " + str(w) + str(e))

    g = defining_set_direction(defining_vectors, n)
    return g


def bias_by_word(model, neutral_words, defining_set, pca):
    g = compute_bias_direction(model, defining_set, pca)
    #print("Computing bias now")
    
    # This is much slower because its calculating len(neutral_words) dot products instead of 1
    for word in neutral_words:
        #if word in model:
        if word in model.wv:
            v = model.wv[word]
            bias = np.dot(v,g)/(np.linalg.norm(v)*np.linalg.norm(g))
            print(word + "," + str(bias))
        else:
            print(word + ",NA")
            pass
    
    return 0

if __name__ == "__main__":
    model = Word2Vec.load("english.model")

    # This is a defining set without word piars, just "male" words and "female" words unordered
    defining_set = ['woman', 'daughter', 'mother', 'girl', 'queen', 'wife', 'madam', 'man', 'son', 'father', 'boy', 'king', 'husband', 'sir']
    neutral = ['nurse', 'teacher', 'writer', 'engineer', 'scientist', 'manager', 'driver', 'banker', 'electrician', 'bartender', 'musician', 'artist', 'chef', 'filmmaker', 'judge', 'comedian', 'inventor', 'worker', 'soldier', 'journalist', 'celebrity', 'student', 'athlete', 'actor', 'policeman', 'governor', 'farmer', 'person', 'lawyer', 'adventurer', 'aide', 'ambassador', 'analyst', 'astronaut', 'astronomer', 'biologist']
    
    bias_by_word(model, neutral, defining_set, 0)
    bias_by_word(model, defining_set, defining_set, 0)

    dimension_reducation(defining_set, defining_set)
