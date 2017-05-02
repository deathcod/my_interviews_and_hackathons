## Testing

Fixtures are set of objects that are the base line for testing.

## Problems faced

1) When I was trying to import files from other directories the import was not working than after searching I got to understand the concept of sys path. below is the code which is simple and serves the purpose.

```python3
import os, sys

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(CURRENT_DIR))
```

2) I am very new to software testing so it is very difficult to get to know how to test the database.

3) I faced error that said it cannnot find module etree of lxml. On search on stackoverflow I came to the conclusion that to run lxml I had to download some dependencies, but the problem is in the local system it is managable but how to manage in the aws lambda that was difficult. 

