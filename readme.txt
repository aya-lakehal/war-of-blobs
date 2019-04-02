
=== 20/03/19 ===

Creation of the class "blob" that we're going to use
for every new blob that is created. This way, it will
be easier to get its position, to change it, to edit
its name, get the number of blobs on the grid...


=== 26/03/19 ===

Creation of the "draw_grid" function to create the
grid, that is going to be printed on the console.

We have "2 grids" :
	* The first one is just the interface to be
	printed thanks to our previous function
	* The second one is where all the informations
	are stored (positions of blobs, empty cells...).
	It is is a list of lists, containing empty strings
	where there are no blobs and a "blob" object where
	there is one blob.

Each blob has 2 "names": one for the interface, which
is just "b" + its number + its weight (its actual
name is going to be generated randomly, like "Mu",
"Ga", "Yo"... but not printed)

A blob has also a color, defined as a tuple (r, g, b)
and a size (which is actually its weight). The r, g
and b values are between 0 and 1 with at most 2 decimals.


=== 27/03/19 ===

Definition of the "changePos" method, which is going
to change the value of the blob's position (self.pos), 
edit the grid (list of lists) to move the blob to the
right position (erase its old position and define its
new one), and also check whether or not there is already
a blob to the position where we want to move the blob.

Also, definition of a function that is going to generate
a blob randomly (name, position...), and that checks
whether or not there is already a blob at the generated
position for the blob. Also, we created a function
"generate_blobs" that uses the previous function to
generated several blobs.


=== 31/03/19 ===

Creation of the "next" function that simulates the next
step of the simulation. However, this function is TEMPORARY
as it is random (which is not the purpose of this simulation). 

Addition of the colorization of the blobs : for that, we
used the module "ansicolors", which we imported as "colors".
Now, every blob's weight is colorized in the console,
depending on the blob's color attribute (that we had to
convert from values in [0:1] to values in [0:255])


==============
 HOW TO USE ?
==============

You can try these commands :

* From a terminal, navigate through the project's
directory and type the following command :
	python3 main.py
And see what happens

* In a python console : 
	- generate_blob(W) to generate a blob of
	weight less than W
	- generate_blobs(n, W) to generate n
	blobs of weight less than W
	- print(draw_grid()) to print the grid
	- generate a new blob "b", print the grid,
	then change the blob's position (b.pos = (x, y))
	and print the grid again to see the changes.
	
	
=====================================================================

GitHub link of the project : https://github.com/luddoz-c/war-of-blobs
(Feel free to open an issue if you detect some problems)
