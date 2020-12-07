import numpy as np
from sklearn.decomposition import PCA
from gensim.models import Word2Vec

def defining_set_direction(defining_sets, n=0):
    matrix = []
    for (w1,w2) in defining_sets:
        center = (w1+w2)/2 #center for covariance to be nice
        matrix.append(w1-center)
        matrix.append(w2-center)
    pca = PCA(n_components=3)
    #print("data matrix is: ")
    #print(matrix)
    pca.fit(matrix)
    print("Explained Variance Ratio: " + str(pca.explained_variance_ratio_)) 
    #print(pca.components_[n])
    return pca.components_[n]


def compute_bias_direction(model, pairs, n=0,):
    defining_sets = []
    words = []
    for (w1,w2) in pairs:
        try:
            w1 = w1.lower()
            w1vec = model[w1]
            w2 = w2.lower()
            w2vec = model[w2]
            vector_pair = (w1vec,w2vec)

            defining_sets.append(vector_pair)
            words.append((' '.join(w1),' '.join(w2)))
        except KeyError as e:
            print("Marzieh owes me a dragon")
            print("One of these words are missing: " + str((w1,w2)) + str(e))
            pass

    g = defining_set_direction(defining_sets, n)
    return g


def bias_by_word(model, neutral_words, defining_set, pca):
    g = compute_bias_direction(model, defining_set, pca)
    print("Computing bias now")
    
    # This is much slower because its calculating len(neutral_words) dot products instead of 1
    for word in neutral_words:
        #if word in model:
        if word in model:
            v = model[word]
            bias = np.dot(v,g)/(np.linalg.norm(v)*np.linalg.norm(g))
            print(word + "," + str(bias))
        else:
            print(word + ",NA")
            pass
    
    return 0

if __name__ == "__main__":
    model = Word2Vec.load("spanish.model")
    pairs = [['mujer', 'hombre'], ['hija', 'hijo'], ['madre', 'padre'], ['niña', 'niño'], ['reina', 'rey'], ['esposa', 'esposo'], ['señora', 'señor']]
    
    neutral= """
    gerente
    electricista
    artista
    cineasta
    periodista
    celebridad
    estudiante
    atleta
    policía
    persona
    ayudante
    analista
    astronauta
    """.split()
    
    female = """
    enfermera
    professora
    escritora
    ingeniera
    científica
    conductora
    banquera
    Camarera
    Música
    cocinera
    jueza
    cómica
    inventora
    trabajadora
    soldada
    actriz
    gobernadora
    granjera
    abogada
    aventurera
    embajadora
    astrónoma
    bióloga
    """.split()

    male= """
    enfermero
    profesor
    escritor
    ingeniero
    científico
    conductor
    banquero
    camarero
    músico
    cocinero
    juez
    cómico
    inventor
    trabajador
    soldado
    actor
    gobernador
    granjero
    abogado
    aventurero
    embajador
    astrónomo
    biólogo
    """.split()


    bias_by_word(model, neutral, pairs, 0)
    bias_by_word(model, female, pairs, 0)
    bias_by_word(model, male, pairs, 0)
