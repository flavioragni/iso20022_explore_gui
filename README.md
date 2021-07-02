ISO20022 EXPLORATION GUI 

GUI made with Python and Tkinter to explore ISO20022 Business Model repository.
The GUI has an interactive autofill search bar that helps the user in the exploration
of the ISO20022 repository.
The GUI lists all ISO20022 Business Components (no messages or attributes), and for each selected component displays name, definition, list of parents (all the relationship tree before that component) and list of children (if present).
To use the GUI, start typing the name of a component in the search bar. The GUI will automatically suggest the list of all business components having a similar name to those typed into the search bar. To see the details press on thebutton "OK". To search for a different term, press the "Delete" button and start over.

PREREQUISITES:
To generate the list of Business Component, you need to download the ISO20022 e-repository in the same folder as the python script. You can download the e-repository at the ISO20022 website (https://www.iso20022.org/iso20022-repository/e-repository).

FR - 20210702
