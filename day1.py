# day1.py


class DialObject:
  def __init__(self, p=50, m=0, n=99):
    self.p = p # initial position
    self.mini = m # the minimum
    self.maxi = n # the maximum dial value
    self.history_moves = []
    self.history_pos = [self.p]
    self.mini_stopped = 0
    self.mini_passed = 0
    
  def get_history_moves(self):
    return self.history_moves

  def get_history_pos(self):
    return self.history_pos
  
  def get_p(self):
    return self.p

  def get_mini_passed(self):
    return self.mini_passed

  def get_mini_stopped(self):
    return self.mini_stopped
    
  def dorun(self, turnList, verbose = True):
    for i, move in enumerate(turnList):
      if i == 0 and verbose:
        print(f"The dial starts by pointing at {d.get_p()}")

      if move == "":
        if verbose:
          print(f"Ignoring empty move request")
        continue

      #if verbose:
      #  print(f"The dial is at {d.get_p()} and rotated {move} to point at",end="")
      
      d.turn(move, verbose)
      #if verbose:
      #  print(f" {d.get_p()}")

  def dorun_fromfile(self, filename, verbose = False):
    try:
      with open(filename, 'r') as f:
        content = f.read()
        #print(content)
        fileRun = content.split("\n")
        self.dorun(fileRun, verbose = verbose)
    except FileNotFoundError:
      print("no such file found")

  def turn(self, move_code, verbose = 0):
    return self.turn_internal(move_code = move_code, verbose = verbose)
  
  def turn_internal(self, move_code, verbose):
    p = self.p
    p_init = p
    p_startedTurnAtMini = False
    passMini_thisTurn = 0

    if p == self.mini:
      p_startedTurnAtMini = True
      # we do NOT count this as stopping at zero, as this is starting at zero

    if move_code[0] == 'L':
      # we are moving LEFT, which decreases p
      if verbose > 1:
        print("moving LEFT to decrease")

      p_dec = int(move_code[1:])
      p -= p_dec

      while p < self.mini:
        # it's below min, so need to RAISE it i x R
        p_prev = p
        passMini_thisTurn += 1
        p += (self.maxi - self.mini + 1)

      if p_startedTurnAtMini:
        passMini_thisTurn -= 1 # don't count the first move back
    
    elif move_code[0] == 'R':
      # we are moving RIGHT, which increases p
      if verbose > 1:
        print("moving RIGHT to inrease")

      p_inc = int(move_code[1:])
      p += p_inc

      while p > self.maxi:
        # it's above max, so need to LOWER it i x R
        p_prev = p
        p -= (self.maxi - self.mini + 1)
        passMini_thisTurn += 1
        # print(f" -     {p_prev:4d} --> {p:4d}")
  
        if p == self.mini:
          # if was decreased to mini, we don't count the last reset
          passMini_thisTurn -= 1


    else:
      print("error - can't parse move_code")
      exit()

    if p == self.mini:
      # if we end on mini, add this as a stopped
      self.mini_stopped += 1
    
    if verbose:
      print(f"The dial (from {p_init}) is rotated {move_code} to point to {p}",end="")
      if passMini_thisTurn:
        print(f"; during this rotation, it points at 0 {passMini_thisTurn} times")
      else:
        print(".")
  
    self.p = p
    self.mini_passed += passMini_thisTurn
  

exampleRunA = ["L68","L30","R48","L5","R60","L55","L1","L99","R14","L82"]      
d = DialObject()
d.dorun(exampleRunA, verbose=True)

d = DialObject()
d.dorun_fromfile("day1_input.txt", verbose=False)

print(f"Stopped at mini: {d.get_mini_stopped()}")
print(f"Passed mini:     {d.get_mini_passed()}")
print(f"Total: {d.get_mini_stopped() + d.get_mini_passed()}")