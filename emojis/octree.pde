// global vars: tree, octreeLoaded
ArrayList<node> tree;
boolean octreeLoaded = false; // to provide error handling in the case of missing text file

// node class - this represents both branching and ending nodes
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
void setupOctree(){
  // to avoid cluttering up setup(), we relegate octree parsing into a separate function
  // first we initialize the node tree and our file reader
  tree = new ArrayList<node>();
  BufferedReader reader = createReader("octree_dumped.txt");
  // now we parse the file; if the file does not exist, we have error handling
  try{
    // input number of lines
    int lines = int(reader.readLine());
    for(int i=0;i<lines;i++){
      // for each line, split on spaces
      String[] s = reader.readLine().split(" ");
      // if the first character is e, it is an ending node, if not, it is a branch node
      if(s[0].charAt(0)=='e'){
        // allocate an ending node; the overloaded ctors come in handy here (note that s[1], the
        // second portion of the line, represents the id of the output emoji
        tree.add(new node(int(s[1])));
      }else{
        // allocate branch node with overloaded ctor; s[1|2|3] represent the 2nd, 3rd, 4th portions of
        // this line in the octree dump, specifying split value, left index, and right index
        tree.add(new node(float(s[1]),int(s[2]),int(s[3])));
      }
    }
    // hopefully everything went well and the octree loaded
    octreeLoaded=true;
  }catch(IOException e){
    // error handling (note that this does not set octreeLoaded, preventing unplanned behavior when
    // traversing the non-filled tree
    print("Oh no! Octree failed to load.\n  Perhaps the data file is missing - "+
      "verify that `octree_dumped.txt` exists in the same directory as this sketch.");
  }
}

// function that takes in a color and outputs the closest emoji to it
int closestEmoji(color c){
  // error handling
  if(!octreeLoaded){
    print("Warning! Octree is not loaded");
    return 0;
  }
  // we will be recursively traversing the tree, so ideally we want to pass some form of
  // information concerning the current node we are looking at. We accomplish this with
  // an overloaded function that can either take in just a color or take in a color, id, and
  // rgb (I will explain what this signifies later) which initially are both set to 0.
  return closestEmoji(c,0,0);
}

// function (overloaded) that takes in color, id of current node, and rgb and recursively traverses
// tree to find closest emoji
int closestEmoji(color c,int id,int rgb){
  // because dealing with octrees in the traditional sense, where each node splits into eight, is rather
  // complex and prone to error, I chose to apply a second subdivision and split each division of 8 into
  // three separate divisions of 2. This is equivalent to the original subdivision because rather than
  // splitting into 8 sectors based on combinations of red,green,blue, my algorithm splits first on red,
  // then splits on green, and then splits on blue. It's a bit complicated, but in practice is less prone
  // to error. Essentially, rgb is one of {0,1,2} representing either a split on 0(red), 1(green), 2(blue).
  // Load the current node into memory. This is slightly more efficient than querying the arraylist every
  // time the properties of the node need to be accessed, and takes up nearly no space.
  node n = tree.get(id);
  if(n.end){
    // for memory reasons we store the id of the output emoji in `l` rather than a separate property
    return n.l;
  }else{
    // cl = whatever part of the input color that corresponds to which split this node is performing -
    // a split on red will cause cl to be the red part of the color, a split on green will cause cl to
    // be the green part of the color, etc.
    float cl;
    if(rgb==0)cl=red(c);
    else if(rgb==1)cl=green(c);
    else cl=blue(c);
    // if this cl is bigger than v(the "middle" value), choose the right node. Otherwise, choose the
    // left node. Also, update rgb.
    if(cl>n.v)return closestEmoji(c,n.r,(rgb+1)%3);
    else return closestEmoji(c,n.l,(rgb+1)%3);
  }
}

// --- driver code ---

// tiny utility to test colors -> emojis
void testClosestEmoji(color c){
  print("Testing closest emoji: color red:"+red(c)+", green:"+green(c)+", blue:"+blue(c)+"\n");
  print("Output emoji: "+closestEmoji(c)+"\n\n");
}

// it does what it looks like it does
color getRandomColor(){
  return color(random(255), random(255), random(255));
}

// we don't need draw() because we aren't drawing anything
void setup(){
  setupOctree();
  int startTime = millis(),
    k = 300;
  // print k tests
  for(int i=0;i<k;i++)
    testClosestEmoji(getRandomColor());
  print(k+" lookups executed in "+(millis()-startTime)+" ms");
}
