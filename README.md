# gloss
Gloss (short for glossary) is a different kind of dictionary.
All values also automatically become keys and so can be looked
up in the Gloss to find its corresponding 'key'. This makes it
easy to lookup and maintain one-to-one relationships such as a
label to a certain magnitude.

As both the key and value are gettable items from the Gloss and
are indistinguishable once added, `term` is the preferred name
for items in a Gloss, and a `term pair` is the 1-1 mapping each
term belongs to.

Gloss is a MutableMapping and supports all the same methods
that `dict` does.

## Examples
```python
from gloss import Gloss

example = Gloss()
example["stdin"] = 0
example.update({"stdout": 1, "stderr": 2})
print(example)
#Gloss({"stdin": 0, "stdout": 1, "stderr": 2})
print(example[1], "goes to" example["stderr"])
#stdout goes to 2
example[3] = "config.toml"
example[1] = "shell pipe"
print(example)
#Gloss({"stdin": 0, "stderr": 2, "config.toml": 3, "shell pipe": 1})
print([fd_or_desc for fd_or_desc in example])
#["stdin", "stderr", "config.toml", "shell pipe", 0, 1, 2, 3]
```

## Differences from Enum
[Enum](https://docs.python.org/3/library/enum.html) is a wonderful
data structure that also supports 1-1 mappings and it's already built
into Python. However, these limitations of Enums are solved by Gloss:

* enum members are static. They are defined all at once in the
  class and their values cannot change. A Gloss on the other hand
  can be added to, altered, even have members deleted or popped,
  all at runtime
* Accessing Enum member names and their values are different
  operations. Looking up a member by name is done with either dot
  dereference or getitem; looking up a member by value is done
  with a call. With a Gloss you don't have to know which side of
  the mapping your key is on (if there even is a distinction to the
  mapping), it is all done by getitem
* One side of an enum mapping must be a string. Because member
  names are attributes they must follow Python identifier naming
  rules. In a Gloss, all terms may be any hashable object

## Differences from Dict
While the classic dict solves some of the limitations of using an Enum,
primarily being mutable at runtime, it is not a 1-1 mapping.

* enforcing uniqueness among dict values is a lot of extra work
* looking up a dict value is O(n). Therefore so is updating, deleting,
  popping, etc that value. Searching a Gloss for any term is O(1) time
* updating any term in a Gloss takes a single operation
