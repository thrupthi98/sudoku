#Imports
from os import stat_result
import copy
import numpy as np
import datetime as dt

#Read the inputs from the data file (.txt format)
file = input("Enter the path to your input file(.txt format) here")
with open(file.strip()) as f:
    contents = f.read()
    Lines = contents.strip().split('\n')

#Get the type of algo to be executed from the user
print("1. Naïve Backtracking Algorithm")
print("2. Naïve Backtracking Algorithm with minimum remaining values")
algo = input("Please enter a number from the above given options")
algo = int(algo)
if algo != 2 or algo != 1:
    print("Please select a valid option")

state = Lines
initial_state = []

#Convert the conents of the data file to a 2D array
for val in state:
  initial_state.append(list(val))

#Print the rows and columns in the initial state
print('*****Initial State*****')
for data in initial_state:
  print(data)
print('\n')

#Function to get all empty_poritions in the state
def get_empty_positions(state):
  positions = []
  #For each row and column in the store all the values that are equal to '0'
  for row in range(0,len(state)):
    for col in range(0,len(state[row])):
      if state[row][col] == '0':
        positions.append([row,col])
  return positions

#Function to get the quadrant given the co-ordinates
def get_quadrant(ordinates):
  #For a 9X9 sudoko puzzle, there are 9 diffrent quadrants present.
  #Check the 9 different cases and return the margin row and column values for that quaddrant
  if(ordinates[0]>=0 and ordinates[0]<=2 and ordinates[1]>=0 and ordinates[1]<=2):
      return [[0,2],[0,2]]
  elif(ordinates[0]>=0 and ordinates[0]<=2 and ordinates[1]>=3 and ordinates[1]<=5):
      return [[0,2],[3,5]]
  elif(ordinates[0]>=0 and ordinates[0]<=2 and ordinates[1]>=6 and ordinates[1]<=8):
      return [[0,2],[6,8]]
  elif(ordinates[0]>=3 and ordinates[0]<=5 and ordinates[1]>=0 and ordinates[1]<=2):
      return [[3,5],[0,2]]
  elif(ordinates[0]>=3 and ordinates[0]<=5 and ordinates[1]>=3 and ordinates[1]<=5):
      return [[3,5],[3,5]]
  elif(ordinates[0]>=3 and ordinates[0]<=5 and ordinates[1]>=6 and ordinates[1]<=8):
      return [[3,5],[6,8]]
  elif(ordinates[0]>=6 and ordinates[0]<=8 and ordinates[1]>=0 and ordinates[1]<=2):
      return [[6,8],[0,2]]
  elif(ordinates[0]>=6 and ordinates[0]<=8 and ordinates[1]>=3 and ordinates[1]<=5):
      return [[6,8],[3,5]]
  elif(ordinates[0]>=6 and ordinates[0]<=8 and ordinates[1]>=6 and ordinates[1]<=8):
      return [[6,8],[6,8]]

#Function to get the possible values at a particular co-ordinate in a state
def get_possible_values(ordinates, state):
  row_list = []
  col_list = []
  quad_list = []

  #get all the elements present in given row
  for ele in state[ordinates[0]]:
    if ele != 0:
      row_list.append(ele)

  #get all the elements present in given column
  for row in range(0,len(state)):
    if state[row][ordinates[1]] != '0':
      col_list.append(state[row][ordinates[1]])

  #get the qaudrant of the given co-ordinate
  quadrant = get_quadrant(ordinates)

  row_start = quadrant[0][0]
  row_end = quadrant[0][1]
  col_start = quadrant[1][0]
  col_end = quadrant[1][1]

  #Get all non-empty elements in the quadrant 
  for row in range(row_start, row_end+1):
    for col in range(col_start, col_end+1):
      if(state[row][col] != '0'):
        quad_list.append(state[row][col])

  #Get the set of elements that can be filled in the given co-ordinate  
  ele_list = row_list + col_list + quad_list
  possible_values = list(set(['1','2','3','4','5','6','7','8','9'])-set(ele_list))
  return possible_values
  
#Function to assign a number at a given position in a state
def assign_num(ordinates, state):
  global filled_positions
  temp_state = copy.deepcopy(state)
  #get all the possible values that can be filled in the given potition
  possible_values = get_possible_values(ordinates, state)
  #For each possible value, check if the state is already present.
  #If present, backtrack to the previous position.
  #Else, update the current_state.
  for val in possible_values:
    temp_state[ordinates[0]][ordinates[1]] = str(val)
    if str(temp_state) not in generated_states:
      state = temp_state
      filled_positions.append(ordinates)
      generated_states.append(str(state))
      break
  else:
    if(len(filled_positions) != 0):
      last_updated_position = filled_positions[-1]
      state[last_updated_position[0]][last_updated_position[1]] = '0'
      filled_positions.pop()
  return state

#Function to get the MRV index
def get_mrv_index(positions,state):
  weights = []
  #For each empty position, get the number of all possible values that can be filled
  for position in positions:
    possible_values = get_possible_values(position,state)
    weights.append(len(possible_values))
  #If the possible values are not empty, return the co-ordinates of the empty position with minimum number of possible values
  if(len(weights) != 0):
    index = weights.index(min(weights))
  else:
    index = 0
  return index

#Declarartion of global variables
filled_positions = []   
generated_states = []
current_state = initial_state

#Get the co-ordinates of all the empty positions present in the initial state
empty_positions = get_empty_positions(initial_state)
#For Naive base backtracking with MRV get MRV index 
if algo == 2:
  index = get_mrv_index(empty_positions, initial_state)
else:
  index = 0

count = 0
start_time = dt.datetime.now()
#Until all empty positions are filled assign a number to the empty_position based on Naive Bayes Bactraking or Naive Bayes Bactraking with MRV
while len(empty_positions) != 0: 
    current_state = assign_num(empty_positions[index],current_state)
    empty_positions = get_empty_positions(current_state)
    if algo == 2:
      index = get_mrv_index(empty_positions, current_state)
    count += 1
    
print('*****Output*****')
for ele in current_state:
  print(ele)
end_time = dt.datetime.now()

print('Steps taken: ' + str(count))
print('Time_Taken: ' + str(end_time-start_time))