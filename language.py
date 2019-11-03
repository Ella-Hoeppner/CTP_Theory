'''
The functions below that start with 'instruction_' are used as the basic  instructions of the theory language. Each one takes two arguments: "state" and "args". "state" is a 2-tuple consisting of a list of integers (called the "int-stack") and a list of sets of claims (called the "claim-stack"), and "args" is a list of integers that can be used to pass additional arguments to the instruction, if necessary.

Most instructions, by default, don't return anything, and instead just modifying "state". Some special instructions like "if" or "for" return a boolean or integer that will be used to control the flow of execution. Certain instructions are only well-defined for a certain type of program state. In the case that an instruction recieves a program state for which it is undefined, it will return -1 to indicate a runtime error.
'''

def instruction_if(state, args):
  """Used to denote that a block will only be executed if a condition passes. Returns False if the top integer is 0, and True otherwise. Undefined when the int-stack is empty."""
  if len(state[0])<1:
    return -1
  return state[0][-1]!=0

def instruction_else(state, args):
  """Used to denote that a block will be executed conditional before the prior block fails."""
  return 0

def instruction_while(state, args):
  """Used to denote that a block will repeatedly execute while a condition holds. Returns False if the top integer is 0, and True otherwise. Undefined when the int-stack is empty."""
  if len(state[0])<1:
    return -1
  return state[0][-1]!=0

def instruction_for(state, args):
  """Used to denote that a block will execute a fixed number of times. Returns the integer on the top of the int-stack. Undefined when the int-stack is empty"""
  if len(state[0])<1:
    return -1
  return state[0][-1]

def instruction_end(state, args):
  """Used to denote the end of a block, which starts with an if, while, or for."""
  return 0

def instruction_forward_int(state, args):
  """Brings an integer at an index specified in args to the top of the stack. The integer at the specified index will be removed and then placed on the top of the stack. Undefined when the specified index is too large for the int-stack."""
  if args[0]+1>=len(state[0]):
    return -1
  index=-(2+args[0])
  temp_value=state[0][index]
  del state[0][index]
  state[0].append(temp_value)

def instruction_swap_int(state, args):
  """Swaps an int at an index specified in args with the integer on the top of the stack. Undefined when the specified index is too large for the int-stack."""
  if args[0]+1>=len(state[0]):
    return -1
  index=-(2+args[0])
  temp_value=state[0][index]
  state[0][index]=state[0][-1]
  state[0][-1]=temp_value

def instruction_duplicate_int(state, args):
  """Pushes an int to the stack equal to the value at the index specified in args. Undefined when the specified index is too large for the int-stack."""
  if args[0]>=len(state[0]):
    return -1
  index=-(1+args[0])
  state[0].append(state[0][index])

def instruction_remove_int(state, args):
  """Deletes an integer from the stack at an index specified in args. Undefined when the specified index is too large for the int-stack."""
  if args[0]>=len(state[0]):
    return -1
  index=-(1+args[0])
  del state[0][index]

def instruction_forward_claim_set(state, args):
  """Brings a set of claims at an index specified in args to the top of the stack. The set of claims at the specified index will be removed and then placed on the top of the stack. Undefined when the specified index is too large for the claim-stack."""
  if args[0]+1>=len(state[1]):
    return -1
  index=-(2+args[0])
  temp_value=state[1][index]
  del state[1][index]
  state[1].append(temp_value)

def instruction_swap_claim_set(state, args):
  """Swaps a set of claims at an index specified in args with the set of claims on the top of the stack. Undefined when the specified index is too large for the claim-stack."""
  if args[0]+1>=len(state[1]):
    return -1
  index=-(2+args[0])
  temp_value=state[1][index]
  state[1][index]=state[1][-1]
  state[1][-1]=temp_value

def instruction_duplicate_claim_set(state, args):
  """Pushes a set of claims to the stack that is identical to the set at the index specified in args. Undefined when the specified index is too large for the claim-stack."""
  if args[0]>=len(state[1]):
    return -1
  index=-(1+args[0])
  claim_set_copy=[]
  for claim in state[1][index]:
    claim_set_copy.append((claim[0], claim[1][:]))
  state[1].append(claim_set_copy)

def instruction_remove_claim_set(state, args):
  """Deletes a set of claims from the stack at an index specified in args. Undefined when the specified index is too large for the claim-stack."""
  if args[0]>=len(state[1]):
    return -1
  index=-(1+args[0])
  del state[1][index]

def instruction_push_const(state, args):
  """Pushes a constant specified in args to the top of the int-stack."""
  state[0].append(args[0])

def instruction_add(state, args):
  """Pushes a value to the int-stack that is equal to the sum of the top two values on the int-stack. Undefined when the int-stack has fewer than two elements."""
  if len(state[0])<2:
    return -1
  state[0].append(state[0][-1]+state[0][-2])

def instruction_equal(state, args):
  """Pushes a value, which is 1 if top two integers on the int-stack are equal and 0 otherwise, to the int-stack. Undefined when the int-stack has fewer than two elements."""
  if len(state[0])<2:
    return -1
  state[0].append(1 if state[0][-1]==state[0][-2] else 0)

def instruction_less(state, args):
  """Pushes a value, which is equal to 1 if the top integer on the int-stack is less than the second-to-top integer on the int-stack. Undefined when the int-stack has fewer than two elements."""
  if len(state[0])<2:
    return -1
  state[0].append(1 if state[0][-1]<state[0][-2] else 0)

def instruction_negate(state, args):
  """Pushes a value equal to the top integer on the int-stack multiplied by -1 to the int-stack. Undefined when the stack is empty."""
  if len(state[0])<1:
    return -1
  state[0].append(state[0][-1]*-1)

def instruction_not(state, args):
  """Pushes a value, which is equal to 1 if the top integer on the stack is 0 and 0 otherwise, to the int-stack. Undefined when the stack is empty."""
  if len(state[0])<1:
    return -1
  state[0].append(1 if state[0][-1]==0 else 0)

def instruction_and(state, args):
  """Pushes a value, which is equal to 1 if the top two elements on the stack are non-zero and 0 otherwise, to the int-stack. Undefined when the stack is empty."""
  if len(state[0])<2:
    return -1
  state[0].append(1 if (state[0][-1]!=0 and state[0][-2]!=0) else 0)

def instruction_or(state, args):
  """Pushes a value, which is equal to 1 if either of the top two elements on the stack are non-zero and 0 otherwise, to the int-stack. Undefined when the stack is empty."""
  if len(state[0])<2:
    return -1
  state[0].append(1 if (state[0][-1]!=0 or state[0][-2]!=0) else 0)

def instruction_xor(state, args):
  """Pushes a value, which is equal to 1 if exactly one of the top two elements on the stack is non-zero and 0 otherwise, to the int-stack. Undefined when the stack is empty."""
  if len(state[0])<2:
    return -1
  state[0].append(1 if (state[0][-1]!=0 != state[0][-2]!=0) else 0)

def instruction_int_count(state, args):
  """Pushes an integer equal to the size of the int-stack to the top of the int-stack."""
  state[0].append(len(state[0]))

def instruction_claim_set_count(state, args):
  """Pushes an integer equal to the size of the claim-stack to the top of the int-stack."""
  state[0].append(len(state[1]))

def instruction_claim_int_count(state, args):
  """Pushes an integer equal to the size of the list of integers in the top claim on the claim-stack to the top of the int-stack. Undefined when the claim-stack is empty."""
  if len(state[1])<1:
    return -1
  state[0].append(len(state[1][-1][1]))

def instruction_claim_bool(state, args):
  """Pushes an integer, which is equal 1 if the boolean in the top claim on the claim-stack is true and 0 otherwise, to the top of the int-stack. Undefined when the claim-stack is empty."""
  if len(state[1])<1:
    return -1
  state[0].append(1 if state[1][-1][0] else 0)

def instruction_claim_int(state, args):
  """Pushes an integer equal to the value in the list of integers in the top claim on the integer at the index specified in args to the top of the int-stack. The index in args can be either negative or non-negative, which will access the elements in the list of integers backwards or forwards, respectively. Undefined if the claim-stack is empty, or if the index is too big, for the list of integers."""
  if len(state[1])<1:
    return -1
  claim=state[1][-1]
  index=args[0]
  if index<0:
    if index*-1>len(claim[1]):
      return -1
    state[0].append(claim[1][index])
  else:
    if index>=len(claim[1]):
      return -1
    state[0].append(claim[1][index])

def instruction_new_claim(state, args):
  """Pushes a new claim to the claim-stack. The new claim has a boolean value of True and an empty list of integers."""
  state[1].append((True,[]))

def instruction_set_claim_bool(state, args):
  """Sets the boolean in the top claim on the claim-stack to false if the top integer on the int-stack is 0 and true otherwise. Undefined when the claim-stack or int-stack are empty."""
  if len(state[0])<1 or len(state[1])<1:
    return -1
  state[1][-1]=(False if state[0][-1]==0 else True,state[1][-1][1])

def instruction_set_claim_int(state, args):
  """Sets the integer at the index specified in args in the list of the claim on the top of the claim-stack to the integer on the top of the int-stack. The index in args can be either negative or non-negative, which will access the elements in the list of integers backwards or forwards, respectively. Undefined if the int-stack or claim-stack are empty, or if the index is too big, for the list of integers."""
  if len(state[0])<1 or len(state[1])<1:
    return -1
  index=args[0]
  claim=state[1][-1]
  if index<0:
    if index*-1>len(claim[1]):
      return -1
    claim[1][index]=state[0][-1]
  else:
    if index>=len(claim[1]):
      return -1
    claim[1][index]=state[0][-1]

def instruction_push_claim_int(state, args):
  """Pushes an integer equal to the value on the top of the int-stack to the end of the list in the top claim on the claim-stack. Undefined if the int-stack or claim-stack are empty."""
  if len(state[0])<1 or len(state[1])<1:
    return -1
  state[1][-1][1].append(state[0][-1])

def instruction_remove_claim_int(state, args):
  """Removes the integer at the index specified in args in the list of the claim on the top of the claim-stack. The index in args can be either negative or non-negative, which will access the elements in the list of integers backwards or forwards, respectively. Undefined if the int-stack or claim-stack are empty, or if the index is too big, for the list of integers."""
  if len(state[0])<1 or len(state[1])<1:
    return -1
  index=args[0]
  claim=state[1][-1]
  if index<0:
    if index*-1>len(claim[1]):
      return -1
    del claim[1][index]
  else:
    if index>=len(claim[1]):
      return -1
    del claim[1][index]

def instruction_assert(state, args):
  """Undefined when the int-stack is empty of the int on the top of the int-stack is 0. This instruction can be narrow the domain of inputs for which theory is defined, by allowing the theory to crash in certain circumstances."""
  if len(state[0])<1 or state[0][-1]==0:
    return -1

def instruction_exec(state, args):
  """Used to denote that a theory or routine should be executed."""
  return 0

'''Describes the types of arguments associated with each instruction. Each instruction is associated with a list of integers. The size of each list describes the number of arguments the instruction takes, and the elements of the lists are strings that describe the types of the corresponding arguments. "int" corresponds to an argument that can take on any integer value, and "nonNegInt" corresponds to an integer value that is greater than or equal to 0.'''
instruction_arg_types={
  instruction_if:[],
  instruction_else:[],
  instruction_while:[],
  instruction_for:[],
  instruction_end:[],
  instruction_forward_int:['nonNegInt'],
  instruction_swap_int:['nonNegInt'],
  instruction_duplicate_int:['nonNegInt'],
  instruction_remove_int:['nonNegInt'],
  instruction_forward_claim_set:['nonNegInt'],
  instruction_swap_claim_set:['nonNegInt'],
  instruction_duplicate_claim_set:['nonNegInt'],
  instruction_remove_claim_set:['nonNegInt'],
  instruction_push_const:['int'],
  instruction_add:[],
  instruction_equal:[],
  instruction_less:[],
  instruction_negate:[],
  instruction_not:[],
  instruction_and:[],
  instruction_or:[],
  instruction_xor:[],
  instruction_int_count:[],
  instruction_claim_set_count:[],
  instruction_claim_int_count:[],
  instruction_claim_bool:[],
  instruction_claim_int:['int'],
  instruction_new_claim:[],
  instruction_set_claim_bool:[],
  instruction_set_claim_int:['int'],
  instruction_push_claim_int:[],
  instruction_remove_claim_int:['int'],
  instruction_assert:[],
  instruction_exec: ['int']
}

'''The list of all basic instructions that can be used in theories.'''
instruction_functions=[
  instruction_if,
  instruction_else,
  instruction_while,
  instruction_for,
  instruction_end,
  instruction_forward_int,
  instruction_swap_int,
  instruction_duplicate_int,
  instruction_remove_int,
  instruction_forward_claim_set,
  instruction_swap_claim_set,
  instruction_duplicate_claim_set,
  instruction_remove_claim_set,
  instruction_push_const,
  instruction_add,
  instruction_equal,
  instruction_less,
  instruction_negate,
  instruction_not,
  instruction_and,
  instruction_or,
  instruction_xor,
  instruction_int_count,
  instruction_claim_set_count,
  instruction_claim_int_count,
  instruction_claim_bool,
  instruction_claim_int,
  instruction_new_claim,
  instruction_set_claim_bool,
  instruction_set_claim_int,
  instruction_push_claim_int,
  instruction_remove_claim_int,
  instruction_assert,
  instruction_exec
]

'''A list of basic instructions that denote the start of a block.'''
block_starter_instructions=[
  instruction_if,
  instruction_while,
  instruction_for
]

'''A list of basic instructions that cause execution to fork if the top element on the claim-stack is a set of multiple claims, rather than a single claim.'''
forking_functions=[
  instruction_claim_int_count,
  instruction_claim_bool,
  instruction_claim_int,
  instruction_set_claim_bool,
  instruction_set_claim_int,
  instruction_push_claim_int,
  instruction_remove_claim_int
]

def get_instruction_function_name(instruction_index):
  """Returns the name of a basic instruction. The name returned is equal to the name used in the instructions declaration, but without the "instruction_" prefix."""
  return instruction_functions[instruction_index].__name__[12:]

def program_string(theory):
  """Returns a string containing a human-readable display of a theory. Each line, there is the name of one basic instruction, along with whatever arguments associated with that instruction. Instructions inside blocks have indentation."""
  string=""
  indentation=0

  for i in range(len(theory)):
    string+=str(i)+".\t"
    instruction=theory[i]
    instruction_index=instruction[0]
    instruction_function=instruction_functions[instruction_index]
    instruction_name=get_instruction_function_name(instruction_index)

    if instruction_function==instruction_end or instruction_function==instruction_else:
      indentation-=1

    string+="  "*indentation
    string+=instruction_name
    for i2 in range(len(instruction)-1):
      string+=" "+str(instruction[i2+1])
    string+="\n"

    if instruction_function==instruction_if or instruction_function==instruction_else or instruction_function==instruction_while or instruction_function==instruction_for:
      indentation+=1
  
  return string

def inlined_program_string(theory_index, theories, routines):
  """Inlines a program (replaces each instance of the "exec" instruction with the implementation of the executede theory or routine) and returns the corresponding program string."""
  inlined_theory=inline_execs(theory_index, theories, routines)
  return program_string(inlined_theory)

def inline_execs(theory_index, theories, routines, inline_theories=True):
  """Replaces each instance of the "exec" instruction with teh implementation of the executed theory or routine."""
  index=0
  theory=theories[theory_index]
  while True:
    if index>=len(theory):
      break
    if instruction_functions[theory[index][0]]==instruction_exec:
      exec_index=theory[index][1]
      if exec_index>=0:
        theory=theory[:index]+routines[exec_index]+theory[index+1:]
      elif inline_theories:
        exec_theory_index=-1-exec_index
        if theory_index==exec_theory_index:
          theory=theory[:index]+theory[index+1:]
        else:
          theory=theory[:index]+theories[exec_theory_index]+theory[index+1:]
    else:
      index+=1
    if index>=len(theory):
      break
  return theory

def run_theory(theory_index, theories, routines, input_set, execution_limit=100):
  """Runs a theory on the provided set of claims and returns the resulting claims."""
  control_map=([],[])
  control_stack=[]
  
  theory=inline_execs(theory_index, theories, routines)

  for i in range(len(theory)):
    instruction_function=instruction_functions[theory[i][0]]
    if instruction_function==instruction_else or instruction_function==instruction_end:
      control_map[1].append(i)
      control_map[0].append(control_stack.pop())
    if instruction_function==instruction_if or instruction_function==instruction_else or instruction_function==instruction_while or instruction_function==instruction_for:
      control_stack.append(i)
  return run_theory_branch(theory, (0, [], [copy_claim_set(input_set)], []), control_map, [], execution_limit, 0)

def run_theory_branch(theory, state, control_map, touched_inputs, execution_limit, execution_count):
  """Executes a branch of execution of a theory, and returns the resulting claims. May recursively branch into multiple strands of execution if necessary."""
  while True:
    pointer=state[0]
    if pointer>=len(theory):
      if not isinstance(state[2][-1],list):
        return [(touched_inputs,state[2][-1])]
      return []
    instruction=theory[pointer]
    instruction_function=instruction_functions[instruction[0]]

    if instruction_function in forking_functions and isinstance(state[2][-1],list):
      full_output_list=[]
      for i in range(len(state[2][-1])):
        lone_claim=state[2][-1][i]
        claim_sets_copy=[]
        for claim_set in state[2]:
          if isinstance(claim_set,list):
            claim_sets_copy.append(copy_claim_set(claim_set))
          else:
            claim_sets_copy.append((claim_set[0], claim_set[1][:]))
        split_state=(pointer, state[1][:], claim_sets_copy[:-1]+[lone_claim], state[3][:])
        output_list=run_theory_branch(theory, split_state, control_map, touched_inputs[:]+[i], execution_limit, execution_count)
        full_output_list+=output_list
      return full_output_list
    
    instruction_output=instruction_function((state[1],state[2]), instruction[1:])

    if instruction_output==-1:
      return []
    
    new_pointer=state[0]
    if instruction_function==instruction_if or instruction_function==instruction_while:
      if instruction_output:
        new_pointer+=1
      else:
        new_pointer=control_map[1][control_map[0].index(pointer)]+1
    elif instruction_function==instruction_else:
      new_pointer=control_map[1][control_map[0].index(pointer)]+1
    elif instruction_function==instruction_for:
      if instruction_output>0:
        new_pointer+=1
        state[3].append(instruction_output)
      else:
        new_pointer=control_map[1][control_map[0].index(pointer)]+1
    elif instruction_function==instruction_end:
      start_index=control_map[0][control_map[1].index(pointer)]
      start_instruction_function=instruction_functions[theory[start_index][0]]
      if start_instruction_function==instruction_if or start_instruction_function==instruction_else:
        new_pointer+=1
      if start_instruction_function==instruction_while:
        new_pointer=start_index
      if start_instruction_function==instruction_for:
        state[3][-1]-=1
        if state[3][-1]<=0:
          state[3].pop()
          new_pointer+=1
        else:
          new_pointer=start_index+1
    else:
      new_pointer+=1
    
    state=(new_pointer, state[1], state[2], state[3])
    
    execution_count+=1
    if execution_count>=execution_limit:
      return []

def copy_claim_set(claims):
  """Returns a set copy of a set of claims."""
  return [(claim[0], claim[1][:]) for claim in claims]

def is_program_valid(program):
  """Returns true if a program is valid, and false otherwise. A program is valid if and only if all block openers have corresponding block closers, all "else" instructions happen between a block start and block end, and the arguments for each theory are of the proper form (e.g. there no "nonNegInt" arguments are negative)."""
  block_starter_stack=[]
  for instruction in program:
    instruction_function=instruction_functions[instruction[0]]
    arg_types=instruction_arg_types[instruction_function]
    if len(instruction)!=len(arg_types)+1:
      return False
    for i in range(len(arg_types)):
      if arg_types[i]=="nonNegInt" and instruction[i+1]<0:
        return False
    if instruction_function in block_starter_instructions:
      block_starter_stack.append(instruction_function)
    if instruction_function==instruction_end:
      if len(block_starter_stack)==0:
        return False
      block_starter_stack.pop()
    if instruction_function==instruction_else:
      if len(block_starter_stack)==0 or block_starter_stack[-1]!=instruction_if:
        return False
  return len(block_starter_stack)==0