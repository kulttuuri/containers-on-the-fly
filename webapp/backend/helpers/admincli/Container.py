from helpers.tables.Container import *

def CLIcontainers():
  breakLoop = False
  while breakLoop == False:
    print(f"\nManaging containers  ({len(getContainers())} containers in database)")
    print("What do you want to do?")
    print("1) List containers")
    print("2) Add new container")
    print("3) Remove container")
    print("4) Edit container")
    print("5) Go back")
    selection = input()

    if (selection == "1"): CLIcontainersList()
    elif (selection == "2"): CLIaddContainer()
    elif (selection == "3"): CLIremoveContainer()
    elif (selection == "4"): CLIeditContainer()
    elif (selection == "5"): breakLoop = True

def CLIcontainersList():
  breakLoop = False
  while breakLoop == False:
    print("\nContainer Listing")
    print("1) List all containers")
    print("2) List container by search")
    print("3) Go back")
    selection = input()

    if selection == "1": CLIPrintAllContainers()
    elif selection == "2": CLIPrintContainerBySearch()
    elif selection == "3": breakLoop = True

def CLIPrintAllContainers():
  containers = getContainers()
  public = "Not public"
  for container in containers:
    if container.public:
      public = "Public"
    else: public = "Not public"
    print("id:", container.containerId, "-", public, "- name:", container.name, "- description:", container.description, "- image:", container.imageName)
    print("created at:", container.createdAt, "- updated at:", container.updatedAt)

def CLIPrintContainerBySearch():
  print("\nWhat is the id or name of the container you are looking for? (name is case-sensitive)")
  filter = input()
  containers = getContainers(filter)
  if containers != None:
    for container in containers:
      if container.public:
        public = "Public"
      else: public = "Not public"
      print("id:", container.containerId, "-", public, "- name:", container.name, "- description:", container.description, "- image:", container.imageName)
      print("created at:", container.createdAt, "- updated at:", container.updatedAt)
  else: print("No match found for:", filter)

def CLIaddContainer():
  breakLoop = False
  while breakLoop == False:
    print("\nContainer Adding")
    print("1) Add container(s)")
    print("2) Go back")
    selection = input()
    
    if (selection == "1"): CLIAddContainers()
    elif (selection == "2"): breakLoop = True

def CLIAddContainers():
  errors = 0
  print("\nList all the container names you want to add separated by commas: (Container1, Container2, Container3, etc...)")
  containersToAdd = input().split(", ")
  for container in containersToAdd:
    print('\nIs "' + container + '" public or not? (True / False)')
    public = input()
    if public.capitalize() == "True":
      public = True
    elif public.capitalize() == "False":
      public = False
    else:
      print("\nNot a valid value for publicity, only accepted values are: True or False")
      errors += 1
      continue
    print('\nWhat description will "' + container + '" have?')
    description = input()
    print('\nWhat image will "' + container + '" be running on?')
    imageName = input()
    # might need a rework, I just did these modifications to the imageName based on the example in the database
    imageName = imageName.lower().replace(".","")
    imageName = imageName.replace(" ","")
    result = addContainer(container, public, description, imageName)
    if result == None: 
      print("Couldn't add:", container, "to containers, this name is already in use.")
      errors += 1
  print(len(containersToAdd)-errors, "containers were added to the database.") #Count of items that arent None

def CLIremoveContainer():
  breakLoop = False
  while breakLoop == False:
    print("\nContainer Removal")
    print("1) Remove container")
    print("2) Go back")
    selection = input()
    
    if (selection == "1"):
      print("\nWhat is the id or name of the container you want to delete? (name is case-sensitive)")
      filter = input()
      container = getContainers(filter)
      if container != None:
        container = container[0]
        removeContainer(container)
        print("Container successfully removed.")
      else: print("No match found for:", filter)
    elif (selection == "2"): breakLoop = True

def CLIeditContainer():
  breakLoop = False
  while breakLoop == False:
    print("\nContainer Editing")
    print("1) Edit container")
    print("2) Go back")
    selection = input()

    if (selection == "1"):
      print("\nWhat is the id or name of the container you want to edit? (name is case-sensitive)")
      filter = input()
      container = getContainers(filter)
      if container != None:
        container = container[0]
        CLIEditContainers(container)
      else: print("No match found for:", filter)
    elif (selection == "2"): breakLoop = True

def CLIEditContainers(container):
  breakLoop = False
  while breakLoop == False:
    print("\nWhich part of", container.name, "do you want to edit?")
    print("1) Edit name")
    print("2) Edit publicity")
    print("3) Edit description")
    print("4) Edit image name")
    print("5) Edit all of the above")
    print("6) Go back")
    selection = input()
    if (selection == "1"):
        print("\nWhat do you want to edit " + container.name + "'s name to?")
        new_name = input()
        editContainer(container, new_name=new_name)
        print("Container successfully edited.")
    elif (selection == "2"):
        print("\nWhat do you want to edit " + container.name + "'s publicity to? (True/False)")
        new_public = input()
        if new_public.capitalize() == "True":
          new_public = True
        elif new_public.capitalize() == "False":
          new_public = False
        else:
          print("\nNot a valid value for publicity, only accepted values are: True or False") 
          continue
        editContainer(container, new_public=new_public)
        print("Container successfully edited.")
    if (selection == "3"):
        print("\nWhat do you want to edit " + container.name + "'s description to?")
        new_description = input()
        editContainer(container, new_description=new_description)
        print("Container successfully edited.")
    if (selection == "4"):
        print("\nWhat do you want to edit " + container.name + "'s image name to?")
        new_image_name = input()
        # might need a rework, I just did these modifications to the imageName based on the example in the database
        new_image_name = new_image_name.lower().replace(".","")
        new_image_name = new_image_name.replace(" ","")
        editContainer(container, new_image_name=new_image_name)
        print("Container successfully edited.")
    elif (selection == "5"):
        print("\nWhat do you want to edit " + container.name + "'s name to?")
        new_name = input()
        print("\nWhat do you want to edit " + container.name + "'s publicity to? (True/False)")
        new_public = input()
        if new_public.capitalize() == "True":
          new_public = True
        elif new_public.capitalize() == "False":
          new_public = False
        else:
          print("\nNot a valid value for publicity, only accepted values are: True or False") 
          continue
        print("\nWhat do you want to edit " + container.name + "'s description to?")
        new_description = input()
        print("\nWhat do you want to edit " + container.name + "'s image name to?")
        new_image_name = input()
        # might need a rework, I just did these modifications to the imageName based on the example in the database
        new_image_name = new_image_name.lower().replace(".","")
        new_image_name = new_image_name.replace(" ","")
        editContainer(container, new_name, new_public, new_description, new_image_name)
        print("Container successfully edited.")
    elif (selection == "6"): breakLoop = True
