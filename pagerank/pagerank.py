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
    if len(corpus[page]) == 0:
        # choose from all
        prob_distribution = dict.fromkeys(corpus.keys(), 1 / len(corpus))
    else:
        d = damping_factor / len(corpus[page])
        # choose from all
        prob_distribution = dict.fromkeys(corpus, (1 - damping_factor) / len(corpus))
        # plus probability of linked pages
        for p in corpus[page]:
            prob_distribution[p] += d
    return prob_distribution

    # keys = set(corpus.keys())
    # values = set().union(*corpus.values())
    # all_pages = keys.union(values)
    # all_pages.discard(page)
    # corpus_without_page = list(all_pages)
    # linked_pages = list(corpus[page])
    # # probability of randomly choose a page from all pages
    # pro_choose_from_all = (1 - damping_factor) / len(all_pages)
    # # probability of choose pages that linked to current page
    # pro_choose_from_linked = damping_factor / len(linked_pages)
    # pages_prob = []
    # for page in all_pages:
    #     if page not in linked_pages:
    #         pages_prob.append((page, pro_choose_from_all))
    #     else:
    #         pages_prob.append((page, pro_choose_from_linked + pro_choose_from_all))
    # return pages_prob


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    page_rank = dict.fromkeys(corpus, 0)
    # the first time: randomly choose the page
    next_page = random.choice(list(corpus.keys()))
    page_rank[next_page] += 1
    for i in range(n - 1):
        # choose the next page
        x = random.uniform(0, 1)
        prob_dis = transition_model(corpus, next_page, damping_factor)
        # cumulative probability
        cumu_prob = 0
        # choose the next page according to the cumulate probability
        for page, p in prob_dis.items():
            cumu_prob += p
            if cumu_prob > x:
                next_page = page
                break
        page_rank[next_page] += 1
        # the value of page_rank is the number of visited times,
        # and we need to turn it to probability
    for page in page_rank.keys():
        page_rank[page] /= n
    print(f"sample check sample: {sum(page_rank.values())}")
    return page_rank


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    n = len(corpus)
    page_rank = dict.fromkeys(corpus, (1 - damping_factor) / n)
    # return a dict that contains the number of links of each page
    num_links = {page: len(corpus[page]) for page in corpus.keys()}
    flag = True
    while flag:
        flag = False
        new_rank = {}
        for page in corpus.keys():
            x = sum((page_rank[i] / num_links[i]) for i in corpus.keys() if page in corpus[i])
            new_rank[page] = (1 - damping_factor) / n + damping_factor * x
            if abs(new_rank[page] - page_rank[page]) > 0.001:
                # still not convergence so continue to loop
                flag = True
        for p in new_rank:
            page_rank[p] = new_rank[p]
    total_rank = sum(page_rank.values())
    for p in page_rank:
        page_rank[p] /= total_rank
    print(f"sample check iteration: {sum(page_rank.values())}")
    return page_rank


if __name__ == "__main__":
    main()
