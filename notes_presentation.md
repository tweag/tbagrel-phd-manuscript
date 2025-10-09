## Slide 1 - Programming languages

As many of you know, there exists many different programming languages, each with their own strengths and weaknesses, being more suitable for certain type of tasks or uses.
Among these, common distinction: imperative languages and functional ones.
Imperative languages are the most know, and are based on a sequence of instructions that change the memory state of the program. In these, mutations happens frequently, and side effects, that is, interaction with the outside world (e.g. file read) can happen at any time.
In functional languages, instead, the main building blocks are functions and expression. Often, they describe what to do/obtain, rather than how to do obtain it. Commonly, they tend to avoid mutations and untracked side effects, in favor of immutability and pure functions (side effects are pushed to the boundaries of the program as much as possible)

## Slide 2 - Functional languages - why?

During my thesis, I focused on functional programming languages, because albeit a bit less known than imperative ones, they present interesting properties.

Among those, they are often quite close to their mathematical foundations, which makes reasoning about programs easier, especially when doing static analysis, aka. studying the properties of a program without running it.

One consequence of their proximity with pure mathematical models is that we often don't want to care about memory management explicitly, and prefer that the language runtime handles it for us, through automatic garbage collection.

## Slide 3 - Functional data structures

Let's see what the memory representation of functional data structures looks like. Here we take Haskell as the reference language, but the same concepts apply to many other functional languages as well.

In Haskell, OCaml, etc, a data structure is made of blocks, called *heap objects*, that are linked together through pointers. Each heap object represent a data constructor, and a given field of this constructor can only contains a primitive type (e.g. `Int#`) or a pointer to another heap object.

The first bytes of a heap object are reserved for a pointer to a header, aka. info table, which is the identity card of the corresponding data constructor.

Here we see on screen how a list of integers is represented in memory. The colon operator is cons, that is, the data constructor corresponding to a single link of the linked list. The bracket aka. nil operator is the empty list.

## Slide 4 - Building order in functional languages - current

This memory organisation of data structure as a tree of heap objects, and the fact that data structures are immutable, has some consequences on how data structures are built in these languages. 

Notably, in the case of lists, we can only join together a front value with an existing list to create a new list through the cons data constructor. So to build the list [1,2], we have to start by creating the list containing just 2 (by joining the value 2 and nil), and then we can join the value 1 with this list to obtain the list [1,2], as displayed on screen.

As you might imagine, this is quite restrictive, and might not always be the order we want to build our data structures in.

## Slide 5 - Building order in functional languages - goal

So what about relaxing this restriction, and allowing to build data structures in any order, by joining our blocks however we want?

E.g, we could decide to first create the list containing the value 1, with no tail yet, and only later connect it to the tail containing the value 2.

But doing so means our data structures, at some point during their construction, will be in an invalid state, as they will contain holes, displayed as red squares on screen, that is, some fields of the data constructors won't be initialized until later.

## Slide 6 -- Challenges

Having holes in our data structures is of course creating new challenges for functional languages:
- First, it means our memory model is not purely immutable anymore, as we will need to mutate the unitialized fields later on to give them a value
- Second, it means that our structures are no longer safe to read at any time. Indeed, it would be highly problematic to try to read the value of a field that is not initialized yet, as it would lead to unpredictable behaviour/segfault.

Hence, we will need to encapsulate these appearingly impure and unsafe operations in a functional interface, that ensures that the user won't suffer from the oddities happening under the hood.

