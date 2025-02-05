### what is this?

This is just a pyqt6 frontend for sftp so my family can get stuff onto my backup servers for them without having to learn how to use sftp from the commandline, or a robust app like Filezilla, which is too complex for their use case.

Also using as practice catching about subtle races, and pythonic approaches to handling them like decorators and EAFP.
And writing a pyqt6 gui

Why pyqt6? because as I understand it pyqt's event loop is single threaded
the project needs a fair amount of routines are blocking
the gui will freeze - excuse to practice


#### todos (and todonts)
- log to files (in addition to ?) console
- security things but dont say them out loud (just kidding)
- handling for bad keys/pass, etc
- dispatch levels need to reflect new approach with `logging`
- threads :( |? :) 
  - qthread?
- ensure decorator usage stays (?) idiomatic
- speaking of decorator, the check for `"upload" in fn.__name__` within it is pretty brittle
- load_key need not belong to client class maybe idk? 
- document better. client is looking sparse aside from todos. very least be better w/ notes in "devlog" (lol)
- better/more sensible logging
- get logging out of decorators
- [X] don't use the markdown checkboxes. no way I'm coming back to x that in


