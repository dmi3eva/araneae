# text2sql_problems_research

**List of test-sets:**
1. *binary_with_values* - queries that mention binary values (one of two opposite in meaning)
2. *dates_with_values* - queries with dates in differnet formats (time, weekdays, dates, etc.)


**To see profile viaualization:**
https://jiffyclub.github.io/snakeviz/
```
pip install snakeviz
snakeviz log/profiling/load_from_json.prof
```

**To execute linting:**
```
pylint araneae/wrapper.py > log/linting/wrapper.txt
```