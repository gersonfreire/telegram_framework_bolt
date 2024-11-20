Here are some examples of using the

exec

 function at runtime:

### Example 1: Defining a Function

```python
code = """
def greet(name):
    return f"Hello, {name}!"
"""

local_vars = {}
exec(code, {}, local_vars)

# Call the defined function
result = local_vars['greet']('World')
print(result)  # Output: Hello, World!
```

### Example 2: Modifying a Variable

```python
code = """
x = 10
x = x + 5
"""

local_vars = {}
exec(code, {}, local_vars)

# Access the modified variable
result = local_vars['x']
print(result)  # Output: 15
```

### Example 3: Executing Multiple Statements

```python
code = """
a = 5
b = 10
c = a + b
"""

local_vars = {}
exec(code, {}, local_vars)

# Access the result of the executed statements
result = local_vars['c']
print(result)  # Output: 15
```

### Example 4: Using Loops

```python
code = """
result = []
for i in range(5):
    result.append(i * i)
"""

local_vars = {}
exec(code, {}, local_vars)

# Access the result of the loop
result = local_vars['result']
print(result)  # Output: [0, 1, 4, 9, 16]
```

### Example 5: Conditional Statements

```python
code = """
x = 10
if x > 5:
    result = "x is greater than 5"
else:
    result = "x is not greater than 5"
"""

local_vars = {}
exec(code, {}, local_vars)

# Access the result of the conditional statement
result = local_vars['result']
print(result)  # Output: x is greater than 5
```

These examples demonstrate how you can use the

exec

 function to execute dynamically generated code at runtime and access the results through the

local_vars

 dictionary.
