#!/usr/bin/env python
# coding: utf-8

# # Agenda
# 
# 1. Review the iterator protocol
# 2. Generator functions
#     - How to define them
#     - How they're different from regular functions
#     - Keeping state across invocations
#     - How do they work?
# 3. Generator expressions (aka generator comprehensions)
#     - How to define them
#     - How to use them

# In[1]:


# Lots of objects in Python are iterable

for one_item in 'abcde':
    print(one_item)


# In[2]:


for one_item in [10, 20, 30, 40, 50]:
    print(one_item)


# In[3]:


d = {'a':1, 'b':2, 'c':3}

for one_item in d:
    print(one_item)


# In[5]:


# d.items returns an object of type "dict_items"
# it is iterable, also!
# it returns a (key, value) tuple with each iteration

for key, value in d.items():
    print(f'{key}: {value}')


# In[6]:


# let's ask d if it is iterable!

i = iter(d)   # normally, don't use "iter" in your programs


# In[7]:


i


# In[8]:


next(i)


# In[9]:


next(i)


# In[10]:


next(i)


# In[11]:


next(i)


# In[12]:


def myfunc():
    return 1
    return 2
    return 3


# In[13]:


myfunc()


# In[14]:


import dis  # disassemble our Python code

dis.dis(myfunc)


# In[17]:


# here, I define a generator function!
# Python knows it's a generator function because it uses "yield"
# the result of invocing a generator function is a generator object
# generators are iterable -- they know how to behave inside of a "for" loop

def myfunc():
    yield 1
    yield 2
    yield 3


# In[18]:


myfunc()


# In[19]:


myfunc()


# In[20]:


myfunc()


# In[21]:


g = myfunc()

next(g)  # if g, our generator, is iterable, then it knows how to respond to "next"


# In[22]:


next(g)


# In[23]:


next(g)


# In[24]:


next(g)


# # What's happening?
# 
# Running `next` on a generator object executes the generator's function body through the next `yield`.  You get the value back, and then the generator function goes to sleep just after the `yield`, waking up when you next call `next` on it.

# In[25]:


def myfunc():
    print('At start')
    yield 1
    print('In the middle')
    yield 2
    print('Almost done!')
    yield 3
    print('Now I am really done')


# In[26]:


g = myfunc()


# In[27]:


next(g)


# In[28]:


next(g)


# In[30]:


next(g)


# In[31]:


next(g)


# In[32]:


def double_numbers(numbers):
    for one_number in numbers:
        yield one_number * 2


# In[33]:


double_numbers([10, 20, 30])


# In[34]:


for one_item in double_numbers([10, 20, 30]):
    print(one_item)


# In[37]:


list(double_numbers([10, 20, 30]))


# In[38]:


g


# In[39]:


type(g)


# In[40]:


# can I create a new instance of generator? ... turns out, I can't.
type(g)()


# In[ ]:





# # Exercise: Only evens
# 
# Write a generator function that takes a list (or any other iterable) of integers as an argument. It should return, with each iteration, the next *EVEN* number in that list of integers.  When we get to the end of the input list, then the generator ends.

# In[42]:


def only_evens(numbers):
    for one_number in numbers:
        if one_number % 2 == 0:
            yield one_number
        
        
for one_item in only_evens(range(5, 13)):
    print(one_item)


# In[46]:


from typing import Iterable, Generator

def only_evens(numbers:Iterable[int]) -> Generator[int, None, None]:
    for one_number in numbers:
        if one_number % 2 == 0:
            yield one_number
        
        
for one_item in only_evens(range(5, 13)):
    print(one_item)


# In[47]:


def fib():
    first = 0
    second = 1
    
    while True:
        yield first  
        first, second = second, first+second


# In[49]:


for one_item in fib():
    if one_item > 100_000_000_000:
        break
        
    print(one_item, end=' ')


# # Exercise: read_n
# 
# Define a generator function, `read_n`, which takes two arguments:
#     - `filename` (a string, with a filename)
#     - `n` (an integer)
#     
# Normally, when we iterate over a file, we get one line at a time. `read_n` should return `n` lines at a time, as a single string.
# 
# If you get to the end of the file and there aren't enough lines to complete `n`, then just return (or should I say `yield`?) what you have.
# 
# Hint: The `readline` method for files always return a string with the next line. If you're at the end of the file already, it returns an empty string.

# In[57]:


def read_n(filename, n):
    f = open(filename)
    
    while True:
        output = []
        for i in range(n):
            output.append(f.readline())
            
        s = ''.join(output)
            
        if s:  # if we have a non-empty string s, then yield it
            yield s

        else:  # if s is empty, then we don't have any more lines to return
            break

for one_chunk in read_n('/etc/passwd', 9):
    print(one_chunk)       


# In[58]:


g = read_n('/etc/passwd', 9)


# In[59]:


next(g)


# In[60]:


g


# In[61]:


dir(g)


# In[62]:


g.gi_code


# In[63]:


g.gi_code.co_varnames


# In[64]:


g.gi_code.co_code


# In[65]:


dis.dis(g.gi_code.co_code)


# In[66]:


dir(g.gi_frame)


# In[67]:


g.gi_frame.f_locals


# In[69]:


g.gi_frame.f_lineno


# In[74]:


f1 = open('mydata.txt', 'w')
f2 = open('mydata.txt', 'w')


# In[75]:


f1.write('aaaaaa\n')
f2.write('bbbbb\n')


# In[76]:


f1.close()


# In[77]:


get_ipython().system('cat mydata.txt')


# In[78]:


f2.close()


# In[79]:


get_ipython().system('cat mydata.txt')


# In[80]:


f1 = open('mydata.txt', 'a') # opening in append mode adds, rather than replaces
f2 = open('mydata.txt', 'a')

f1.write('!!! aaaaaa\n')
f2.write('@@@@ bbbbb\n')


# In[81]:


f1.close()


# In[82]:


f2.close()


# In[83]:


get_ipython().system('cat mydata.txt')


# In[85]:


# list comprehension  -- creates a list based on an iterable
[x*x
for x in range(-5, 5)]


# In[86]:


# set comprehension  -- creates a set based on an iterable
{x*x
for x in range(-5, 5)}


# In[87]:


# dict comprehension  -- creates a dict based on an iterable
{x : x*x
for x in range(-5, 5)}


# In[88]:


# if I use round parentheses, do I get a tuple comprehension?
(x*x
for x in range(-5, 5))


# In[89]:


# tuple comprehensions don't exist
# but generator comprehensions (aka generator expressions ) do!


# In[91]:


g = (one_number
 for one_number in range(10, 25)
if one_number % 2 == 0)


# In[92]:


for one_item in g:
    print(one_item)


# In[93]:


mylist = ['abcd', 'efgh', 'ijkl']

'*'.join(mylist)


# In[94]:


# what if I want to join numbers?
mylist = [10, 20, 30]

'*'.join(mylist)


# In[95]:


# I have a sequence of integers
# I want a sequence of strings
# I can turn an int into a string with str()

'*'.join([str(one_number)
          for one_number in mylist])


# In[96]:


# use a generator expression instead of a list comprehension
'*'.join((str(one_number)
          for one_number in mylist))


# In[97]:


# when we pass a generator expression as an argument to a function,
# we don't need two sets of parentheses!
'*'.join(str(one_number)
          for one_number in mylist)


# # Exercise: Word lengths
# 
# Using a generator expression, calculate the total of all word lengths in a file. Your comprehension should return the length of each word.  Then you can use `sum` to sum those all together.  You'll thus get the lengths of the words in the file.  You can assume that whitespace separates words.

# In[98]:


[x*x                 # SELECT
 for x in range(5)   # FROM
 if x%2 ]            # WHERE


# In[99]:


get_ipython().system('cat wcfile.txt')


# In[104]:


# I have a file, which I can read one word at a time (using read().split())
# I want to create a list of integers
# I can use len() to measure the length of each word

sum([len(one_word)
for one_word in open('wcfile.txt').read().split()])


# In[106]:


# nested comprehension 

sum(len(one_word)
 for one_line in open('wcfile.txt')  # iterate over lines in the file
 for one_word in one_line.split())   # iterate over the words in one_line.split()


# In[108]:


# nested comprehension 

sum(len(one_word)                       # (5) 

    for one_line in open('wcfile.txt')  # (1) iterate over lines in the file
    if len(one_line) > 10               # (2) 
    
     for one_word in one_line.split()   # (3) iterate over the words in one_line.split()
     if len(one_word) > 3)              # (4) 


# In[109]:


g = (len(one_word)                       # (5) 

    for one_line in open('wcfile.txt')  # (1) iterate over lines in the file
    if len(one_line) > 10               # (2) 
    
     for one_word in one_line.split()   # (3) iterate over the words in one_line.split()
     if len(one_word) > 3)  


# In[110]:


next(g)


# In[111]:


next(g)


# In[114]:


g.gi_frame.f_locals


# In[115]:


next(g)


# In[116]:


g.gi_frame.f_locals


# In[117]:


next(g)


# In[118]:


g.gi_frame.f_locals


# In[119]:


def double(numbers):
    for one_number in numbers:
        yield one_number * 2


# In[120]:


list(double([10, 20, 30]))


# In[122]:


(one_number * 2
  for one_number in [10, 20, 30])


# In[123]:


def double(numbers):
    return (one_number * 2
      for one_number in numbers)


# In[124]:


# there's basically no difference between cell 119 and cell 123


# In[ ]:




