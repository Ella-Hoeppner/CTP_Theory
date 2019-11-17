import language
from numpy.random import random
from numpy.random import geometric

'''MUTATION_TYPE_DISTRIBUTION is a distribution that controls the selection of mutation types. The three types are insertion, deletion, and inlining (replacing a referenced theory or routine with its implementation), and the distribution should contain three numbers corresponding to the likelihood of each type. The three numbers must sum to 1.'''
MUTATION_TYPE_DISTRIBUTION=[0.4,0.4,0.2]

'''INSERTION_TYPE_DISTRIBUTION is a distribution that controls the selection of insertion types in an insertion mutation. The three types of insertion are basic instruction insertion, theory insertion, and routine insertion, and the distribution should contain three numbers corresponding to the likelihood of each type. The three numbers must sum to 1.'''
INSERTION_TYPE_DISTRIBUTION=[0.9, 0.05, 0.05]

def vary(theories, theory_index, routines, steps=1):
  """Generates a variation on a given theory.

  Args:
    theories (list): The list of theories that can be referenced by the specified theory. This is also used, along with "theory_index", to determine which theory will be varied.
    theory_index (int): The index of the theory in "theories" that should be varied.
    routines (list): The list of routines that can be referenced by the specified theory.
    steps (int): Defaults to 1. This controls the number of iterations of variation the algorithm should perform on the input before returning. The higher this number is, the more different from the original theory the output will be.

  Returns:
    A new theory, which is created by randomly varying the provided theory.
  """
  theory=theories[theory_index]

  theory_count=len(theories)
  theory_distribution=[0 if i==theory_index else 1/(theory_count-1) for i in range(theory_count)]

  routine_count=len(routines)
  routine_distribution=[1/routine_count for i in range(routine_count)]

  instruction_count=len(language.instruction_functions)-1
  instruction_distribution=[1/instruction_count for i in range(instruction_count)]

  while steps>0:
    new_theory=theory[:]

    mutation_type=choose_from_distribution(MUTATION_TYPE_DISTRIBUTION)

    if mutation_type==0:
      #Insertion
      insertion_type=choose_from_distribution(INSERTION_TYPE_DISTRIBUTION)
      insertion_index=int(random()*(len(new_theory)+1))
      instruction=None
      insert_end=False
      if insertion_type==0:
        #Insert basic instruction
        instruction_index=choose_from_distribution(instruction_distribution)
        instruction_function=language.instruction_functions[instruction_index]
        instruction_arg_types=language.instruction_arg_types[instruction_function]
        instruction_args=[]
        for arg_type in instruction_arg_types:
          if arg_type=="int":
            instruction_args.append(generateRandomInt())
          if arg_type=="nonNegInt":
            instruction_args.append(generateRandomNonNegInt())
        instruction=tuple([instruction_index]+instruction_args)
        if instruction_function in language.block_starter_instructions:
          insert_end=True
      if insertion_type==1:
        #Insert theory
        if len(theories)==1:
          continue
        chosen_theory_index=choose_from_distribution(theory_distribution)
        instruction=(language.instruction_functions.index(language.instruction_exec), -(1+chosen_theory_index))
      if insertion_type==2:
        #Insert routine
        if len(routines)==0:
          continue
        instruction=(language.instruction_functions.index(language.instruction_exec),choose_from_distribution(routine_distribution))
      new_theory=new_theory[:insertion_index]+[instruction]+new_theory[insertion_index:]
      if insert_end:
        end_index=min(insertion_index+1+geometric(p=0.5), len(new_theory))
        new_theory=new_theory[:end_index]+[(language.instruction_functions.index(language.instruction_end),)]+new_theory[end_index:]
    if mutation_type==1:
      #Deletion
      if len(new_theory)==0:
        continue
      else:
        deletion_index=int(random()*len(new_theory))
        instruction_function=language.instruction_functions[new_theory[deletion_index][0]]
        new_theory=new_theory[:deletion_index]+new_theory[deletion_index+1:]
        if instruction_function in language.block_starter_instructions:
          depth=1
          for i in range(deletion_index, len(new_theory)):
            instruction_function_2=language.instruction_functions[new_theory[i][0]]
            if instruction_function_2 in language.block_starter_instructions:
              depth+=1
            if instruction_function_2 == language.instruction_end:
              depth-=1
            if depth==0:
              new_theory=new_theory[:i]+new_theory[i+1:]
              break
      
      if instruction_function == language.instruction_end:
        depth=1
        for i in range(deletion_index-1, -1, -1):
          instruction_function_2=language.instruction_functions[new_theory[i][0]]
          if instruction_function_2 in language.block_starter_instructions:
            depth-=1
          if instruction_function_2 == language.instruction_end:
            depth+=1
          if depth==0:
            new_theory=new_theory[:i]+new_theory[i+1:]
            break

    if mutation_type==2:
      #Inline
      exec_indeces=[]
      for i in range(len(new_theory)):
        if language.instruction_functions[new_theory[i][0]]==language.instruction_exec:
          exec_indeces.append(i)
      if len(exec_indeces)==0:
        continue
      exec_index=exec_indeces[int(random()*len(exec_indeces))]
      exec_function_index=new_theory[exec_index][1]
      if exec_function_index>=0:
        new_theory=new_theory[:exec_index]+routines[exec_function_index]+new_theory[exec_index+1:]
      else:
        exec_theory_index=-1-exec_function_index
        new_theory=new_theory[:exec_index]+theories[exec_theory_index]+new_theory[exec_index+1:]
    
    if language.is_program_valid(new_theory):
      theory=new_theory
      steps-=1

  return theory

def choose_from_distribution(d):
  """Given a list of non-negative numbers that sum to 1, this function randomly returns the index of one of the numbers. The probability of a given index being chosen is equal to the number in the list at that index.

  Args:
    d (list): A list of numbers that sum to 1. This list describes a probability distribution, where each integer greater than or equal to 0 and less than the length of "d" is assigned probability equal to the number in the list at the corresponding index.

  Returns:
    An integer greater than or equal to 0 and less than the length of "d". The integer will be chosen according to the probabilities that "d" describes.
  """
  choice_value=random()
  for i in range(len(d)):
    choice_value-=d[i]
    if choice_value<=0:
      return i
  return -1

def generateRandomNonNegInt():
  """Generates a random integer that is greater than or equal to 0. Uses a geometric distribution.

  Returns:
    A value chosen using a geometric distribution with p=5, starting  at 0.
  """
  return geometric(p=0.5)

def generateRandomInt():
  """Generates a random integer. Uses a geometric distribution.

  Returns:
    An integer that is chosen that has a 50% chance of being 0 or greater, and a 50% chance of being negative.
  """
  if random()>0.5:
    return geometric(p=0.5)
  else:
    return -(1+geometric(p=0.5))