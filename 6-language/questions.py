import nltk
import sys
import os
import string
import math

FILE_MATCHES = 1
SENTENCE_MATCHES = 1


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    files_map = {}

    for file_name in os.listdir(directory):
        with open(os.path.join(directory, file_name), encoding="utf-8") as file:
            files_map[file_name] = file.read()

    return files_map


def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.
    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    tokenised_words = nltk.tokenize.word_tokenize(document.lower())

    words = [word for word in tokenised_words if word not in nltk.corpus.stopwords.words("english") and word not in string.punctuation]

    return words


def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.
    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    idfs = {}
    total_docs_num = len(documents)

    unique_words = set(sum(documents.values(), []))
    for unique_word in unique_words:
        num_of_unique_words = 0
        for document in documents.values():
            if unique_word in document:
                num_of_unique_words += 1

        idf = math.log(total_docs_num/num_of_unique_words)
        idfs[unique_word] = idf

    return idfs


def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    tf_idf_values = {}
    for filename, filecontent in files.items():
        tf_idf_value = 0
        for query_word in query:
            if query_word in filecontent:
                tf_idf_value += filecontent.count(query_word) * idfs[query_word]
        if tf_idf_value != 0:
            tf_idf_values[filename] = tf_idf_value

    sorted_tf_idf_values = [k for k, v in sorted(tf_idf_values.items(), key=lambda x: x[1], reverse=True)]
    return sorted_tf_idf_values[:n]


def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    idf_values = {}

    for sentence, sentence_words in sentences.items():
        idf_value = 0

        for query_word in query:
            if query_word in sentence_words:
                idf_value += idfs[query_word]

        if idf_value != 0:
            density = sum([sentence_words.count(query_word) for query_word in query]) / len(sentence_words)

            idf_values[sentence] = (idf_value, density)

    sorted_idf_values = [k for k, v in sorted(idf_values.items(), key=lambda x: (x[1][0], x[1][1]), reverse=True)]

    return sorted_idf_values[:n]


if __name__ == "__main__":
    main()
