from menu import *

menu = Menu('Example menu')
submenu = SubMenu('SubMenuLabel','SubMenuTitle','This is the text of the menu')
submenu.addItem(SubMenu('2ndLevelSubMenu','This is a second level sub menu'))
submenu.text = "You can change the text of the menu afterwards"
menu.addItem(submenu)
submenu.addItem(TextItem('Bascially a text placeholder inside menus'))
submenu.addItem(SpaceItem())
submenu.addItem(TextItem('Above this TextItem is a Spaceitem'))

def dynMenuFunction(menu,count,kwarg):
  menu.text = "The Count was %s and kwarg was '%s'\n" % (count,kwarg)
  menu.text += "Some appended text"
  menu.parent = menu #mess up the menus parent, we can't get back!
  
submenu.addItem(DynMenu('ADynMenu',dynMenuFunction,10,kwarg='ten'))

def searchMenuFunction(menu,searchString):
  menu.text = "You searched for '%s'" % (searchString)
  if searchString == 'correct':
    nextmenu = SubMenu('','Correct Menu',"This is where you end up if you type 'correct'")
    nextmenu.parent = menu
    return nextmenu
  
menu.addItem(SearchMenu('SearchMenu',searchMenuFunction))

menu.run()