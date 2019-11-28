import language
import conjecture
import extract
import minds

def test_theories():
  """Demonstrates the execution of theories."""
  print("Executing test_theories:")
  increment_theory=[
    (26,-1),
    (13,1),
    (14,),
    (31,-1),
    (30,),
    (8,0),
    (8,0),
    (8,0)
  ]

  repeat_increment_theory=[
    (3,),
    (33,0),
    (4,)
  ]

  repeat_increment_10_times_theory=[
    (13,10),
    (33,1)
  ]

  sum_theory=[
    (13,0),
    (13,1),
    (2,),
    (8,0),

    (26,-1),
    (31,-1),
    (14,),
    (8,1),
    (8,1),

    (24,),
    (4,),
    
    (8,0),
    (30,)
  ]

  print("increment_theory:")
  print(language.program_string(increment_theory))

  print("Running increment_theory on (True, [0, 0])")
  print(language.run_theory(0, [increment_theory], [], [(True, [0, 0])]))
  print("\n")

  print("repeat_increment_theory:")
  print(language.program_string(repeat_increment_theory))

  print("repeat_increment_10_times_theory:")
  print(language.program_string(repeat_increment_10_times_theory))

  print("Running repeat_increment_10_times_theory on (True, [0, 0])")
  print(language.run_theory(0, [repeat_increment_10_times_theory], [increment_theory, repeat_increment_theory], [(True, [0, 0])]))

def test_claim_generation():
  """Demonstrates the process of claim generation, including the process of finding problems."""
  print("Executing test_claim_generation:")
  append_9_theory=[
    (13,9),
    (30,)
  ]
  set_false_and_append_9_theory=[
    (13,0),
    (28,),
    (13,9),
    (30,)
  ]

  print("append_9_theory:")
  print(language.program_string(append_9_theory))
  print("set_false_and_append_9_theory:")
  print(language.program_string(set_false_and_append_9_theory))

  mind=minds.new_mind(theories=[append_9_theory,set_false_and_append_9_theory],claims=[(True,[])])

  for i in range(10):
    minds.generate_claims(mind)

  print(minds.mind_string(mind))

def test_extract():
  """Demonstrates the extraction of routines."""
  print("Executing test_extract:")

  theory_1=[
    (14,),
    (15,),
    (14,),
    (16,)
  ]
  theory_2=[
    (14,),
    (15,),
    (14,),
    (17,)
  ]
  theory_3=[
    (15,),
    (14,)
  ]

  mind=minds.new_mind(theories=[theory_1,theory_2,theory_3])

  print("Mind initial state:")
  print(minds.mind_string(mind, show_claims=False, show_problems=False))

  minds.extract_new_routines(mind,1)
  print("Mind after 1 step of extraction:")
  print(minds.mind_string(mind, show_claims=False, show_problems=False))

  minds.extract_new_routines(mind,1)
  print("Mind after 2 steps of extraction:")
  print(minds.mind_string(mind, show_claims=False, show_problems=False))


def test_conjecture():
  """Demonstrates the process of conjecturing new theories."""
  print("Executing test_conjecture:")

  theory=[]

  print(language.program_string(theory))
  for i in range(10):
    theory=conjecture.vary([theory], 0, [], steps=1)
    print("Theory after {i+1} stages of variation:")
    print(language.program_string(theory))