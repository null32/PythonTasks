# Usage
```sh
python3 dep_installer <python_script.py>
```

Sample output for sample test out below
```sh
python3 dep_installer test2.py
[+] socket
[+] numpy
[+] datetime
[+] sys
[+] hashlib
[+] math
[-] some_local_lib
[+] os
```

Sample test file
```python3
import datetime
import sys, os, socket

import numpy
from hashlib import md5
from math import cos, sin
import some_local_lib

print("test")
```