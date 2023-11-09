/*
  Octree-based color to emoji lookup utility
  Code author: Vincent Loh

  Pre: "unrolled octree" computed by c++ preprocessor, inputted as a text file
  Post: a method that can efficiently (in log N time) find the visually closest emoji to an
        arbitrary input color
*/

// init global vars: tree, octreeLoaded
node[] tree;
boolean octreeLoaded = false; // to provide error handling in the case of missing text file

// node class - this represents both branching and ending nodes; components of the tree
class node{
  // in a branching node, v represents the "middle" value to swap around,
  // and l and r represent the indexes of the left and right branches (unrolled tree)
  float v;
  int l;
  int r;
  // however, in an ending node, all we care about is the id of the corresponding emoji, so
  // we store that in l for the sake of memory efficiency
  boolean end=false;
  // we will have two overloaded constructors, one for ending nodes, and the other for branching ones,
  // to make instantiation a bit easier
  node(int ll){
    l=ll;
    end=true; // ctor for end nodes
  }
  // ctor for branch nodes
  node(float vv,int ll,int rr){
    l=ll;r=rr;v=vv;
  }
}

// function that parses unrolled text file and builds it into a more easily parseable data structure
void setupOctree(String inputFile){
  // to avoid cluttering up setup(), we relegate octree unrolling into a separate function
  // our file reader
  BufferedReader reader = createReader(inputFile);
  // now we parse the file; if the file does not exist, we have error handling
  try{
    // input number of lines
    int lines = int(reader.readLine());
    // now that we know the number of lines, we can initialize the tree with proper length
    tree = new node[lines];
    for(int i=0;i<lines;i++){
      // for each line, split on spaces
      String[] s = reader.readLine().split(" ");
      // if the first character is e, it is an ending node, if not, it is a branch node
      if(s[0].charAt(0)=='e'){
        // allocate an ending node; the overloaded ctors come in handy here (note that s[1], the
        // second portion of the line, represents the id of the output emoji
        tree[i] = new node(int(s[1]));
      }else{
        // allocate branch node with overloaded ctor; s[1|2|3] represent the 2nd, 3rd, 4th portions of
        // this line in the octree dump, specifying split value, left index, and right index
        tree[i] = new node(float(s[1]),int(s[2]),int(s[3]));
      }
    }
    // hopefully everything went well and the octree loaded
    octreeLoaded=true;
  }catch(Exception e){
    // error handling (note that this does not set octreeLoaded, preventing unplanned behavior when
    // traversing the non-filled tree
  }
  if(!octreeLoaded)print("Oh no! Octree failed to load.\n  Perhaps the data file is missing - "+
      "verify that `"+inputFile+"` exists in the same directory as this sketch.\n\n");
}

// provide overloaded setupOctree() to provide default behavior in case no input file is given
void setupOctree(){
  setupOctree("octree_dumped.txt");
}

// function that takes in a color and outputs the closest emoji to it
int closestEmoji(color c){
  // error handling
  if(!octreeLoaded){
    print("Warning! Octree is not loaded\n");
    return 0;
  }
  // we will be recursively traversing the tree, so ideally we want to pass some form of
  // information concerning the current node we are looking at. We accomplish this with
  // an overloaded function that can either take in just a color or take in a color, id, and
  // rgb (I will explain what this signifies later) which initially are both set to 0.
  // also, to increase efficiency we will unroll the color into its r,g,b beforehand so we do not
  // have to recompute it in the recursive loop
  return closestEmoji(red(c),green(c),blue(c),0,0);
}

// function (overloaded) that takes in color, id of current node, and rgb and recursively traverses
// tree to find closest emoji
int closestEmoji(float r, float g, float b,int id,int rgb){
  // because dealing with octrees in the traditional sense, where each node splits into eight, is rather
  // complex and prone to error, I chose to apply a second subdivision and split each division of 8 into
  // three separate divisions of 2. This is equivalent to the original subdivision because rather than
  // splitting into 8 sectors based on combinations of red,green,blue, my algorithm splits first on red,
  // then splits on green, and then splits on blue. It's a bit complicated, but in practice is less prone
  // to error. Essentially, rgb is one of {0,1,2} representing either a split on 0(red), 1(green), 2(blue).
  if(tree[id].end){
    // for memory reasons we store the id of the output emoji in `l` rather than a separate property
    return tree[id].l;
  }else{
    // cl = whatever part of the input color that corresponds to which split this node is performing -
    // a split on red will cause cl to be the red part of the color, a split on green will cause cl to
    // be the green part of the color, etc.
    float cl;
    if(rgb==0)cl=r;
    else if(rgb==1)cl=g;
    else cl=b;
    // if this value is bigger than our node's v(the "middle" value), choose the right node. Otherwise,
    //  choose the left node. Also, update rgb.
    if(cl>tree[id].v)return closestEmoji(r,g,b,tree[id].r,(rgb+1)%3);
    else return closestEmoji(r,g,b,tree[id].l,(rgb+1)%3);
  }
}

// --- driver code ---

// it does what it looks like it does
color getRandomColor(){
  return color(random(255), random(255), random(255));
}

// we don't need draw() because we aren't drawing anything
void setup(){
  setupOctree();
  int startTime = millis(),
    k = 100000;
  // run k tests
  for(int i=0;i<k;i++)
    closestEmoji(getRandomColor());
  print(k+" lookups executed in "+(millis()-startTime)+" ms");
}
