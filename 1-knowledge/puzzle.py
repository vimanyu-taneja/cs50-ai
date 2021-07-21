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

    Or(AKnight, AKnave), # A must be either a Knight or a Knave, obviously

    Not(And(AKnight, AKnave)), # A cannot be both a Knight and a Knave at the same time, obviously

    Implication(AKnight, And(AKnight, AKnave)), # If A is a Knight, then A is a Knight and A is a Knave because Knights tell the truth

    Implication(AKnave, Not(And(AKnight, AKnave))) # If A is a Knave, then A cannot be both a Knight and a Knave because Knaves lie
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(

    Or(AKnight, AKnave), # A must be either a Knight or a Knave, obviously

    Not(And(AKnight, AKnave)), # A cannot be both a Knight and a Knave at the same time, obviously

    Or(BKnight, BKnave), # A must be either a Knight or a Knave, obviously

    Not(And(BKnight, BKnave)), # B cannot be both a Knight and a Knave at the same time, obviously

    Or(And(AKnight, BKnave), And(AKnave, BKnight)), # A and B cannot both be the same character, obviously

    Implication(AKnight, And(AKnave, BKnave)), # If A is a Knight, then both A and B are Knaves because Knights tell the truth

    Implication(AKnave, Not(And(AKnave, BKnave))) # If A is a Knave, then both A and B are not Knaves because Knaves lie
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(

    Or(AKnight, AKnave), # A must be either a Knight or a Knave, obviously

    Not(And(AKnight, AKnave)), # A cannot be both a Knight and a Knave at the same time, obviously

    Or(BKnight, BKnave), # A must be either a Knight or a Knave, obviously

    Not(And(BKnight, BKnave)), # B cannot be both a Knight and a Knave at the same time, obviously

    Or(And(AKnight, BKnave), And(AKnave, BKnight)), # A and B cannot both be the same character, obviously

    Implication(AKnight, And(AKnight, BKnight)), # If A is a Knight, then both A and B must be Knights because Knights tell the truth, and A said that both A and B are the same character

    Implication(AKnave, Not(And(AKnave, BKnave))), # If A is a Knave, then both A and B cannot be Knaves because Knaves lie, and A said that both A and B are the same character

    Implication(BKnight, And(BKnight, AKnave)), # If B is a Knight, then A is a Knave and B is Knight because Knights tell the truth

    Implication(BKnave, Not(And(BKnave, AKnight))) # If B is a Knave, then A cannot be a Knight, i.e. of a different kind to B, because Knaves lie
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(

    Or(AKnight, AKnave), # A must be either a Knight or a Knave, obviously

    Not(And(AKnight, AKnave)), # A cannot be both a Knight and a Knave at the same time, obviously

    Or(BKnight, BKnave), # A must be either a Knight or a Knave, obviously

    Not(And(BKnight, BKnave)), # B cannot be both a Knight and a Knave at the same time, obviously

    Or(CKnight, CKnave), # C must be either a Knight or a Knave, obviously

    Not(And(CKnight, CKnave)), # C cannot be both a Knight and a Knave at the same time, obviously

    # A says either "I am a knight." or "I am a knave.", but you don't know which.
    Or( # Either... or...

        # A says "I am a knight."
        And(
            Implication(AKnight, AKnight), # If A is a Knight and he says that he is a Knight, then he is actually a Knight, because Knights tell the truth

            Implication(AKnave, Not(AKnight)) # If A is a Knave and he says that he is a Knight, then he is actually a Knave, i.e. not a Knight, because Knaves lie
        ),
        
        # A says "I am a knave."
        And(
            Implication(AKnight, AKnave), # If A is a Knight and he says that he is a Knave, then he is actually a Knave, because Knights tell the truth

            Implication(AKnave, Not(AKnave)) # If A is a Knave and he says that he is a Knave, then he is actually a Knight, i.e. not a Knave, because Knaves lie
        )
    ),

    # A says that he is either a knight or a knave, not both
    Not(And(
    
        # A says "I am a knight."
        And(
            Implication(AKnight, AKnight), # If A is a Knight and he says that he is a Knight, then he is actually a Knight, because Knights tell the truth

            Implication(AKnave, Not(AKnight)) # If A is a Knave and he says that he is a Knight, then he is actually a Knave, i.e. not a Knight, because Knaves lie
        ),
        
        # A says "I am a knave."
        And(
            Implication(AKnight, AKnave), # If A is a Knight and he says that he is a Knave, then he is actually a Knave, because Knights tell the truth

            Implication(AKnave, Not(AKnave)) # If A is a Knave and he says that he is a Knave, then he is actually a Knight, i.e. not a Knave, because Knaves lie
        )
    )),

    # B says "A said I am a knave"."

    Implication(BKnight, And( # If B is a Knight and B says "A said I am a knave", then, because Knights tell the truth, the following implications are true

        Implication(AKnight, AKnave), # If A is a Knight, then A is a Knave, because Knights tell the truth

        Implication(AKnave, Not(AKnave)) # If A is a Knave, then A is a Knight, i.e. not a Knave, because Knaves lie
    )),

    Implication(BKnave, Not(And( # If B is a Knave and B says "A said I am a knave", then, because Knaves tell lies, the following implications are false

        Implication(AKnight, AKnave), # If A is a Knight, then A is a Knave, because Knights tell the truth

        Implication(AKnave, Not(AKnave)) # If A is a Knave, then A is a Knight, i.e. not a Knave, because Knaves lie
    ))),


    # B says "C is a knave."

    Implication(BKnight, CKnave), # If B is a Knight and says that C is a Knave, then C must be a Knave as Knights tell the truth

    Implication(BKnave, Not(CKnave)), # If B is a Knave and says that C is a Knave, then C must be a Knight, i.e. not a Knave, because Knaves lie

    # C says "A is a knight."

    Implication(CKnight, AKnight), # If C is a Knight and says that A is a Knight, then A must be a Knight, as Knights tell the truth

    Implication(CKnave, Not(AKnight)) # If C is a Knave and says that A is a Knight, then A must be a Knave, i.e. not a Knight, because Knaves lie
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
