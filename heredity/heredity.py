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
    """
    def _check_if_child(person):
        return people[person]["mother"] is not None and people[person]["father"] is not None 

    def _get_num_genes(person):
        if person in two_genes:
            return 2
        elif person in one_gene:
            return 1
        return 0

    info = {
        2: (PROBS["mutation"], 1 - PROBS["mutation"]),
        1: (0.5, 0.5),
        0: (1-PROBS["mutation"], PROBS["mutation"]) 
    }

    joint_prob = 1
    for person in people:
        person_num_genes = _get_num_genes(person)
        # 1. check if person is a parent or a child
        if _check_if_child(person):
            mother, father = people[person]["mother"], people[person]["father"]
            mother_info = info[_get_num_genes(mother)]
            father_info = info[_get_num_genes(father)]

            if person in two_genes:
                prob = mother_info[1] * father_info[1]
            elif person in one_gene:
                prob = mother_info[0] * father_info[1] + mother_info[1] * father_info[0]
            else:
                # 1. mother 0 genes and does not mutate & father 0 genes and does not mutate ---> (1-PROBS["mutation"]) * PROBS["mutation"]
                # 2. mother 0 genes and does not mutate & father 1 gene and does not pass.   ---> (1-PROBS["mutation"]) * 0.5 
                # 3. mother 0 genes and does not mutate & father 2 genes and mutates (i.e. does not pass) ---> (1-PROBS["mutation"]) * PROBS["mutation"]
                # 4. mother 1 gene and does not pass & father 0 genes and does not mutate ---> 0.5 * PROBS["mutation"]
                # 5. mother 1 gene and does not pass & father 1 genes and does not pass ---> 0.5 * 0.5
                # 6. mother 1 gene and does not pass & father 2 genes and mutates (i.e. does not pass) ---> 0.5 * PROBS["mutation"]
                # 7. mother 2 genes and mutates (i.e. does not pass) & father 0 genes and does not mutate ---> PROBS["mutation"] * (1-PROBS["mutation"])
                # 8. mother 2 genes and mutates (i.e. does not pass) & father 1 gene and does not pass ---> PROBS["mutation"] * 0.5
                # 9. mother 2 genes and mutates (i.e. does not pass) & father 2 genes and mutates ---> PROBS["mutation"] * PROBS["mutation"]
                prob = mother_info[0] * father_info[0]
            
            joint_prob *= prob * PROBS["trait"][person_num_genes][person in have_trait]
        else:
            joint_prob *= PROBS["gene"][person_num_genes] * PROBS["trait"][person_num_genes][person in have_trait]

    return joint_prob

def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """
    for person in probabilities:
        if person in one_gene:
            gn = 1
        elif person in two_genes:
            gn = 2
        else:
            gn = 0

        probabilities[person]["gene"][gn] += p
        probabilities[person]["trait"][person in have_trait] += p

def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """
    for person in probabilities:
        total_prob = sum([probabilities[person]["gene"][x] for x in [0, 1, 2]])
        for x in [0, 1, 2]:
            probabilities[person]["gene"][x] /= total_prob
        
        total_prob = sum([probabilities[person]["trait"][x] for x in [True, False]])
        for x in [True, False]:
            probabilities[person]["trait"][x] /= total_prob


if __name__ == "__main__":
    main()
    # people = {
    #     'Harry': {'name': 'Harry', 'mother': 'Lily', 'father': 'James', 'trait': None},
    #     'James': {'name': 'James', 'mother': None, 'father': None, 'trait': True},
    #     'Lily': {'name': 'Lily', 'mother': None, 'father': None, 'trait': False}
    # }
    # joint_prob = joint_probability(people, {"Harry"}, {"James"}, {"James"})
    # print(joint_prob)
