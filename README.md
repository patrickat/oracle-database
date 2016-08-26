# oracle-database

## Requirements
**VERY IMPORTANT**: Install the correct version of Python for the architecture for _your_ operating system.

* **[Python](//www.python.org/)**:
 * [2.7](//www.python.org/downloads/release/python-2712/)
 * [3.5](//www.python.org/downloads/release/python-352/)
* **[cx_Oracle](//pypi.python.org/pypi/cx_Oracle/5.2.1)**

## Implementation
After installing the proper files, the code is ready to connect to your Oracle database.

Here are some resources used:
* [Stack Overflow Answer](//stackoverflow.com/a/9853319/6469907)
* [Oracle Tutorial](//www.oracle.com/technetwork/articles/dsl/python-091105.html)

## Example
```python
import collections
import csv
from oracle-database import Oracle

# Set up the namedtuple
User = collections.namedtuple('User', [
  'first_name',
  'last_name',
  'title',
  'active'
])

command = 'SELECT {} FROM {} ORDER BY {}'.format(
  'firstName, lastName, title, active',
  'userTable',
  'lastName'
)

db = Oracle()

# Convert the tuple list into an User list
users = [User._make(u) for u in db.select(command)]

# Save results to an csv
with open('output.csv', 'w') as f:
  w = csv.writer(f)
  w.writerow(('Name', 'Title', 'Active'))
  w.writerows([
    '{} {}'.format(u.first_name, u.last_name), u.title, u.active
    for u in users
  ])
```
