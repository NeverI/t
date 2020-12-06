t with batteries
=======

`t` is a command-line todo list manager for people that want to *finish* tasks,
not organize them. But they also too lazy to type `t` or even forget to type `t -f ID` 
even worst forget something important to do...

Why t with batteries?
------

Yeah, I know, *another* command-line todo list manager.  Several others already
exist ([todo.txt][] and [TaskWarrior][] come to mind), so why make another one?

[todo.txt]: http://ginatrapani.github.com/todo.txt-cli/
[TaskWarrior]: http://taskwarrior.org/

*(And I even forked another one...)*

### It Does the (almost) Simplest Thing That Could Possibly Work

Todo.txt and TaskWarrior are feature-packed.  They let you tag tasks, split
them into projects, set priorities, order them, color-code them, and much more.

**That's the problem.**

It's easy to say "I'll just organize my todo list a bit" and spend 15 minutes
tagging your tasks.  In those 15 minutes you probably could have *finished*
a couple of them.

`t` was inspired by [j][].  It's simple, messy, has almost no features, and is
extremely effective at the one thing it does.  With `t` the only way to make
your todo list prettier is to **finish some damn tasks**.

[j]: http://github.com/rupa/j2/

#### But a task without a due date just a note

For myself I have to assign some due date to task, so I know what I have to do next.
Otherwise I overwhelmed with the never ending task list, so I also want to see my task in that order. 

### It's Flexible

`t`'s simplicity makes it extremely flexible.

Want to edit a bunch of tasks at once?  Open the list in a text editor.

Want to view the lists on a computer that doesn't have `t` installed?  Open the
list in a text editor.

Want to synchronize the list across a couple of computers?  Keep your task
lists in a [Dropbox][] folder.

Want to use it as a distributed bug tracking system like [BugsEverywhere][]?
Make the task list a `bugs` file in the project repository.

[Dropbox]: https://www.getdropbox.com/
[BugsEverywhere]: http://bugseverywhere.org/

### It Plays Nice with Version Control

Other systems keep your tasks in a plain text file.  This is a good thing, and
`t` follows their lead.

However, some of them append new tasks to the end of the file when you create
them.  This is not good if you're using a version control system to let more
than one person edit a todo list.  If two people add a task and then try to
merge, they'll get a conflict and have to resolve it manually.

`t` uses random IDs (actually SHA1 hashes) to order the todo list files.  Once
the list has a couple of tasks in it, adding more is far less likely to cause
a merge conflict because the list is sorted.


Installing t
------------

`t` requires [Python][] 2.5 or newer, and some form of UNIX-like shell (bash
works well).  It works on Linux, OS X, and Windows (with [Cygwin][]).

[Python]: http://python.org/
[Cygwin]: http://www.cygwin.com/

Installing and setting up `t` will take about one minute.

First, download the newest version or clone the this repository
(`https://github.com/NeverI/t.git`).  Put it anywhere you like.

Install some dependency:

    pip install dateparser humanize

Next, decide where you want to keep your todo lists.  I put mine in `~/tasks`.
Create that directory:

    mkdir ~/tasks

Finally, set up an alias to run `t`.  Put something like this in your
`~/.bashrc` file:

    alias t='python ~/path/to/t.py --task-dir ~/tasks --list tasks'

Make sure you run `source ~/.bashrc` or restart your terminal window to make
the alias take effect.

Using t
-------

`t` is quick and easy to use.

### Add a Task

To add a task, use `t [task description]`:

    $ t Clean the apartment.
    $ t Write chapter 10 of the novel.
    $ t Buy more beer.
    $

### List Your Tasks

Listing your tasks is even easier -- just use `t`:

    $ t
    9  - Buy more beer.
    30 - Clean the apartment.
    31 - Write chapter 10 of the novel.
    $

`t` will list all of your unfinished tasks and their IDs.

### Finish a Task

After you're done with something, use `t -f ID` to finish it:

    $ t -f 31
    $ t
    9  - Buy more beer.
    30 - Clean the apartment.
    $

### Edit a Task

Sometimes you might want to change the wording of a task.  You can use
`t -e ID [new description]` to do that:

    $ t -e 30 Clean the entire apartment.
    $ t
    9  - Buy more beer.
    30 - Clean the entire apartment.
    $

Yes, nerds, you can use sed-style substitution strings:

    $ t -e 9 /more/a lot more/
    $ t
    9  - Buy a lot more beer.
    30 - Clean the entire apartment.
    $

### Delete the Task List if it's Empty

If you keep your task list in a visible place (like your desktop) you might
want it to be deleted if there are no tasks in it.  To do this automatically
you can use the `--delete-if-empty` option in your alias:

    alias t='python ~/path/to/t.py --task-dir ~/Desktop --list todo.txt --delete-if-empty'

Installing the batteries
-------------------------

I know I sad this task manager is for lazy people.. 
But we have to put some work before could sit back and watch our masterpiece.

### dmenu for your lazy ass task adding, finishing, editing or even deleteting

[dmenu](https://tools.suckless.org/dmenu/) is an universal GUI tool for selecting an item from a list.

Our tasks are happened to be a list of items so dmenu (but I think [fzf](https://github.com/junegunn/fzf) also could fine in the terminal) is perfect.
Just need to apply the [print input text patch](https://tools.suckless.org/dmenu/patches/printinputtext/) and ready to go... 

But lucky for you I just have one a [dmenu here](https://github.com/NeverI/dmenu) with this (and some more) patch.

Now you have to create a shortcut to `taskmenu`. In i3 something like this:

    bindsym $mod+t exec /path/to/taskmenu ~/tasks todo.txt
    
After that, simply press `$mod+t` write your task, press `enter` and your task is saved.ready to mark to fi... 

*nah... ready to forget about in your deep task list...*

### Here comes the dbus notification system to rescue you

I am using [dunst](https://dunst-project.org/) which is a lightweight keyboard driven notification daemon. 
But with a little hacking any notification system could be used. (xcfe4 is almost a drop in replace).

Just add this line to the `crontab -e`:

    */5 * * * * export DISPLAY=:0 && /path/to/taskdunstify /path/to/tasks todo.txt >/dev/null 2>&1

And you got notification from your overdue tasks at every five minutes.

I lied a little bit... You also have to edit the `taskdunstify`. You must update the path to you `t` and I also recommend to check the actions, timeout, urgency and everything else. This is a very flexible solution. Make it yours.

Using the batteries
-------------------

Let see how easy to manage our tasks

### Due dates

The hour has to be started with `@` and the dates with `=`

    $ t This work must be done before @13:30                   # for today 13:30
    $ t This work for =2020-12-15                              # this will create a due date with 00:00 
    $ t This work for a specified datetime =2020-12-08 @09:45
    
I think it is easy, but there is even [more](https://dateparser.readthedocs.io/en/latest/introduction.html)

    $ t This need to be done =tomorrow @14:00
    $ t This needed for =Friday                # this will be the next Friday
    $ t This =next_week                        # notice the '_' char, you have to use instead of a space
    $ t This is for =Dec-12
    
### Task orders

The tasks first ordered by ascending due date, then ascending created time.

But sometimes you did not want to assign a due date for the task, but wanted to be in a higher place. 

Just toss some `A` somewhere in the task :)

    $ t Its a task @13:40
    $ t Its an important task AA
    $ t Oh, no its a more important task AAA
    $ t Its must be done in the first place AAAAAAAAAAAAAAAAAAAA
    
    # so the order will be
    Its a task @13:40
    Its must be done in the first place AAAAAAAAAAAAAAAAAAAA
    Oh, no its a more important task AAA
    Its an important task AA
    
*maybe this will change to priority -> dueDate -> created*
    
### Taskmenu

Here comes the true lazyness 

#### Add a task

Press `your shortcut` write something and press the `enter` 

#### List your task 

Press `your shortcut`

#### Finish a task

Press `your shortcut` start to type or use the arrow keys, press `tab` when you find your task and press `enter`

#### Edit a task

Press `your shortcut` select your task with `tab` modify the text and press `enter`

#### Delete a task

Press `your shortcut` select your task with `tab` append ` DD` at the end and press `enter`

Tips and Tricks
---------------

`t` might be simple, but it can do a lot of interesting things.

### Count Your Tasks

Counting your tasks is simple using the `wc` program:

    $ t | wc -l
          2
    $

### Put Your Task Count in Your Bash Prompt

Want a count of your tasks right in your prompt?  Edit your `~/.bashrc` file:

    export PS1='[$(t | wc -l | sed -e"s/ *//")]'" $PS1"

Now you've got a prompt that looks something like this:

    [2] $ t -f 30
    [1] $ t Feed the cat.
    [2] $

### Multiple Lists

`t` is for people that want to *do* tasks, not organize them.  With that said,
sometimes it's useful to be able to have at least *one* level of organization.
To split up your tasks into different lists you can add a few more aliases:

    alias g='python ~/path/to/t.py --task-dir ~/tasks --list groceries'
    alias m='python ~/path/to/t.py --task-dir ~/tasks --list music-to-buy'
    alias w='python ~/path/to/t.py --task-dir ~/tasks --list wines-to-try'

### Distributed Bugtracking

Like the idea of distributed bug trackers like [BugsEverywhere][], but don't
want to use such a heavyweight system?  You can use `t` instead.

Add another alias to your `~/.bashrc` file:

    alias b='python ~/path/to/t.py --task-dir . --list bugs'

Now when you're in your project directory you can use `b` to manage the list of
bugs/tasks for that project.  Add the `bugs` file to version control and you're
all set.

Even people without `t` installed can view the bug list, because it's plain text.


Problems, Contributions, Etc
----------------------------

`t` was hacked together in a couple of nights to fit my needs.  If you use it
and find a bug, please let me know.

If you want to request a feature feel free, but remember that `t` is meant to
be simple.  If you need anything beyond the basics you might want to look at
[todo.txt][] or [TaskWarrior][] instead.  They're great tools with lots of
bells and whistles.
