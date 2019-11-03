def get_max_character(strings):
  """Given a list of "strings" (really, lists of integers), this function finds the highest "character" (really, an integer) in any of the strings."""
  m=0
  for string in strings:
    for char in string:
      if char>m:
        m=char
  return m

def concat_with_separator(strings, starting_separator):
  """Concatenates a list of "strings" (really, lists of integers) using a given separator character (really, an integer)."""
  s=[]
  for i in range(len(strings)):
    s+=strings[i]+[starting_separator+i]
  return s

def get_longest_valid_repeated_nonoverlapping_substring(string, validity_function):
  """Uses dynamic programming to find the longest nonoverlapping substring in a given string (really, a list of integers) that passes the specified validity function."""
  string_length=len(string) 
  table=[[0 for i2 in range(string_length+1)] for i in range(string_length+1)] 

  repeated_substring_length=0
  repeated_substring=[]
  for i in range(1, string_length+1): 
    for i2 in range(i+1, string_length+1): 
      if (string[i-1]==string[i2-1] and table[i-1][i2-1]<(i2-i)): 
        table[i][i2]=table[i-1][i2-1]+1
        if table[i][i2]>repeated_substring_length:
          candidate_string=string[i-table[i][i2]:i]
          if validity_function(candidate_string):
            repeated_substring_length=table[i][i2]
            repeated_substring=candidate_string
      else: 
        table[i][i2]=0

  return repeated_substring 

def replace_instance(s, to_replace, replacement):
  """Replaces each instance of to_replace in s with replacement"""
  index=0
  matchedIndeces=0
  while index<len(s):
    if s[index]==to_replace[matchedIndeces]:
      matchedIndeces+=1
      if matchedIndeces>=len(to_replace):
        s=s[:index-(matchedIndeces-1)]+replacement+s[index+1:]
        index-=matchedIndeces-1
        matchedIndeces=0
    else:
      matchedIndeces=0
    index+=1
  return s

def extract_int_function(programs, replacement_marker, validity_function):
  """Given a list of programs, expressed as lists of integers, this function finds the longest repeated valid substring and extracts it as a function. Instances of the function's implementation are replaced with references to the function."""
  maxInstruction=get_max_character(programs)

  fullString=concat_with_separator(programs, maxInstruction+1)
  
  function=get_longest_valid_repeated_nonoverlapping_substring(fullString, validity_function)

  if len(function)<2:
    return ([], programs)

  return (function, [replace_instance(program, function, [replacement_marker]) for program in programs])

def tuple_int_translator(tuples):
  """Given a set of tuples, this function creates a dictionary that maps each unique tuple to a unique integer, starting from 1."""
  currentIndex=0
  d={}
  for t in tuples:
    if t not in d.keys():
      d[t]=currentIndex
      currentIndex+=1
  return d

def extract_tuple_function(programs, replacement_marker, validity_function):
  """Given a list of programs, expressed as tuples, this function will translate the functions to integer expressions using tuple_int_translator, call extract_int_function to extract a function, and then convert everything back to tuple-form and return it."""
  flat_programs=[]
  for p in programs:
    flat_programs+=p

  d=tuple_int_translator(flat_programs)
  reverse_d={v: k for k, v in d.items()}
  reverse_d[-1]=replacement_marker

  int_programs=[[d[t] for t in p] for p in programs]

  def int_validity_function(program):
    tuple_program=[reverse_d[i] for i in program]
    return validity_function(tuple_program)

  function, new_int_programs=extract_int_function(int_programs, -1, int_validity_function)

  tuple_function=[reverse_d[i] for i in function]

  new_programs=[[reverse_d[i] for i in p] for p in new_int_programs]

  return new_programs, tuple_function

def extract_new_routine(theories, routines, exec_routine_instruction_index, validity_function):
  """Given a list of theories and routines, this function attempts to extract a new routine using extract_tuple_function."""
  new_programs, function=extract_tuple_function(theories+routines, (exec_routine_instruction_index,len(routines)),validity_function)
  if function==[]:
    return False
  theory_count=len(theories)
  return ([new_programs[i] for i in range(theory_count)], [new_programs[i] for i in range(theory_count, len(new_programs))]+[function])

def extract_routine_instances(theories, routines, exec_routine_instruction_index):
  """Finds instances in theories where the a chunk of code identical to the implementation of some routine is present, and replaces that chunk of code with a reference to the routine."""
  new_theories=[]
  for theory in theories:
    for i in range(len(routines)):
      routine=routines[i]
      theory=replace_instance(theory,routine,[(exec_routine_instruction_index,i)])
    new_theories.append(theory)
  return new_theories