"""This file contains functions for automatically extracting routines. A "routine" is a program that is never executed independently, but can be referenced by other theories or routines. The functions in this file are used to find chunks of code that appear several times in the theories in a mind, and create a routine that contains that chunk of code. The initial chunks of code can then be replaced with a reference to the routine, and references to routines can be inserted as part of conjecture.

The term "program" is used in this file to refer to either a theory or a routine. Theories and routines are both sequences of instructions, and they differ only in how they are used by the mind.

Programs in minds are normally represented as lists of tuples, but that format is not ideal for extracting routines, so most of the functions in this file expect programs to be represented as lists of integers. These lists of integers are thought of as strings, with each unique integer representing a different character. These are represented as lists of integers, rather than actual strings, because the number of characters is not known ahead of time. This file also contains functions for translating lists of tuples to lists of integers and vice versa, so that the other functions in this file can be used with programs expressed as lists of tuples.
"""

def get_max_character(strings):
  """Given a list of "strings" (really, lists of integers), this function finds the highest "character" (really, an integer) in any of the strings.

  Args:
    strings (list): A list of lists of integers. Each integer is treated like a character, and each list of integers is thus treated like a string.
  
  Returns:
    An integer equal to the largest integer that appears in any of the lists of integers in the input.
  """
  m=0
  for string in strings:
    for char in string:
      if char>m:
        m=char
  return m

def concat_with_separator(strings, starting_separator):
  """Concatenates a list of "strings" (really, lists of integers) using a given separator character (really, an integer).

  Args:
    strings (list): A list of lists of integers. Each integer is treated like a character, and each list of integers is thus treated like a string.
    starting_separator (int): An integer, which is used as a character, that will be the first character used to separate the strings when they are concatenated. A different separator will be used between each string, with each separator character being 1 greater than the last.

  Returns:
    A list of integers formed by concatenating each list in the "strings" with separator between each.
  """
  s=[]
  for i in range(len(strings)):
    s+=strings[i]+[starting_separator+i]
  return s

def get_longest_valid_repeated_nonoverlapping_substring(string, validity_function):
  """Uses dynamic programming to find the longest nonoverlapping substring in a given string (really, a list of integers) that passes the specified validity function.

  Args:
    string (list): A list of integers, which is interpreted as a string where each integer is a character.
    validity_function (function): A function that takes a list of integers as an input and returns a bool. This function is used to determine whether or not a string is valid: A string is valid if and only if this function returns True when that string is used as input.

  Returns:
    The longest substring in string which passes the validity function and which occurs at least twice (such that the two occurrences don't overlap) 
  """
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
  """Replaces each instance of to_replace in s with replacement

  Args:
    s (list): A list of integers, which will be interpreted as a string, in which instances of "to_replace" will be replaced with "replacement"
    to_replace (list): A list of integers, which will be interpreted as a string, and which will be replaced wherever it occurs in "s".
    replacement (list): A list of integers, which will be interpreted as a string, and which will be used to replace "to_replace" in "s".

  Returns:
    A version of "s" in which each instance of "to_replace" has been replaced with "replacement".
  """
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
  """Given a list of programs, expressed as lists of integers, this function finds the longest repeated valid substring and extracts it as a function. Instances of the function's implementation are replaced with references to the function.

  Args:
    programs (list): A list of lists of integers, such that each list of integers describes a program.
    replacement_marker (int): An integer that will be used to mark the location in each program where the extracted function was removed.
    validity_function (function): A function that takes in a list of integers and returns a bool.

  Returns:
    A tuple (function, new_programs)
      function (list): A list of integers describing the function that was extracted from "programs"
      new_programs (list): A list of lists of integers. This will be a modified version of the "programs" input in which each instance of the extracted function is replaced with "replacement_marker"
  """
  maxInstruction=get_max_character(programs)

  fullString=concat_with_separator(programs, maxInstruction+1)
  
  function=get_longest_valid_repeated_nonoverlapping_substring(fullString, validity_function)

  if len(function)<2:
    return ([], programs)

  return (function, [replace_instance(program, function, [replacement_marker]) for program in programs])

def tuple_int_translator(tuples):
  """Given a set of tuples, this function creates a dictionary that maps each unique tuple to a unique integer, starting from 1.

  Args:
    tuples (list): A list of tuples for which a translator will be created.

  Returns:
    A dictionary containing each unique tuple in "tuples" as a key. Each unique "tuple" in tuples is mapped to a unique integer.
  """
  currentIndex=0
  d={}
  for t in tuples:
    if t not in d.keys():
      d[t]=currentIndex
      currentIndex+=1
  return d

def extract_tuple_function(programs, replacement_marker, validity_function):
  """Given a list of programs, expressed as tuples, this function will translate the functions to integer expressions using tuple_int_translator, call extract_int_function to extract a function, and then convert everything back to tuple-form and return it.

  Args:
    programs (list): A list of lists of tuples of integers. Each tuple describes an instruction, and each list of tuples this describes a program.
    replacement_marker (tuple): A tuple that will be used to replace the extracted function in each program.
    validity_function (function): A function that takes a list of tuples of integers as an input and returns a bool.

  Returns:
    A tuple (new_programs, tuple_function)
      new_programs (list): A list of lists of tuples of integers. This will be a modified version of the "programs" input in which each instance of the extracted function is replaced with "replacement_marker"
      function (list): A list of tuples of integers describing the function that was extracted from "programs".
    """

  flat_programs=[]
  for p in programs:
    flat_programs+=p

  # Create a dictionary that will be used to translate lists of tuples to list of integers, and an inverse dictionary to translate in the reverse way.
  d=tuple_int_translator(flat_programs)
  reverse_d={v: k for k, v in d.items()}
  reverse_d[-1]=replacement_marker

  int_programs=[[d[t] for t in p] for p in programs]

  # Define a new validity function that works on lists of integers rather than lists of tuples, using the provided validity function.
  def int_validity_function(program):
    tuple_program=[reverse_d[i] for i in program]
    return validity_function(tuple_program)

  function, new_int_programs=extract_int_function(int_programs, -1, int_validity_function)

  tuple_function=[reverse_d[i] for i in function]

  new_programs=[[reverse_d[i] for i in p] for p in new_int_programs]

  return new_programs, tuple_function

def extract_new_routine(theories, routines, exec_routine_instruction_index, validity_function):
  """Given a list of theories and routines, this function attempts to extract a new routine using extract_tuple_function.

  Args:
    theories (list): A list of lists of tuples of integers, such that each list of tuples describes a program.
    routines (list): A list of lists of tuples of integers, such that each list of tuples describes a program.
    exec_routine_instruction_index (int): The index of the exec instruction. This is used to replace instances of the extracted function with a reference to them.
    validity_function (function): Takes a program (a list of lists of tuples of integers) as an input and returns a bool. This is used to determine whether a series of instructions is valid as an independent function.

  Returns:
    A tuple (new_theories, new_routines):
      new_theories (list): A list of lists of tuples of integers. Each list is a modified version of the corresponding list in "theories", with each instance of the extracted function being replaced with a reference to it
      new_routines (list): A list of lists of tuples of integers. Each list, except for the last, is a modified version of the corresponding list in "routines", with each instance of the extracted function being replaced with a reference to it. The last list in this list is the extracted function.
  """
  new_programs, function=extract_tuple_function(theories+routines, (exec_routine_instruction_index,len(routines)),validity_function)
  if function==[]:
    return False
  theory_count=len(theories)
  return ([new_programs[i] for i in range(theory_count)], [new_programs[i] for i in range(theory_count, len(new_programs))]+[function])

def extract_routine_instances(theories, routines, exec_routine_instruction_index):
  """Finds instances in theories where the a chunk of code identical to the implementation of some routine is present, and replaces that chunk of code with a reference to the routine.

  Args:
    theories (list): A list of lists of tuples of integers. This list will be searched for instances of the implementation of each routine, and found instances will be replaced with references to the routines.
    routines (list): A list of lists of tuples of integers. This list contains each routine which will be searched for in each theory.
    exec_routine_instruction_index (int): The index of the exec instruction. This is used to replace instances of the extracted function with a reference to them.
  Returns:
    A list of lists of tuples of integers. This is a modified version of "theories" in which each program has each instance of the implementation of a routine replaced with a reference to that routine.
  """
  new_theories=[]
  for theory in theories:
    for i in range(len(routines)):
      routine=routines[i]
      theory=replace_instance(theory,routine,[(exec_routine_instruction_index,i)])
    new_theories.append(theory)
  return new_theories