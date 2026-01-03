def main():
  new_tupple = (1,2,3)
  print(f"new tupple: {new_tupple}\n")
  
  # Access
  print(f"1st item in tupple: {new_tupple[0]}\n")
  
  # Extract tupple item
  a, _, _ = new_tupple
  print(f"extracted item in tupple: a = {a}\n")

  # Create tupple from spilt
  (a, b, c) = "1,2,3".split(',')
  print(f"a = {a}\nb = {b}\nc = {c}\n")




if __name__ == '__main__':
  main()