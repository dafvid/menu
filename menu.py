#Python Menu class
#David Wahlund 2014

import os
import types

class MenuItem(object):
  def __init__(self,label):
    self.key = ''
    self.type = 'item'
    self.label = label
class SpaceItem(MenuItem):
  def __init__(self):
    super(SpaceItem,self).__init__('')
    self.type = 'other'
class TextItem(MenuItem):
  def __init__(self,label):
    super(TextItem,self).__init__(label)
    self.type = 'other'

class SubMenu(MenuItem):
  def __init__(self,label,title=None,text=''):
    super(SubMenu,self).__init__(label)
    self.itemsCount = 1
    self.items = []
    self.title = title if title is not None else label
    self.text = text
  
  def addSpaceItem(self):
    self.items.append(SpaceItem())
    
  def addItem(self,item,key=None):
    if not hasattr(item,'parent') or not item.parent: item.parent = self
    if item.type == 'other':
      self.items.append(item) 
    elif key:
      item.key = key
      self.items.append(item)
    else:
      item.key = str(self.itemsCount)
      self.items.append(item)
      self.itemsCount += 1
      
  def clearItems(self):
    self.itemsCount = 1
    self.items = []

class DynMenu(SubMenu):
  def __init__(self,label,init,*args,**kwargs):
    super(DynMenu,self).__init__(label)
    self.init = init
    self.args = args
    self.kwargs = kwargs

class SearchMenu(SubMenu):
  def __init__(self,label,search):
    super(SearchMenu,self).__init__(label)
    self.search = search

class Menu(object):
  def __init__(self,title,cls=True):
    self.rootMenu = SubMenu(title)
    self.rootMenu.parent = None
    self.cls = cls
    self.menu = self.rootMenu
  
  def addItem(self,item,key=None):
    self.rootMenu.addItem(item,key)
  def show(self):
    if self.cls:os.system('cls')
    if not isinstance(self.menu,SubMenu):
      raise Exception("self.menu not SubMenu")
      return
    print("### "+self.menu.title+" ###\n")
    
    if self.menu.text:
      print(self.menu.text+"\n")
    
    for item in self.menu.items:
      if type(item) is SpaceItem:
        print()
      elif type(item) is TextItem:
        print("%s" % (item.label))
      else:
        print("%s: [%s]" % (item.key,item.label))
    
    print()
    if self.menu.parent is not None:
      print("-: [Back]")
    if type(self.menu) is DynMenu:
      print("u: [Update]")
    
    print("0: [Home]")
    print("q: [Quit]")
  
  def read(self):
    ans = input('\n#?: ')
    
    item = None
    if ans == 'q':
      self.menu = None
      return
    elif ans == '0':
      self.menu = self.rootMenu
      return
    elif ans == '-':
      self.menu = self.menu.parent
      return
    elif ans=='u' and type(self.menu) is DynMenu:
      menu = self.menu
      menu.clearItems()
      menu.init(menu,*menu.args,**menu.kwargs)
      self.menu = menu
      return
    
    if type(self.menu) is SearchMenu:
      item = self.menu.search(self.menu,ans)
      if not item: 
        return
    else:
      if ans in [i.key for i in self.menu.items]:
        for i in self.menu.items:
          if i.key == ans:
            item = i
            break
      else:
        return
    
    if item != None:
      if type(item) is SubMenu or type(item) is SearchMenu:
        self.menu = item
      elif type(item) is DynMenu:
        item.clearItems()
        item.init(item,*item.args,**item.kwargs)
        self.menu = item
        return
      elif type(item) is not SpaceItem and type(item) is not TextItem:
        raise Error('Unknown menu class')
  
  def run(self):
    run = True
    while(run):
      self.show()
      self.read()
      if self.menu == None:
        run = False