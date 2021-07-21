import nltk
import sys
import re

TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and" | "until"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"
"""

NONTERMINALS = """
S -> N V
PART -> NP VP | NP Adv VP | VP
NP -> N | NA N
S -> PART | PART Conj PART
S -> NP VP | VP NP | S Conj S
PP -> P NP
SUPP -> NP | P | Adv | SUPP SUPP | SUPP SUPP SUPP
NP -> N | Det N | NP PP | Det AdjP N
VP -> V | V NP | V PP | Adv VP | VP Adv
AdjP -> Adj | Adj AdjP
NA -> Det | Adj | NA NA
VP -> V | V SUPP
"""

grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)

def main():

    # If filename specified, read sentence from file
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            s = f.read()

    # Otherwise, get sentence as input
    else:
        s = input("Sentence: ")

    # Convert input into list of words
    s = preprocess(s)

    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
    except ValueError as e:
        print(e)
        return
    if not trees:
        print("Could not parse sentence.")
        return

    # Print each tree with noun phrase chunks
    for tree in trees:
        tree.pretty_print()

        print("Noun Phrase Chunks")
        for np in np_chunk(tree):
            print(" ".join(np.flatten()))


def preprocess(sentence):
    """
    Convert `sentence` to a list of its words.
    Pre-process sentence by converting all characters to lowercase
    and removing any word that does not contain at least one alphabetic
    character.
    """
    # Create a RegEx pattern to match words with at least one alphabetic character
    alpha_char = re.compile(".*[a-z].*")

    # Convert all the characters in the sentence to lowercase and word tokenise this modified string
    tokenised_words = nltk.word_tokenize(sentence.lower())

    # Remove all words that do not contain at least one alphabetic character using the RegEx pattern described above, and add the remaining words to the list
    words = [word for word in tokenised_words if alpha_char.match(word)]

    # Return the processed list
    return words



def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """
    np_chunks = []

    for subtree in tree.subtrees():
        if subtree.label() == "NP":
            np_chunks.append(subtree)

    return np_chunks


if __name__ == "__main__":
    main()
