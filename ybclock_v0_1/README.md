# Using Sequences

Open up runmanager (ybclock_vX_X) and select the sequence you want. (De)select run/view shots as you please. 

For testing compilation, turn off run/view shot then engage.S

# File Structure

This folder contains full-fledged experimental sequences and the connection_table. If you have an experiment that uses a different connection table, it should go in the next version of ybclock_vX_X, i.e. ybclock_v0_2. This helps seperate code that was written for different wiring setups.  Things that return full data sets upon completion. Subsequences which are components of each full sequence are held in the subfolder labeled 'subsequences'.

# How to Define Sequence Sections

The sequence must be defined in compartmentalized sections. That means a file for a the Loading Sequence, maybe a file for the green mot, maybe for the blue. A file for pumping sequence, and so on.
A top-down partition is a MUST for posterity, readability, and debugging.
How 'down' you go is up to you. Too many files for especially simple sequences is counter productive. As with everything in life, this is an art.

See 'loading_sequence.py' for a good example. It has a function in there you can 
call to include it in the main sequence, or if you just want to run it in constant mode to optimize the mot by hand you can, as there is a second block for allowing compilation by run manager.

# Programming Environment

Use Sublime Text, and Sublime Merge for a fantastic text editor and repository manager respectively. 
Use the elasticTabstops package in Sublime Text! Very useful for maintaining readable code.