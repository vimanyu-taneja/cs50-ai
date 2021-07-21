import sys
import copy

from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        w, h = draw.textsize(letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        # Iterate through the domain
        for variable in self.crossword.variables:

            # Iterate through the words in the domain
            for word in self.crossword.words:

                # If the length of the word does not equal the length of the variable
                if len(word) != variable.length:

                    # Delete the word from the domain
                    self.domains[variable].remove(word)

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.
        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        # Get the overlapping cells
        overlap = self.crossword.overlaps[x, y]

        # Unpack co-ordinates to variables
        x_overlap, y_overlap = overlap

        # Make a copy of the domains
        domains_copy = copy.deepcopy(self.domains)

        # If there is no overlap
        if overlap is None:

            # No revision is made
            made_revision = False

        # If there is overlap
        else:

            # Iterate through the words in the x-domain
            for x_word in domains_copy[x]:
                possible_overlap = False

                # Iterate through the words in the y-domain
                for y_word in self.domains[y]:

                    # if the x word and the y word have same letter in the same (overlapping) position
                    if x_word[x_overlap] == y_word[y_overlap]:

                        possible_overlap = True

                        # There is no need to check the rest of words from y for that word of x
                        break
              
                # If the x and y matched, proceed with another x word
                if possible_overlap:
                    continue
                else:

                    # If there is no matching y word to the selected x word, remove the x word from the domain
                    self.domains[x].remove(x_word)
                    made_revision = True
        
        # Return a boolean which represents whether or not a revision was made
        return made_revision

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.
        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """

        # If `arcs` is None, begin with initial list of all arcs in the problem
        if not arcs:
            arcs = []

            # Populate the list of initial arcs
            for variable1 in self.crossword.variables:
                for variable2 in self.crossword.neighbors(variable1):
                    if self.crossword.overlaps[variable1, variable2] is not None:
                        arcs.append((variable1, variable2))

        while len(arcs) > 0:
            x, y = arcs.pop(0)
            if self.revise(x, y):
                if len(self.domains[x]) == 0:
                    return False
                for neighbour in self.crossword.neighbors(x):
                    if neighbour != y:
                        arcs.append((neighbour, x))
            return True

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        for variable in self.domains:
            if variable not in assignment:
                return False
            if assignment[variable] not in self.crossword.words:
                return False
        return True

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """

        # Check if there are any conflicts between neighbouring variables, i.e. check overlap constraints
        for variable1 in assignment:
            for neighbour in self.crossword.neighbors(variable1):
                if neighbour in assignment:

                    overlap = self.crossword.overlaps[variable1, neighbour]
                    x_overlap, y_overlap = overlap
                    if assignment[variable1][x_overlap] != assignment[neighbour][y_overlap]:
                        return False

        # Check if every value is the correct length
        for variable2 in assignment:
            if variable2.length != len(assignment[variable2]):
                return False

        # Check if all values are distinct
        words = [*assignment.values()]
        if len(set(words)) != len(words):
            return False

        # If all constraints have been checked and there were no conflicts, then we can return True
        return True

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """

        # Store the neighbours of the given var
        neighbours = self.crossword.neighbors(var)

        
        # Initialise an empty dictionary for temporarily holding words
        temp_word_dict = {}


        # Iterate through the words of the given var
        for word in self.domains[var]:

            # Reset the number of ruled out words to zero
            ruled_out = 0

            # Iterate through the neighbours of the given var
            for variable in neighbours:

                # Don't count the neighbour if it has already been assigned a value
                if variable in assignment:
                    continue

                else:
                    # Get the overlap between the two variables and unpack the coordinates to variables
                    overlap = self.crossword.overlaps[var, variable]
                    x_overlap, y_overlap = overlap

                    # Iterate through the words of the neighbour variable
                    for variable_word in self.domains[variable]:

                        # Check for ruled out words in the words of the neighbour variable and update the 'ruled_out' counter accordingly
                        if variable_word[y_overlap] != word[x_overlap]:
                            ruled_out += 1

            # Add the ruled out words of the neighbour to the temporary dictionary initialised above
            temp_word_dict[word] = ruled_out

        # Sort the variables in the temporary dictionary by the number of ruled out words of each neighbour
        sorted_dict = {key: value for key, value in sorted(temp_word_dict.items(), key=lambda item:item[1])}

        return [*sorted_dict]

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        selection_dict = {}

        # Iterate through the variables in the domain
        for variable in self.domains:

            # Iterating through the variables in the assignment
            if variable not in assignment:

                # If variable is not yet in assignment, then add it to the selection dictionary initialised above
                selection_dict[variable] = self.domains[variable]

        # Make a list of variables sorted by number of remaining values
        sorted_list = [value for value, key in sorted(selection_dict.items(), key=lambda item:len(item[1]))]

        # Return an unassigned variable not already a part of 'assignment' with the minimum number of remaining values possible
        return sorted_list[0]

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.
        `assignment` is a mapping from variables (keys) to words (values).
        If no assignment is possible, return None.
        """
        # If the assignment is already ready, then just return it as it is
        if len(self.domains) == len(assignment):
            return assignment

        # Select one of the unassigned variables
        unassigned_variable = self.select_unassigned_variable(assignment)

        # Iterate through the words in the selected unassigned variable
        for value in self.domains[unassigned_variable]:

            # Update the variable value to the assignment
            assignment[unassigned_variable] = value

            # Check for consistency using the defined function
            if self.consistent(assignment):

                # Store the result of the new assignment backtrack
                backtrack_result = self.backtrack(assignment)
                if backtrack_result is not None:
                    return backtrack_result

        # If no assignment is possible, then return None
        return None


def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
