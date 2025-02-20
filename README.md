### README.md

# Description
Python script to get top packages and their frequencies for given debian architecture. 

# How to run
For local machines:
Install python
First, run `pip install -r requirements.txt` to install required packages
Navigate to `src/main/`  and run `python main.py <ARCHITECTURE>`
Using github actions
Go to Actions tab, click on "Code Test" workflow
Under run workflow, enter desired architecture
Click into the job, then click into the Get Package Info step to see output

# Time Spent
2 hours

# Algo
```
pkgs = []
lines = get_data(URL)
for line in lines:
  current_packages = lines[1]
  pkgs += current_packages
counter(pkgs).most_common(10)
```

