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
pkgs = [] #we can store all packages we find
lines = get_data(URL) # download the data, decompress it into readable format 
for line in lines: # iterate through data
  current_packages = lines[1] # only care about packages. We know the format is such
                                # A filename relative to the root directory, without leading .
                                # A list of qualified package names, separated by comma. A qualified package name has the form [[$AREA/]$SECTION/]$NAME, where $AREA is the archive area, $SECTION the package section, and    
                                # $NAME the name of the package. Inclusion of the area in the name should be considered deprecated.
                                # Therefore only get the relevant list of packages 
  pkgs += current_packages # add the packages to the list of found packages
counter(pkgs).most_common(10) # count the most comon packages
```

