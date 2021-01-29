# To Do

* Define script for globally renaming variable names across all files. Useful
for channels.

# Documentation

Documentation is stored in '/html'.

Documentation shall be performed using 'pdoc', as it is simple. Perfect for grad
students. 

Whenever possible, divide code into functions, modules, etc. and document those
functions via  'docstrings'. These keeps the documentation close to the source
and allows pdoc to find it. The docstrings use markdown, as well as reST?, and latex**!**.

To use inline equations, type `\\(...\\)`. For a block, use `$$...$$` or `\\[...\\]`.

See [the pdocs documentation](https://pdoc3.github.io/pdoc/doc/pdoc/#gsc.tab=0) 
for more.

Run `compile_documentation.bat` to compile the docs. It will work if the labscript
is on an anaconda install.

If you wish to build documentation see `labscriptlib.html` for more.

# Virtual Environments

I am not familiar with the use of virtual environments. I know only that they 
are used to maintain independent versions of different programs. 

Code writing unfortunately involves a lot of debugging and determining the 
idiosyncracies of every function defined in the libraries you're using for 
development. These are at the whims of the developer and may change at any time.
No library is perfect in what ever respect you define at the outset, and so the 
developer might decide to change the syntax needed to do something. Rather than
have to rewrite *perfectly working* code, one can use a virtual environment to 
keep the libraries young for eternity. And if one needs to move or try updates,
transfer to a new virtual environment without breaking existing code.

That's all I know. If you want to learn more about how to actually implement 
these ideas in practice. Use google.

I'm using conda to manage virtual environments I believe. They are used via 
`conda activate ybclock` commands in the Anaconda Powershell. Use that as a starting point for understanding
how this virtual environment management is implemented. See [the labscript docs](https://docs.labscriptsuite.org/en/stable/installation/regular-anaconda/) for
more. Hopefully, that link won't break in the future.

# Using Sequences

Open up `runmanager (ybclock)` and select the sequence you want. (De)select
run/view shots as you please. 

For testing compilation, turn off run/view shot then engage.

# Sequence File Structure

Sequence files can be stored anywhere. The way they import modules makes them
free to be wherever. So you can use whatever folder structure you desire to
organize the large number of sequences that will arise in the future.

I have them in `ybclock.sequences`

# Subsequence File Structure

The sequence must be defined in compartmentalized sections. That means a file
for a the Loading Sequence, maybe a file for the green mot, maybe for the blue.
A file for pumping sequence, and so on. A top-down partition is a MUST for
posterity, readability, and debugging. How 'down' you go is up to you. Too many
files for especially simple sequences is counter productive. As with everything
in life, this is an art.

See 'loading_sequence.py' for a good example. It has a function in there you can
 call to include it in the main sequence, or if you just want to run it in
constant mode to optimize the mot by hand you can, as there is a second block
for allowing compilation by run manager.

# Recommended Programming Environment

Use Sublime Text, and Sublime Merge for a fantastic text editor and repository
manager respectively.  Use the elasticTabstops package in Sublime Text! Very
useful for maintaining readable code.
