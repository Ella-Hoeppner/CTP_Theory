"""This file contains functions relating to minds. The primary elements of a mind are theories, claims, and problems, but minds also contain some supplementary elements.

A mind is a list of length 6, [theories, routines, claims, claim_records, claim_hash_table, problems]
-theories is a list of theories
-routine is a list of routines
-claims is a list of claims
-claim_records is a list of claim records
-claim_hash_table is a list of lists of ints, which is used as a hashtable for quickly searching for claims with identical lists.
-problems is a list of problems
"""

import language
import extract
import conjecture
from numpy.random import random

def new_mind(theories=[], routines=[], claims=[],hash_table_size=1000):
  """Creates a new mind, which is empty by default, but can optionally be started with a set of theories, routines, or claims.

  Args:
    theories (list): Defaults to an empty list. The set of theories that the mind will start off with.
    routines (list): Defaults to an empty list. The set of routines that the mind will start off with.
    claims (list): Defaults to an empty list. The set of claims that the mind will start off with.
    hash_table_size (int): Defaults to 1000. The size of the hash table which will be used to quickly check for contradictions between claims. Claims are placed into the hash table based on their integer lists so that claims with the same integer lists will fall into the same location. A higher number will make it less likely that different integer lists fall into the same location, but it also requires more memory.

  Returns:
    The new mind, as a list.
  """
  return[
    theories,
    routines,
    claims,
    [(-1,[]) for claim in claims],
    [[] for i in range(hash_table_size)],
    []
  ]

def mind_string(mind, show_theories=True, show_routines=True, show_claims=True, show_problems=True):
  """Creates a human-readable string that describes a mind. Takes several flags to customize what information is shown.

  Args:
    mind (list): The mind to create a string for.
    show_theories (bool): Defaults to True. If this is True, the string will contain a description of all the theories in the mind.
    show_routines (bool): Defaults to True. If this is True, the string will contain a description of all the routines in the mind.
    show_claims (bool): Defaults to True.  If this is True, the string will contain a description of all the claims in the mind.
    show_problems (bool): Defaults to True.  If this is True, the string will contain a description of all the problems in the mind.

  Returns:
  """
  string=""
  if show_theories:
    string+="THEORIES:\n"
    for i in range(len(mind[0])):
      string+=str(i)+":\n"+language.program_string(mind[0][i])+"\n"
  if show_routines:
    string+="\nROUTINES:\n"
    for i in range(len(mind[1])):
      string+=str(i)+":\n"+language.program_string(mind[1][i])+"\n"
  if show_claims:
    string+="\nCLAIMS:\n"
    for i in range(len(mind[2])):
      string+=str(i)+":\n"+str(mind[2][i])+"\nfrom:"+str(mind[3][i])+"\n\n"
  if show_problems:
    string+="\nPROBLEMS:\n"
    for i in range(len(mind[5])):
      string+=str(i)+":\n"+str(mind[5][i])+"\n\n"

  return string

def generate_claims(mind):
  """Randomly chooses a theory from the mind, and then use it with the population of claims in the mind to generate new claims.

  Args:
    mind (list): The mind to use to generate claims. A theory will be randomly chosen from the minds list of theories, and then executed with all of the claims in the mind as the input set. The resulting claims will then be added to the mind's list of claims.
  """
  chosen_theory_index=int(random()*len(mind[0]))
  outputs=language.run_theory(chosen_theory_index, mind[0], mind[1], mind[2])
  for output in outputs:
    touched_claim_indeces=output[0]
    claim=output[1]
    add_claim(mind, claim, (chosen_theory_index, touched_claim_indeces))

def add_claim(mind, claim, record):
  """Adds a claim to the mind's population of claims. This function will not add a claim if the claim and it's record are identical to a claim/record pair already present in the mind. This function also checks if the new claim contradicts any other claims in the mind, and creates a problem if so.
  
  Args:
    mind (list): The mind to add the claim to.
    claim (tuple): The claim to add to the mind.
    record (tuple): The record of the claim that will be added to the mind.
  """
  claim_index=len(mind[2])
  h=hash(tuple(claim[1]))%len(mind[4])
  problem_indeces=[]
  claim_unique=True
  for old_claim_index in mind[4][h]:
    # Check all claims at the same location in the hash table.
    claim2=mind[2][old_claim_index]
    if claim[1]==claim2[1]:
      # If the claims have the same int lists, see whether they have the same boolean values.
      if claim[0]==claim2[0]:
        if record==mind[3][old_claim_index]:
          # If the new claim is identical to an old one (both in int list and boolean value), and the records are identical, set "claim_unique" to False to designate that this new claim should not be added.
          claim_unique=False
          break
      else:
        # If the new claim has an identical int-list to an old one, but the boolean values are different, then the two claims are contradictory.
        problem_indeces.append(old_claim_index)
  if claim_unique:
    # If the claim is unique, add it to the mind.
    mind[2].append(claim)
    mind[3].append(record)
    # Add a problem for each claim that was found that contradicted the new one.
    for old_claim_index in problem_indeces:
      add_problem(mind, (claim_index, old_claim_index))
    # Record the claim in the hash table.
    mind[4][h].append(claim_index)

def extract_new_routines(mind, max_to_extract=-1):
  """Iteratively extracts new routines from the theories and routines present in the mind.

  Args:
    mind (list): The mind from which to extract routines.
    max_to_extract (int): Defaults to -1. This value is the maximum number of routines to extract before stopping this function. This function is not guaranteed to extract this number of routines, because it may not be possible to extract the given number of routines. If this value is -1, the function will continue until it is no longer possible to extract a routine.
  """
  extracted=0
  while max_to_extract==-1 or extracted<max_to_extract:
    output=extract.extract_new_routine(mind[0], mind[1], language.instruction_functions.index(language.instruction_exec), language.is_program_valid)
    if output==False:
      break
    mind[0]=output[0]
    mind[1]=output[1]
    extracted+=1

def replace_routine_instances(mind):
  """Applies extract.extract_routine_instances to the mind's theories. This will find all chunks of code that are identical to the implementation of a routine, and replace such chunks with the routine.

  Args:
    mind (list): The mind in which to find and replace the implementations of routines within theories.
  """
  mind[0]=extract.extract_routine_instances(mind[0], mind[1], language.instruction_functions.index(language.instruction_exec))

def inline_and_delete_all_routines(mind):
  """Erases all routines in the mind, and replaces each reference to a routine with the implementation of that routine.

  Args:
    mind (list): The mind in which to search for get rid of all routines, and inline their implementations into theories where necessary.
  """
  mind[0]=[language.inline_execs(i, mind[0], mind[1], inline_theories=False) for i in range(len(mind[0]))]
  mind[1]=[]

def inline_and_delete_underused_routines(mind):
  """This function counts the number of uses for each routine, and gets rid of the routines which are used less than twice. When a routine is removed, each reference to the routine will be replaced with the routine's implementation.

  Args:
    mind (list): The mind in which to search for and delete routines which are only used once.
  """

  # Find each reference to each theory in other theories and routines.
  theory_uses=[[] for i in range(len(mind[1]))]
  for i in range(len(mind[0])):
    theory=mind[0][i]
    for i2 in range(len(theory[1])):
      instruction=theory[1][i2]
      if language.instruction_functions[instruction[0]]==language.instruction_exec and instruction[1]>=0:
          theory_uses[instruction[1]]+=(i,i2)

  # Find each reference to each routine in other routines and theories.
  routine_uses=[[] for i in range(len(mind[1]))]
  for i in range(len(mind[1])):
    routine=mind[1][i]
    for i2 in range(len(routine[1])):
      instruction=routine[1][i2]
      if language.instruction_functions[instruction[0]]==language.instruction_exec and instruction[1]>=0:
          routine_uses[instruction[1]]+=(i,i2)

  # Find underused routines, and replace refernces to them with their implementation.
  underused_routines=[]
  for i in range(len(mind[1])):
    uses=len(theory_uses[i])+len(routine_uses[i])
    if uses<2:
      underused_routines.append(i)
      routine_to_inline=mind[1][i]
      for i2 in range(len(theory_uses)):
        theory_use=theory_uses[i2]
        theory=mind[0][theory_use[0]]
        mind[0][theory_use]=theory[:theory_use[1]]+routine_to_inline+theory[theory_use[1]+1:]
      for i2 in range(len(routine_uses)):
        routine_use=routine_uses[i2]
        routine=mind[1][routine_use[0]]
        mind[1][routine_use]=routine[:routine_use[1]]+routine_to_inline+routine[routine_use[1]+1:]
  
  delete_routines(mind, underused_routines[i])

def delete_routines(mind, routines):
  """Removes some set of routines from the mind's population of routines. This function updates all references to routines that are affected by the change.

  Args:
    mind (list): The mind in which to delete routines.
    routines (list): A list of integers containing the indeces of the routines that will be deleted.
  """
  exec_instruction=language.instruction_functions.index(language.instruction_exec)
  for i in range(len(routines)):
    routine_index=routines[i]-i
    mind[1]=mind[1][:routine_index]+mind[1][routine_index+1:]
    for program in mind[0]+mind[1]:
      for i2 in range(len(program)):
        instruction=program[i2]
        if instruction[0]==exec_instruction and instruction[1]>routine_index:
          program[i2]=(exec_instruction, instruction[1]-1)

def add_problem(mind, claims):
  """Adds a problem to the mind's population of problems. A problem consists of a pair of traces that describe the way two contradictory claims were created.

  Args:
    mind (list): The mind to add the problem to.
    claims (tuple): A tuple of length 2 containing the two contradictory claims.
  """
  mind[5].append((get_claim_trace(mind,claims[0]), get_claim_trace(mind,claims[1])))

def get_claim_trace(mind, claim):
  """This function recursively traces backwards to determine the lineage of a claim. It returns a claim trace, a nested tuple describing how 

  Args:
    mind (list): The mind that contains the claim to be traced.
    claim (int): The index of the claim in the mind to get the claim trace of.
  """
  record=mind[3][claim]
  if record[0]==-1:
    return claim
  return tuple([record[0]]+[get_claim_trace(mind, subclaim) for subclaim in record[1]])