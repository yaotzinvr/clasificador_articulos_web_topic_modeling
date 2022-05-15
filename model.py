import re
import gensim
from config import CATEGORIAS_EXCLUIR

stop_words = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll", "you'd", 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', "don't", 'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't"]
stop_words += ['lack', 'make', 'want', 'seem', 'run', 'need', 'even', 'right','use', 'not', 'would', 'say', 'could', '_', 'be', 'know', 'good', 'go', 'get', 'do','done', 'try', 'many','from', 'subject', 're', 'edu','some', 'nice', 'thank','think', 'see', 'rather', 'easy', 'easily', 'lot', 'line', 'even', 'also', 'may', 'take','come','using','used','one','two','set','given']
stop_words += CATEGORIAS_EXCLUIR


def get_data_words(texto):
    try:
        # Limpia texto de signos
        texts = texto.split('.')
        corpus = [re.sub('[\.,\\\/#¡!¿?$%\^&\*;:{}\[\]=\'+\-_`~()”“"…<>]', ' ', t).lower().replace('  ', ' ') for t in texts]
        # Genera estructura de palabras
        data_words = [gensim.utils.simple_preprocess(t, deacc=True) for t in corpus]
        # Elimina stopwords
        data_words_clean = [[word for word in gensim.utils.simple_preprocess(str(doc)) if word not in stop_words] for doc in data_words]
    except Exception as e:
        raise Exception('(get_data_words)' + str(e))
    return data_words_clean


def get_model(texto_completo):
    try:
        #Genera corpus
        data_words = get_data_words(texto_completo)
        #Genera modelo LDA
        id2word = gensim.corpora.Dictionary(data_words)
        corpus = [id2word.doc2bow(text) for text in data_words]
        lda = gensim.models.ldamodel.LdaModel(corpus, id2word=id2word, num_topics=1)
    except Exception as e:
        raise Exception('(get_model)' + str(e))
    return {x.split('*')[1]:float(x.split('*')[0]) for x in lda.print_topic(0).replace('"','').replace(' ','').split('+')[:10]}
