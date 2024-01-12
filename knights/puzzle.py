from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And(
    Or(AKnight, AKnave), # either one is correct (inclusive or)
    Not(And(AKnight, AKnave)), # cannot be both 
    Biconditional(AKnight, Not(And(AKnight, AKnave))), # A is a Knight <=> it cannot be both
    # Biconditional(AKnave, And(AKnight, AKnave)) # A is a Knave <=> it can be both
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
    ###################################
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),
    Or(BKnight, BKnave),
    Not(And(BKnight, BKnave)),
    ###################################
    Implication(AKnave, Not(And(AKnave, BKnave))), # if A is a Knave, then they cannot be both knaves
    Implication(AKnight, And(AKnave, BKnave)), # if A is a Knight, then they would be both knaves (contradiction)
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
    ###################################
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),
    Or(BKnight, BKnave),
    Not(And(BKnight, BKnave)),
    ###################################
    Implication(AKnight, And(AKnight, BKnight)),
    Implication(AKnave, Not(And(AKnave, BKnave))),
    Implication(BKnight, And(BKnight, AKnave)),
    Implication(BKnave, Not(And(BKnave, AKnight))),
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'." --> contradiction ---> lie ----> B is a knave
# B says "C is a knave."  ---> C is a knight
# C says "A is a knight." ---> A is a knight
knowledge3 = And(
    ####################################
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),
    Or(BKnight, BKnave),
    Not(And(BKnight, BKnave)),
    Or(CKnight, CKnave),
    Not(And(CKnight, CKnave)),
    ###################################
    Implication(BKnight, Implication(AKnave, AKnight)),
    Implication(BKnight, Implication(AKnight, AKnight)),
    Implication(BKnave, AKnight),

    Implication(BKnight, CKnave),
    Implication(BKnave, CKnight),
    
    Implication(CKnight, AKnight),
    Implication(CKnave, AKnave),

)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
