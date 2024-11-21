# OOP
I'm not super used to Object-Oriented Programming.
blah blah blah...

### Diamond Problem
Consider four classes. Class `A` is our parent/super class, class `B` and `C` inherit from `A`, and `D` inherits from both `B` and `C`
#todo an inheritance diagram here would go craaaaazy

Suppose class `A` has a method that is overridden by `B` and `C`. The method is *not* overridden by `D`
###### Example Script
```python
class A:
	def m(self):
	print("inside A")

class B(A):
	def m(self):
		print("inside B")

class C(A):
	def m(self):
		print("inside C")

class D(B, C):
	pass

# and fifth more sinister class for good reason
class E(C, B):
	pass

obj1 = D()
obj2 = E()
obj1.m()
# Output: inside B
obj2.m()
# Output: inside C
```
The order of parent classes decide which class `D` and `E` inherit from!