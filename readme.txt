===================================================
27/03/2019

We created the class blob that we're going to use
for every new blob that is created. This way, it's
going to be easier to get its position, to change
it, to edit it's name, get the numer of blobs on
the grid...

We also created the function to create the grid,
that is returning a text : this text has to be
printed so that the grid prints in the good way
(otherwise, \n won't work).

We have "2 grids" : one that is just the interface
to be printed thanks to our function, but the other
is where all the informations are store. This last
is a list of lists, containing empty strings where
there is no blobs and a blob object where there is
one blob.

Each blob has 2 "names": one for the interface, which
is just "b" + its number + its weight. But its actual
name is going to be generated randomly, like "Mu",
"Ga", "Yo" ...

The blob has also a color, defined as a tuple (r, g, b)
and a size (which is actually its weight).

We also defined the changePos function, which is going
to change the value of the blob position (self.pos), 
edit the grid (list of lists) to move the blob in the
good position (erase its old position and define its new
one), and also check whether or not there is already a
blob to the position we want to move the blob in.

We also defined a function that is going to generate
a blob randomly (name, position...), and that checks
whether or not there is already a blob at the generated
position for the blob.


HOW TO USE ?
You can try these commands :
	- generate_blob(W) to generate a blob of weight
		less than W
	- generate_blobs(n, W) to generate n blobs of 
		weight less than W
	- print(draw_grid()) to print the grid
	- generate a new blob "b", print the grid, then
		change the blob's position (b.pos = (x, y))
		and print the grid again to see the changes.
