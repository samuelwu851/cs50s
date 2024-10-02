import csv
import itertools
import sys

PROBS = {

    # Unconditional probabilities for having gene
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },

    "trait": {

        # Probability of trait given two copies of gene
        2: {
            True: 0.65,
            False: 0.35
        },

        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },

        # Probability of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        }
    },

    # Mutation probability
    "mutation": 0.01
}


def main():
    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    people = load_data(sys.argv[1])

    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people
    }

    # Loop over all sets of people who might have the trait
    names = set(people)
    for have_trait in powerset(names):

        # Check if current set of people violates known information
        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
            for person in names
        )
        if fails_evidence:
            continue

        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):
                # Update probabilities with new joint probability
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)

    # Ensure probabilities sum to 1
    normalize(probabilities)

    # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None)
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]


def joint_probability(people, one_gene, two_genes, have_trait):
    """
    Compute and return a joint probability.

    The probability returned should be the probability that
        * everyone in set `one_gene` has one copy of the gene, and
        * everyone in set `two_genes` has two copies of the gene, and
        * everyone not in `one_gene` or `two_gene` does not have the gene, and
        * everyone in set `have_trait` has the trait, and
        * everyone not in set` have_trait` does not have the trait.

    1. get situation of all people we want to calculate
    2. for each person in the set, compute the probability and times with total prob
        3. compute the probability that this person expresses trait and it's prob
        4. if the info of his parents is not available: compute the prob
        5. if it's available:
            6. get his parents' info
            7. for each situation of how many copies of gene this person carries, compute the prob
                helper function : we need a helper function to compute the prob that his parents gave
                a copied gene to him or not in all situation, including mutated
    """
    condition = {
        name: {
            "gene": 1 if name in one_gene else 2 if name in two_genes else 0,
            "trait": True if name in have_trait else False
        }
        for name in people.keys()
    }
    total_porb = 1
    for person in people:
        prob = 1
        prob_trait = PROBS["trait"][condition[person]["gene"]][condition[person]["trait"]]
        prob *= prob_trait

        if people[person]["mother"] is None:
            prob_trait_uncond = PROBS["gene"][condition[person]["gene"]]
            prob *= prob_trait_uncond

        else:
            mom = people[person]["mother"]
            dad = people[person]["father"]
            gene_num = condition[person]["gene"]
            mom_gene_num = condition[mom]["gene"]
            dad_gene_num = condition[dad]["gene"]
            if gene_num == 0:
                prob *= prob_gene_num(dad_gene_num, False) * prob_gene_num(mom_gene_num, False)
            elif gene_num == 1:
                p_from_dad = prob_gene_num(dad_gene_num, True) * prob_gene_num(mom_gene_num, False)
                p_from_mom = prob_gene_num(dad_gene_num, False) * prob_gene_num(mom_gene_num, True)
                prob *= (p_from_dad + p_from_mom)
            else:
                prob *= prob_gene_num(dad_gene_num, True) * prob_gene_num(mom_gene_num, True)
        total_porb *= prob
    return total_porb


def prob_gene_num(ori_gene, child_gene):
    # child got gene from parent
    if child_gene:
        if ori_gene == 0:
            # child got gene by mutated
            return PROBS["mutation"]
        if ori_gene == 1:
            # got the gene or got the good gene but mutated
            return 0.5 + 0.5 * PROBS["mutation"]
        if ori_gene == 2:
            return 1 - PROBS["mutation"]
    # child did not get gene from parent
    else:
        if ori_gene == 0:
            return 1 - PROBS["mutation"]
        if ori_gene == 1:
            return 0.5 + 0.5 * PROBS["mutation"]
        if ori_gene == 2:
            return PROBS["mutation"]


def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """
    condition = {
        name: {
            "gene": 1 if name in one_gene else 2 if name in two_genes else 0,
            "trait": True if name in have_trait else False
        }
        for name in probabilities.keys()
    }
    for name in probabilities.keys():
        probabilities[name]["gene"][condition[name]["gene"]] += p
        probabilities[name]["trait"][condition[name]["trait"]] += p


def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """
    for name in probabilities.keys():
        normalizer = sum(probabilities[name]["gene"].values())
        for gene in probabilities[name]["gene"]:
            probabilities[name]["gene"][gene] /= normalizer

        normalizer = sum(probabilities[name]["trait"].values())
        for trait in probabilities[name]["trait"]:
            probabilities[name]["trait"][trait] /= normalizer


if __name__ == "__main__":
    main()
