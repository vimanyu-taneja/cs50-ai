import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.
    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
  

    probability_distribution = {}

    page_links = corpus[page]
    dict_len = len(corpus.keys())
    pages_len = len(corpus[page])

    # If there are no outgoing links, then assign a probability to each page that corresponds to a random choice between the pages
    if pages_len < 1:    
        for key in corpus:
            probability_distribution[key] = 1 / dict_len

    else:
        random_probability = (1 - damping_factor) / dict_len
        even_probability = damping_factor / pages_len

        for key in corpus:
            if key not in page_links:
                probability_distribution[key] = random_probability
            else:
                probability_distribution[key] = even_probability + random_probability

    return probability_distribution


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.
    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    # Initialise a dictionary where the number of samples is equal to zero
    samples_dict = corpus.copy()
    for i in samples_dict:
        samples_dict[i] = 0
    sample = None

    # Iterate n times, as we are sampling n pages
    for _ in range(n):
        if sample:
            # If there is a previous sample available, then choose using the transition model
            distribution = transition_model(corpus, sample, damping_factor)
            distribution_list = list(distribution.keys())
            distribution_weights = [distribution[i] for i in distribution]
            sample = random.choices(distribution_list, distribution_weights, k=1)[0]
        else:
            # If there is no previous sample available, then choose randomly
            sample = random.choice(list(corpus.keys()))

        # Count each sample
        samples_dict[sample] += 1

    # Convert sample count to percentage
    for i in samples_dict:
        samples_dict[i] /= n

    return samples_dict


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.
    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    num_of_pages = len(corpus)
    new_dictionary = {}
    old_dictionary = {}

    # Assign each page a PageRank value of 1/n, where n is the number of pages in the corpus, i.e. random selection
    for page in corpus:
        old_dictionary[page] = 1 / num_of_pages

    # Repeatedly calculate new PageRank values based on all of the current rank values
    # This process should repeat until no PageRank value changes by more than 0.001 between the current rank values and the new rank values
    change = 1
    while change >= 0.001:
        for page in corpus:
            new_val = 0
            for linking_page in corpus:

                # Check if the current page links to the current linking page
                if page in corpus[linking_page]:
                    new_val += (old_dictionary[linking_page] / len(corpus[linking_page]))

                # If the current page has no links, then interpret it as having one link for every other page
                if len(corpus[linking_page]) == 0:
                    new_val += (old_dictionary[linking_page]) / len(corpus)
            new_val *= damping_factor
            new_val += (1 - damping_factor) / num_of_pages

            new_dictionary[page] = new_val
      
        change = max([abs(new_dictionary[x] - old_dictionary[x]) for x in old_dictionary])
        old_dictionary = new_dictionary.copy()

    return old_dictionary


if __name__ == "__main__":
    main()
