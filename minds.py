import language
import extract
import conjecture
from numpy.random import random

"""
A mind is a list of length 6, [theories, routines, claims, claim_records, claim_hash_table, problems]
-theories is a list of theories
-routine is a list of routines
-claims is a list of claims
-claim_records is a list of claim records
-claim_hash_table is a list of lists of ints, which is used as a hashtable for quickly searching for claims with identical lists.
-problems is a list of problems
"""

def new_mind(theories=[], routines=[], claims=[],hash_table_size=1000):
  """Creates a new, empty mind."""
  return[
    theories,
    routines,
    claims,
    [(-1,[]) for claim in claims],
    [[] for i in range(hash_table_size)],
    []
  ]

def mind_string(mind, show_theories=True, show_routines=True, show_claims=True, show_problems=True):
  """Creates a human-readable string that describes a mind. Takes several flags to customize what information is shown."""
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
  """Randomly chooses a theory from the mind, and then use it with the population of claims in the mind to generate new claims."""
  chosen_theory_index=int(random()*len(mind[0]))
  outputs=language.run_theory(chosen_theory_index, mind[0], mind[1], mind[2])
  for output in outputs:
    touched_claim_indeces=output[0]
    claim=output[1]
    add_claim(mind, claim, (chosen_theory_index, touched_claim_indeces))

def add_claim(mind, claim, record):
  """Adds a claim to the mind's population of claims. This function will not add a claim if the claim and it's record are identical to a claim/record pair already present in the mind. This function also checks if the new claim is contradictory with any other claims in the mind, and creates a problem if so."""
  claim_index=len(mind[2])
  h=hash(tuple(claim[1]))%len(mind[4])
  problem_indeces=[]
  claim_unique=True
  for old_claim_index in mind[4][h]:
    claim2=mind[2][old_claim_index]
    if claim[1]==claim2[1]:
      if claim[0]==claim2[0]:
        if record==mind[3][old_claim_index]:
          claim_unique=False
          break
      else:
        problem_indeces.append(old_claim_index)
  if claim_unique:
    mind[2].append(claim)
    mind[3].append(record)
    for old_claim_index in problem_indeces:
      add_problem(mind, (claim_index, old_claim_index))
    mind[4][h].append(claim_index)

def extract_new_routines(mind, max_to_extract=-1):
  """Iteratively extracts new routines from the theories and routines present in the mind."""
  extracted=0
  while max_to_extract==-1 or extracted<max_to_extract:
    output=extract.extract_new_routine(mind[0], mind[1], language.instruction_functions.index(language.instruction_exec), language.is_program_valid)
    if output==False:
      break
    mind[0]=output[0]
    mind[1]=output[1]
    extracted+=1

def replace_routine_instances(mind):
  """Applies extract.extract_routine_instances to the mind's theories."""
  mind[0]=extract.extract_routine_instances(mind[0], mind[1], language.instruction_functions.index(language.instruction_exec))

def inline_and_delete_all_routines(mind):
  """Erases all routines in the mind, and replaces each reference to a routine with the implementation of that routine."""
  mind[0]=[language.inline_execs(i, mind[0], mind[1], inline_theories=False) for i in range(len(mind[0]))]
  mind[1]=[]

def inline_and_delete_underused_routines(mind):
  """This function counts the number of uses for each routine, and gets rid of the routines which are used less than twice. When a routine is removed, each reference to the routine will be replaced with the routine's implementation."""
  theory_uses=[[] for i in range(len(mind[1]))]
  for i in range(len(mind[0])):
    theory=mind[0][i]
    for i2 in range(len(theory[1])):
      instruction=theory[1][i2]
      if language.instruction_functions[instruction[0]]==language.instruction_exec and instruction[1]>=0:
          theory_uses[instruction[1]]+=(i,i2)
  routine_uses=[[] for i in range(len(mind[1]))]
  for i in range(len(mind[1])):
    routine=mind[1][i]
    for i2 in range(len(routine[1])):
      instruction=routine[1][i2]
      if language.instruction_functions[instruction[0]]==language.instruction_exec and instruction[1]>=0:
          routine_uses[instruction[1]]+=(i,i2)
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
  """Removes some set of routines from the mind's population of routines. This function updates all references to routines that are affected by the change."""
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
  """Adds a problem to the mind's population of problems. A problem consists of a pair of traces that describe the way two contradictory claims were created."""
  mind[5].append((get_claim_trace(mind,claims[0]), get_claim_trace(mind,claims[1])))

def get_claim_trace(mind, claim):
  """This function recursively traces backwards to determine the lineage of a claim."""
  record=mind[3][claim]
  if record[0]==-1:
    return claim
  return tuple([record[0]]+[get_claim_trace(mind, subclaim) for subclaim in record[1]])