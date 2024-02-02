# On the art of data manipulation

All programs are ultimately no more than very elaborate machines, moving around little pieces of memory from place to place, determined by
little patterns contained in these blocks of memory. At least, this was the vision of one of the first - and greatest - computer scientists
who ever lived - Alan Turing.

Though the concept of every program as nothing but a state machine might seem unproductive - I mean, we created abstract datastructures for a
reason, right? - it is a very useful tool to use when facing any unfamiliar program. Whether it be written in something high-level like JS,
or very low level like FORTRAN, all programs can ultimately be broken down into operations that move around memory from one place to another,
or read from pre-existing memory to decide what to do. Often when facing a program I don't understand, especially if it's a block of syntax
that I'm not familiar with, a little bit of thought into what bits are moving from where to where can make it a lot easier.

And in practice, memory manipulation isn't only a tool, it's an art. Much of competitive programming is about threading a balance between two
things - writing a simple enough solution that can be debugged quickly without collapsing into spaghetti, and designing an algorithm elegant
and efficient enough to run within some given time frame.

Efficiency in an algorithm ultimately comes down to how many pieces of data it needs to move around to produce a result. This is actually more
direct than one might expect! Even trivial operations such as addition and subtraction are ultimately directives that tell the CPU to move
bits into its registers and calculate their sum, storing its result in another register.

There's an art to the flow of the bits through a program as it runs - it's like watching the work of decades of programming gods work together
in unison with your own hastily-written code, which begins to look increasingly clumsy in comparison. But not all languages have this art.

In assembly, variables don't even exist; they are, to assembly, restrictive blinds that only serve to limit the vast possibilites of the computer
while giving us programmers some idea of control. Nevertheless, it is a beautiful language, so close to the native tounge of the computer itself
it barely needs to be compiled. And it is immensely powerful - not in terms of speed, but it can simply do things that other languages cannot.

I know people who are fluent in assembly, and their perspectives on programming were what drew me to learning C++ in the first place. I know
people who mix inline assembly with C because they can optimize better than the compiler can. I know people who painstakingly optimize every
function to its limits, talking not in terms of big O notation, but in terms of individual CPU cycles. It's a form of unity with the computer
that I can only dream of achieving.

Low-level languages (I say low-level, but it's really all relative) such as C or C++ offer a sort of functional middle ground. They have enough
abstraction to do functionally large tasks, unlike the extremely low level, but have a deep enough connection to the computer that they can
use to the fullest extent the minute details of how a computer's memory works. C has variables, but its variables are extremely simple - there
isn't any of the object-oriented clutter that other languages have - storing the bits that represent a variable's values directly. C doesn't
have variable length, appendable strings; rather, it stores strings as arrays of characters. Even arrays make intuitive sense how they work -
to allocate an array of length n, one simply allocates the amount of memory necessary for one element, multiplied by n. And arrays aren't even
some odd datatype, like they are in JavaScript, but simply a pointer to the first element of the array, which the programmer can perform
pointer arithmetic on to find the value of different elements.

Pointers, the side of C++ that new programmers dread, are in actuality so shockingly simple both in what they are and how they work - as most
low-level concepts tend to be. What's a call stack? Assembly could tell you lots about that. Why is it easy to have an array with integer
indices, but hard to have a datastructure with string indices? C/C++ linear memory and pointer arithmetic shows that pretty nicely.

This is the type of data manipulation that higher level languages lose. Even Java, which is a relatively low-level language, doesn't have
much of this manual control. For example, what does it mean to "pass by reference"? In Java, they use a `Ref<T>`, but what even is a `Ref<T>`,
and how does it pass by reference? In C, to pass by reference literally means to *pass the reference to the variable*, to pass the pointer
to the location in memory where the variable resides. Java has a garbage-collection system floating around in the background, but what does
it do? How does it collect garbage, and more importantly, how does it know what is garbage and what isn't? C has, in my opinion, the best
garbage collection system in existence - `malloc(n)`, which allocates `n` units of memory, and `free(p)`, which frees the memory specified
by the pointer `p`. With C, I don't have to worry about when a variable will be gc'ed, or which ones will; rather, I simply have to make it
happen.

Low level programming is an art. I remember the first time I got a linked list to work in C++, using some combination of pointers and heap
allocations - how many Python users can tell you when a variable is allocated on the stack or heap? I don't even know myself if Python
differentiates between the two - and I could look back over my code and see so clearly why it worked. Memory manipulation is so magical
because it works.

Memory manipulation and optimization come hand in hand - as a rule of thumb, when I am optimizing a program, I think about it in terms of
what it's storing and moving around: Where does the memory come from, and where does it need to be? And importantly, what's the best and simplest
way to store the memory in between those two events?

Let's say that we're given a sentence, and want to find only the second word of it. The high-level solution to do this would be to run
`string.split(" ")` or some equivalent method, and extract the second element of it. But this is not good from a bare memory standpoint.
What exactly does `string.split()` do, and how is it moving around memory? Will it be able to know that we only need the second word, or
will it do potentially a huge amount of extra computation that isn't needed?

The solution that comes to mind for me is to use some sort of for loop or iterator to step through the characters of the string one by one,
and appending these into an output string, until te second space character is found. However, this looks like a worse solution - it looks like
it does more operations - O(n) rather than O(1), right?

This is where we have a disconnect - what time complexity is `string.split()` exactly?

It probably uses an algorithm similar to what I described, appending characters into a buffer and flushing it each time the character to split on
is found. But ultimately, if one wants to truly know how their program behaves, they have to use datastructures and methods that they fundamentally
understand how they work internally, or write up their own algorithm that they can fully understand. This sounds like it goes against the tenents
of what makes an abstract datastructure abstract - and it does. But I don't think abstraction is always a good thing.

That's my issue with high-level languages. It's why I don't like Python - not for the odd syntax, but because it's never fully clear what the
program is doing, especially with its use of iterators and overloads thrown everywhere, not to mention that most variables are objects and stem
from some rooted inheritance tree.

Low level programming techniques are an art. Abstraction kills that art.

But I suppose we can't have everything. Python is undoubtedly an amazing language for writing simple, quick programs on the fly, and I do
use it for this exact purpose quite often. Hopefully, though, I'm not the only one who sees art in the mundane of manual data manipulation -
as in this new age of generative AI, it may one day be lost to time.
