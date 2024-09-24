from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a knight and a knave."
p0_a = And(AKnight, AKnave)
knowledge0 = And(
    Or(AKnight, AKnave),
    Implication(AKnight, Not(AKnave)),
    Implication(AKnave, Not(AKnight)),
    Implication(AKnight, p0_a),
    Implication(AKnave, Not(p0_a))
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
p1_a = And(AKnave, BKnave)
knowledge1 = And(
    Or(AKnight, AKnave),
    Or(BKnight, BKnave),
    Implication(AKnight, Not(AKnave)),
    Implication(AKnave, Not(AKnight)),
    Implication(BKnight, Not(BKnave)),
    Implication(BKnave, Not(BKnight)),
    Implication(AKnight, p1_a),
    Implication(AKnave, Not(p1_a))
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
p2_a = Or(And(AKnight, BKnight), And(AKnave, BKnave))
p2_b = Or(And(AKnight, BKnave), And(AKnave, BKnight))
knowledge2 = And(
    Or(AKnight, AKnave),
    Or(BKnight, BKnave),
    Implication(AKnight, Not(AKnave)),
    Implication(AKnave, Not(AKnight)),
    Implication(BKnight, Not(BKnave)),
    Implication(BKnave, Not(BKnight)),
    Implication(AKnight, p2_a),
    # Implication(AKnight, Not(p2_b)),
    Implication(AKnave, Not(p2_a)),
    # Implication(AKnave, p2_b),
    Implication(BKnight, p2_b),
    # Implication(BKnight, Not(p2_a)),
    Implication(BKnave, Not(p2_b)),
    # Implication(BKnave, p2_a)
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# {A or B, but not both: (A ∨ B) ∧ ¬ (A ∧ B)}


# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."

# A said "I am a knight"
p3_asaid_Kni = And(
    Implication(AKnight, AKnight),
    Implication(AKnave, Not(AKnight))
)
# A said "I am a knave"
p3_asaid_Kna = And(
    Implication(AKnight, AKnave),
    Implication(AKnave, Not(AKnave))
)

p3_a1 = Or(p3_asaid_Kni, p3_asaid_Kna)

p3_b1 = And(Implication(BKnight, p3_asaid_Kna),
            Implication(BKnave, Not(p3_asaid_Kna)))
# p3_b1_1 = Implication(BKnave, Not(p3_asaid_Kna))
p3_b2 = CKnave
p3_c = AKnight
knowledge3 = And(

    Or(AKnight, AKnave),
    Or(BKnight, BKnave),
    Or(CKnight, CKnave),
    Implication(AKnight, Not(AKnave)),
    Implication(AKnave, Not(AKnight)),
    Implication(BKnight, Not(BKnave)),
    Implication(BKnave, Not(BKnight)),
    Implication(CKnight, Not(CKnave)),
    Implication(CKnave, Not(CKnight)),

    p3_a1,

    p3_b1,
    Implication(BKnight, p3_b2),
    Implication(BKnave, Not(p3_b2)),

    Implication(CKnight, p3_c),
    Implication(CKnave, Not(p3_c))
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
