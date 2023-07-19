# This is a comment
# Author:  Vlad Mariano
# Last update:  22 April 2021

print("Hello World")
name = input("What is your name? ")
print("Hello ", name)
age_str = input("How old are you? ")  # age_str is a string
age = int(age_str)  # int() will convert age_str into a number
print("I am ", age, " years old")
age = age + 1   # add one to your age
print("I am " + str(age) + " years old next week")

# Let's do a loop
for i in range(age):
    print( name + " used to be " + str(i) + " years old" )
    
print("Good bye!")
