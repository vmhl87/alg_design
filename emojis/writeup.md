### The project

In this CS project, a Processing sketch reads webcam input and then processes it, dividing it into squares and drawing for each square the chromatically most similar emoji. To make this as efficient as possible, I used a datastructure called an Octree to categorize and sort the emojis.

To "sort the emojis", I wanted to reorganize the emojis into a structure that would order them in order of their R, G, and B values. This would enable a binary search-type algorithm which could crawl through the sorted emojis and on O(log n) time determine the optimal emoji.

However, sorting the emojis wasn't as simple as plugging it into mergesort. Sorting in the standard sense can only sort linearly based on a single value, but I needed to sort the emojis based on three fields. In other words, a simple sort would organize my data points along a single 1-dimensional line, but I needed to organize the data in three dimensions - into the 3-dimensional RGB "color space".

### Organizing the data

The performance improvements of a {log n} algorithm were too big to ignore, however, so I came up with another way to implement binary search - not with a sorted list and a binary search algorithm, but with a binary tree representing the data.

When we think about traditional binary search, we usually picture a list of objects, of which we divide in half, and see if our target is on the left or right side.

```js
{* * * * ! * * *}
 * * * *{! * * *}
 * * * *{! *}* *
 * * * *{!}* * *
```

However, if we compare the search paths of binary search of elements that are close together on the list, we can notice:

```js
{* ! * * * * * *}  {* * ! * * * * *}  {* * * ! * * * *}
{* ! * *}* * * *   {* * ! *}* * * *   {* * * !}* * * *
{* !}* * * * * *    * *{! *}* * * *    * *{* !}* * * *
 *{!}* * * * * *    * *{!}* * * * *    * * *{!}* * * *
```

Items close together on the list share parts of the search path with one another, and items farther apart share less of the search path with one another. In fact, we can notice that two items will share the same search path up until a point, where they diverge, and no longer have the same search path after that point. We can see that these search paths in fact make up a binary tree.

```js
     {* * * *}
      /     \
{* *}* *   * *{* *}
           /     \
      * *{*}*   * * *{*}
```

Another way to think about this type of search tree is that each node, and its "bounds", which are represented with {}, represents all the locations where the target could be in. Similarly, each subnode tightens the bounds by eliminating several locations where the target is known to not exist.

Unlike the sorted array-implementation of binary search, this method of using a binary tree does not depend on the data being easily linearizable.

Say that I wanted to organize my data with respect to two quantities, x and y. To do this, I would simply have to change the binary search tree so that it wouldn't split into only two sides - rather, it would split into four subnodes, each one determined by a tightened x and y range.

Utilizing this approach to organize with respect to three fields results in an 8-split tree, or in other words, an octree.

### Implementation

Because the data now had to be organized into a search tree, I wrote a separate program to preprocess the emojis into a tree.

First, I had to read the emojis and calculate the average color; another team member already did this, and so I reused their code.

In the tree, I didn't need to store the emojis themselves, so I created a datastructure to store each emoji:

```java
class Emoji{
	float[] value;
	Emoji(color c){
		value = new float[3];
		value[0] = red(c);
		value[1] = green(c);
		value[2] = blue(c);
	}
}
```

Then, to store the nodes in the tree, I created a node datastructure:

```java
class Node{
	float split;
	int left;
	int right;
	boolean end = false;
	float[][] bounds;
	boolean finished;
	int rgb;
	Node(){
		bounds = new float[3][2];
		finished = false;
	}
}
```

Because nodes could be either ending nodes (which pointed to a single emoji) or tree nodes (which split into several nodes), I included an `end` flag.

To simplify the traversal of the emojis I actually broke down each node (which theoretically would split into 8) into a series of nodes, each which split into 2, but chained. They first split on the Red quantity, then on Green, and then on Blue. This was stored in `rgb`.

For computation, I also stored the bounds (in terms of upper and lower bounds on each quantity R, G, and B) in a float array.

To link this node to its next nodes in the tree, I stored two integers Left and Right. Essentially, because this data was to be preprocessed, I wanted to store it in a format that was easily writable to a text file, and readable from one too. I found that the easiest way to do so was to have a different node on each line, and for one node to link to others, it would store the line numbers of its next nodes.

The actual computation was slightly tedious, and I ran into several issues where emojis with identical color caused infinite loops, and other issues with line numbers being offset, but in the end, I had a Processing file (`octreeparse.pde`) which would read from the same dataset of emojis as the webcam sketch, and compute the dumped tree (`octree_dumped.txt`) which could then be read in by the webcam sketch.

Traversing the tree on the recieving end was very easy. The tree was loaded into a large array, and to compute the closest emoji given an input color, I wrote a method to start at the first node, and recursively travel to the correct next node, until an ending node was reached.

### Performance

Though a brute-force O(n) search is fast enough to produce a relatively high-refresh rate image, we ultimately wanted to run the program on an old laptop so that it could be continously displayed at all times. This was not a very fast computer, and it ran noticeably a lot better with my O(log n) octree search as opposed to direct search.

The computation of the octree dump didn't take that long either, because the data to be processed wasn't very large.
