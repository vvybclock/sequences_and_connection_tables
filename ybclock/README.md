Welcome to Ybclock Labscript Edition!

#How to Edit & Build the Documentation

Documentation is stored in '/html'.

Documentation shall be performed using 'pdoc', as it is simple. Perfect for grad
students. 

Whenever possible, divide code into functions, modules, etc. and document those
functions via  'docstrings'. These keeps the documentation close to the source
and allows pdoc to find it. The docstrings use markdown, as well as reST?, and latex**!**.

To use inline equations, type `\\(...\\)`. For a block, use `$$...$$` or `\\[...\\]`.

If you wish to add images, use a `.. image:: .imgs/imagefile.png` type
command. Note, currently, as far as I know, you have to manually move over the
images to the appropiate location in the `/html` build location. With the
batch file provided, pdoc won't move them.

See [the pdocs documentation](https://pdoc3.github.io/pdoc/doc/pdoc/#gsc.tab=0) 
for more.

Run `compile_documentation.bat` to compile the docs. It will work if the labscript
is on an anaconda install.s

If you wish to build documentation see `labscriptlib.html` for more.

.. include:: ./BUGS.md

# Renaming a Variable

Occasionally, you need to rename a channel, either to improve clarity or to
reflect an update. A multi-file search and replace is ideal for this, and
luckily, sublime text does this easily. 

While there is risk of unforseen replacements, an advantage of using long
variable names like we do, is there is reduced chance of errors when
performing a global search and replace. Although it is true, that the search
and replace might be so easy that you forget to update the documentation. 

To prevent this, document first, then perform a global search and replace.

To do this in sublime text, `Find > Find in Files (Ctrl+Shift+F)`, then select
your folder as `labscriptlib/ybclock/` and attempt to find the variable name
in question. Check to see that find is accurate, then write down the variable
name replacement. Double check the replacement spelling. Commit after the
change. This way it's easy to revert any unforseen incidents.



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

# Using Metadata (Essential)

Labscript was designed for BEC/Fermi gas type experiments that involve
manipulation of quantum gases. Such experiments are typically probed via
absorption imaging. A process which is destructive to the atoms, so one can
only measure once at the end of the experiment.

Our experiment isn't at all destructive, while it perturbs the spin state, for
the most part, the atoms are left intact. While the measurement can cause
unwanted heating and spin mixing, the atoms aren't guaranteed to be lost.

This allows us to measure repeatedly. And furthermore we can measure to
extract different aspects of the atomic spin state. Unfortunately, each
measurement can be quite similar in execution. This is essentially scanning
light across the cavity. 

However, *context* on the desired experiment can change analysis. So it's
useful to save **metadata** to be able to simplify analysis. This metadata
lets us easily save parameters that are available when writing the experiment,
that is much harder to infer from the instructions sent to the NI cards (which
is typically the only thing guaranteed to be saved either in your average AMO
lab or in Labscript).

While Labscript does not have wrapper functions for simplifying this process,
thanks to the help of the labscript writers, there exists a method for saving
metadata. The earliest implementation occured in the ExperimentalCavity class,
currently (April 9, 2021) saved in subsequences. (It's location may change in
the future.) See [this google group chat](groups.google.com/g/labscriptsuite/c/5ZzEHWkWft0) 

for more contextual information as well as technical detail. Look for my
questions (Enrique Mendez) to understand the intention. It took a number of
emails to straighten out a mutual understanding. Phil's answers I believe have
the most useful answers as well as technical information for how to store
metadata.

Currently, one must save the metadata in the HDF group 'shot_properties'. This
can be done with `compiler.shot_properties` which is a dictionary. One can
import `compiler` from `labscript`, i.e., `from labscript import compiler`.
This works only when executing a sequence script in runmanager.

To save complicated formats of data like dictionaries (which are quite nice as
they serve the ability to be self documenting since they can be indexed by
strings), one can use the `pickle` library which serializes (turns into a
binary stream), something that doesn't have a predefined algorithm for
serializing. In other words, it allows you to store `dict`s in a file.

Data can be saved by opening up the HDF file directly or using labscripts
techniques for saving data: for example, in lyse, one can use
`run.save_result()`, or in the sequence generation side
`compiler.shot_properties`. 

# Working with HDF files

HDF files are nice, they're sort of like zip files, in that they are one file
that can hold "groups" which are just like Windows Folders, and "datasets"
which are like files, but restricted to multidimensional arrays consisting of
integers or floats. (This means if one wants to save something one needs to
encode it in such a format.)

However, unfortunately, **they are easy to corrupt**. If you access the HDF
file from two programs at once, it will corrupt. So if you leave it open in
python for instance and open it up with an HDF viewer, it will corrupt. So one
needs to take care not to open it from two places at once. This obviously
becomes less risky when working with old datasets (HDFs) as that means
labscript isn't opening the data. The biggest danger I've found is to work on
it with python and then open it up with an external HDF Viewer GUI. So if one
doesn't use the HDF Viewer, as well as only access HDF files via a `with
h5py.File(hdf5_filename, 'r') as hdf5_file:` syntax calls, which always close
the files when you leave their scope, you'll be fine. 

Labscript I believe also takes effort to prevent corruption, but I'm not so
well versed with it's protection techniques. So I'm not sure how much harder
it makes it to mess things up.

It definitely does not protect against 3rd Party Programs from reading an HDF
file simultaneously and causing corruption.

# Recommended Programming Environment

Use Sublime Text, and Sublime Merge for a fantastic text editor and repository
manager respectively.  Use the elasticTabstops package in Sublime Text! Very
useful for maintaining readable code.

# Adding Devices

If you add a new device, it can be defined in either the virtual environment
directory of `labscript_devices` or the local directory `user_devices`.

Every change you make beyond might need to be accompanied by a reset of the
appropriate portion labscript program.  You can get away sometimes with
smaller resets in each of the programs. Try it, but if it fails you know why.

If you edit `labscript_devices`, you definitely need to reset the whole program.