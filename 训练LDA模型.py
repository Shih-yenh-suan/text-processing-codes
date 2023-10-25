import os
import logging
import math
import pandas as pd
from gensim import corpora, models
from gensim.models.ldamodel import LdaModel
from sklearn.model_selection import train_test_split
'''
输入： LDA 模型的模型数区间、数据集路径、输出 xlsx 文件路径、迭代次数

训练模型，将模型数和对应的困惑度保存到 xlsx 文件中。

注意：困惑度根据定义手动计算

'''
logging.basicConfig(
    format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
os.chdir('D:\ZZZMydocument\Codes\LDA主题模型')


def train_lda(data_folder, excel_path, num_topics_range, num_iterations):
    # Load data
    files = os.listdir(data_folder)
    data = []
    for file in files:
        with open(os.path.join(data_folder, file), 'r', encoding='utf-8') as f:
            data.append(f.read().split())

    # Split data into train and test sets
    train_data, test_data = train_test_split(
        data, test_size=0.2, random_state=42)

    # Create dictionary and corpus
    dictionary = corpora.Dictionary(train_data)
    corpus = [dictionary.doc2bow(text) for text in train_data]
    test_corpus = [dictionary.doc2bow(text) for text in test_data]

    perplexities = []
    for num_topics in num_topics_range:
        # Train LDA model
        lda = LdaModel(corpus, num_topics=num_topics,
                       id2word=dictionary, iterations=num_iterations)

        # Calculate perplexity
        calc_perplexity = perplexity(
            lda, test_corpus, dictionary, len(dictionary.keys()), num_topics)
        perplexities.append((num_topics, calc_perplexity))

    # Write results to Excel
    df = pd.DataFrame(perplexities, columns=['num_topics', 'perplexity'])
    df.to_excel(excel_path, index=False)


def perplexity(ldamodel, testset, dictionary, size_dictionary, num_topics):
    """calculate the perplexity of a lda-model"""
    # dictionary : {7822:'deferment', 1841:'circuitry',19202:'fabianism'...]
    print('the info of this ldamodel: \n')
    print('num of testset: %s; size_dictionary: %s; num of topics: %s' %
          (len(testset), size_dictionary, num_topics))
    prep = 0.0
    prob_doc_sum = 0.0
    # store the probablity of topic-word:[(u'business', 0.010020942661849608),(u'family', 0.0088027946271537413)...]
    topic_word_list = []
    for topic_id in range(num_topics):
        topic_word = ldamodel.show_topic(topic_id, size_dictionary)
        dic = {}
        for word, probability in topic_word:
            dic[word] = probability
        topic_word_list.append(dic)
    # store the doc-topic tuples:[(0, 0.0006211180124223594),(1, 0.0006211180124223594),...]
    doc_topics_ist = []
    for doc in testset:
        doc_topics_ist.append(
            ldamodel.get_document_topics(doc, minimum_probability=0))
    testset_word_num = 0
    for i in range(len(testset)):
        prob_doc = 0.0  # the probablity of the doc
        doc = testset[i]
        doc_word_num = 0  # the num of words in the doc
        for word_id, num in doc:
            prob_word = 0.0  # the probablity of the word
            doc_word_num += num
            word = dictionary[word_id]
            for topic_id in range(num_topics):
                # cal p(w) : p(w) = sumz(p(z)*p(w|z))
                prob_topic = doc_topics_ist[i][topic_id][1]
                prob_topic_word = topic_word_list[topic_id][word]
                prob_word += prob_topic*prob_topic_word
            if prob_word <= 0:
                prob_word = 1
            prob_doc += math.log(prob_word)  # p(d) = sum(log(p(w)))
        prob_doc_sum += prob_doc
        testset_word_num += doc_word_num
    # perplexity = exp(-sum(p(d)/sum(Nd))
    prep = math.exp(-prob_doc_sum/testset_word_num)
    print("the perplexity of this ldamodel is : %s" % prep)
    return prep


def main():
    start = 11
    end = 29
    step = 2
    data_folder = ""
    excel_path = f"{start}_{end}_{step}.xlsx"
    num_topics_range = range(start, end + 1, step)
    num_iterations = 1000

    train_lda(data_folder, excel_path, num_topics_range, num_iterations)


if __name__ == "__main__":
    main()
