# pdoc Installation

`pdoc` was installed via 

```
conda activate ybclock_v0_1
conda install pip 
echo '#in case the venv doesn't have pip'
C:\Users\Boris\anaconda3\envs\ybclock_v0_1\Scripts\pip install pdoc3
echo '#uses the venv pip to ensure it installs in the venv'
```

# pdoc Usage

```
ls ./documentation_htmls
pdoc3 --html labscriptlib.ybclock_v0_1
```

The last line generates documentation for the parent folder.