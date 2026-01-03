

def print_values(digits: list[int]):
  print(f"1st item: {digits[0]}")
  print(f"2st item: {digits[1]}")
  print(f"Last item: {digits[-1]}")
  print(f"2nd last item: {digits[-2]}")
  print('')

def print_array(digits: list[int]):
  print(digits)
  print('')

def delete(digits: list[int], index: int):
  del digits[index]

def add(digits: list[int], new_number: int):
  digits.append(new_number)

def add_nultiple(digits: list[int], new_number_list: list[int]):
  digits.extend(new_number_list)

def get_length(digits: list[int]):
  return len(digits)

def get_index(digits: list[int], search: int) -> int:
  return digits.index(search)

def slice(digits: list[int], start_index: int | None, end_index: int | None):
  """
  Slice an array and return a copy of the slice.

  Args:
    end_index (int | None): End of the index for the slice. Will be excluded from the slice.
  """

  return digits[start_index : end_index]

def sort(digits: list[int], is_reverse: bool = False):
  digits.sort(reverse=is_reverse)
  return digits


def main():
  Digits: list[int] = [1, 2, 3, 4, 5, 6]
  print_values(Digits)
  
  print("Before deletion")
  print_array(Digits)
  
  delete(digits=Digits, index=1)

  print("After deletion")
  print_array(Digits)

  new_digit=10
  print(f"After adding {new_digit}")
  add(Digits, new_digit)
  print_array(Digits)

  new_digit_array=[11,12,13]
  print(f"After adding {new_digit_array}")
  add_nultiple(Digits, new_digit_array)
  print_array(Digits)

  length = get_length(Digits)
  print(f'Total element in arr: {length}')


def slice_main():
  Digits: list[int] = [1, 2, 3, 4, 5, 6]
  print(f'Original array: {Digits}\n')
  print(f'Slice from index 1 to 3: {slice(Digits, 1, 4)}')
  print(f'Slice for the last 2 items: {slice(Digits, -2, None)}')
  print(f'Slice for the first 2 items: {slice(Digits, None, 2)}')

def list_utils_main():
  Digits: list[int] = [1, 2, 3, 4, 5, 6]
  print(f'Original: {Digits}\n')
  
  print(f"Index of 3 is {get_index(Digits, 3)}\n")
  
  sort(Digits, is_reverse=True)
  print(f"After sort: {Digits}\n")


if __name__ == "__main__":
  # main()
  # slice_main()
  list_utils_main()
