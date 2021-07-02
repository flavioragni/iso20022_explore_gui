from tkinter import *
import xml.etree.ElementTree as ET

root = Tk()
root.title('ISO20022 Search')
#root.geometry("1000x600")
root.state('zoomed')

#Get ISO20022 xml
tree = ET.parse('20200914_ISO20022_2013_eRepository.iso20022')
xml_root = tree.getroot()

#Get parent list
term_list = sorted([term.attrib['name'] for term in xml_root.iter('topLevelDictionaryEntry') if term.attrib["{http://www.w3.org/2001/XMLSchema-instance}type"] == "iso20022:BusinessComponent" if term.attrib["registrationStatus"] == "Registered"])

info = StringVar()

#Update the listbox
def update(data):
	#Clear the listbox
	my_list.delete(0, END)

	#Add business components to listbox
	for item in data:
		my_list.insert(END, item)

#Update entry box with listbox clicked
def fillout(e):
	#Delete whatever is in the entry box
	my_entry.delete(0, END)

	# Add clicked list item to entry box
	my_entry.insert(0, my_list.get(ANCHOR))

#Create function to check entry vs listbox
def check(e):
	# grab what was typed
	typed = my_entry.get()

	if typed == '':
		data = term_list
	else:
		data = []
		for item in term_list:
			if typed.lower() in item.lower():
				data.append(item)

	#update our listbox with selected items
	update(data)				

    
def output_window(term):
    global info_label
    #Define element name
    elem_name = str(xml_root.find("./dataDictionary/topLevelDictionaryEntry[@name='%s']" % term).attrib["name"])
    #Define element definition
    elem_def = str(xml_root.find("./dataDictionary/topLevelDictionaryEntry[@name='%s']" % term).attrib["definition"])
    #Extract the tree (parents, grandparents, etc) of current element
    try:
        elem_parent = []
        parent_id = xml_root.find("./dataDictionary/topLevelDictionaryEntry[@name='%s']" % term).attrib['superType']
        for i in range(100):
            if xml_root.find("./dataDictionary/topLevelDictionaryEntry[@{http://www.omg.org/XMI}id='%s']" % parent_id).attrib['{http://www.w3.org/2001/XMLSchema-instance}type'] == "iso20022:BusinessComponent":
                #If so print parent name
                elem_parent.append(str(xml_root.find("./dataDictionary/topLevelDictionaryEntry[@{http://www.omg.org/XMI}id='%s']" % parent_id).attrib['name']))
                print(elem_parent)
                try:
                    parent_id = str(xml_root.find("./dataDictionary/topLevelDictionaryEntry[@{http://www.omg.org/XMI}id='%s']" % parent_id).attrib['superType'])
                except:
                    break
    except:
        #Else print None
        elem_parent = 'None' 
    #Reverse the list to show entire tree
    if type(elem_parent) == list:
        elem_parent = '> '.join(list(reversed(elem_parent)))    
        
    #Print element child
    try:
        elem_child = []
        for child in xml_root.find("./dataDictionary/topLevelDictionaryEntry[@name='%s']" % term).attrib['subType'].split():
            if str(xml_root.find("./dataDictionary/topLevelDictionaryEntry[@{http://www.omg.org/XMI}id='%s']" % child).attrib["{http://www.w3.org/2001/XMLSchema-instance}type"]) == "iso20022:BusinessComponent":
                elem_child.append(str(xml_root.find("./dataDictionary/topLevelDictionaryEntry[@{http://www.omg.org/XMI}id='%s']" % child).attrib['name']))
    except:
        elem_child = 'None'
    #If there are more than 1 child join the list
    if type(elem_child) == list:
        elem_child = '; '.join(elem_child)
    #Prepare element info
    info_label = Message(root, text = "Name: " + elem_name + 
                 "\nDefinition: " + elem_def +
                 "\nParent: " + elem_parent +
                 "\nChild: " + elem_child,
                 font=("Helvetica", 14), justify=CENTER, width = 1000)
    info_label.pack(pady=20)
    #Disable ok button
    ok_btt['state'] = DISABLED
    my_list['state'] = DISABLED
    my_entry['state'] = DISABLED

def del_label():
    #Enable back ok button
    ok_btt['state'] = NORMAL
    my_list['state'] = NORMAL
    my_entry['state'] = NORMAL
    #Remove term info
    info_label.pack_forget()
    #Remove what's typed in entry box
    my_entry.delete(0, 'end')
    #Update list again to remove search
    update(term_list)  
    
# Create a label
my_label = Label(root, text="Start Typing ISO20022 Business Component...",
	font=("Helvetica", 14), fg="grey")

my_label.pack(pady=20)

#Create frame
my_frame = Frame(root)

# Create an entry box
my_entry = Entry(my_frame, font=("Helvetica", 16), width=31)
my_entry.pack(pady = 15)

#Add scrollbar
scrollbar = Scrollbar(my_frame, orient=VERTICAL)

# Create a listbox with list of business components
my_list = Listbox(my_frame, width=60, yscrollcommand=scrollbar.set)
#Configure scrollbar
scrollbar.config(command=my_list.yview)
scrollbar.pack(side=RIGHT, fill=Y)
my_frame.pack()
my_list.pack(fill = 'y')

# Add business components to the list
update(term_list)

# Create a binding on the listbox
my_list.bind("<<ListboxSelect>>", fillout)

# Create a binding on the entry box
my_entry.bind("<KeyRelease>", check)

#Insert ok button. When pressed, get entry
ok_btt = Button(root, text="Ok", command=lambda: output_window(my_entry.get()))
ok_btt.pack(ipadx = 59, pady = 10)

#Insert delete button
del_btt = Button(root, text='Delete', command=del_label)
del_btt.pack(ipadx = 50)

root.mainloop()