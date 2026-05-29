# csc.SystemVariables

> 公式: https://cascadeur.com/python-api/_generate/csc.SystemVariables.html

Contains static methods related to system variables of Cascadeur.

## Methods

- **`git_count()`** → `str`
  - Returns the git count of the current repository.

- **`git_date()`** → `str`
  - Returns the git date of the current repository.

- **`git_sha()`** → `str`
  - Returns the git SHA hash of the current repository.

- **`git_version()`** → `str`
  - Returns the git version of the current repository.

## Example

```python
import csc
print(csc.SystemVariables.git_sha())
print(csc.SystemVariables.git_date())
print(csc.SystemVariables.git_count())
print(csc.SystemVariables.git_version())
```
