#Python Menu class
#David Wahlund 2015

##TODO
# -reserved nav keys (eg. p,n,u,-,0)

import os
import types

class MenuItem(object):
    def __init__(self,label,key='',):
        self.label = label
        
class NoNavItem(MenuItem): #Item outside of navigation
    pass
class SpaceItem(NoNavItem):
    def __init__(self):
        super(SpaceItem,self).__init__('')
class TextItem(NoNavItem):
    def __init__(self,label):
        super(TextItem,self).__init__(label)

class NavItem(MenuItem):
    def __init__(self,label):
        super(NavItem,self).__init__(label)
        self.key = ''
        # self.label = ''
        
class ActionItem(NavItem):
    def __init__(self,label,actionFunc,*args,**kwargs):
        super(ActionItem,self).__init__(label)
        self.msg=''
        self.actionFunc=actionFunc
        self.args=args
        self.kwargs=kwargs
    
    def action(self):
        self.actionFunc(self,*self.args,**self.kwargs)
    
    def hasMsg(self):
        return self.msg != ''
  
    def getMsg(self):
        msg=self.msg
        self.msg=''
        return msg

class SubMenu(NavItem):
    def __init__(self,label,title='',text=''):
        super(SubMenu,self).__init__(label)
        self.itemsCount = 1
        self.items = []
        self.title = title if title else label
        self.text = text
        self.msg = ''

    # def addText(self,text,spaceAbove=False):
        # if spaceAbove:
            # self.text += '\n'
        # self.text += "%s\n"%(str(text))
    
    def addSpaceItem(self):
        self.items.append(SpaceItem())
    def addTextItem(self,text,spaceAbove=False):
        if spaceAbove: # It's common to add space above titles and labels
            self.addSpaceItem()
        self.items.append(TextItem(text))
    
    def addItem(self,item,key=''):
        if not hasattr(item,'parent') or not item.parent: 
            item.parent = self

        if isinstance(item,NoNavItem):
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

    def hasMsg(self):
        return self.msg != ''

    def getMsg(self):
        msg=self.msg
        self.msg=''
        return msg

    def navItems(self):
        return [i for i in self.items if isinstance(i,NavItem)]
        
class DynMenu(SubMenu):
    def __init__(self,label,initFunc,*args,**kwargs):
        super(DynMenu,self).__init__(label)
        self.initFunc = initFunc
        self.updatable = False
        self.args = args
        self.kwargs = kwargs

    def initMenu(self):
        self.initFunc(self,*self.args,**self.kwargs)

    def reset(self):
        self.clearItems()
        self.text = ''
        self.initMenu()

class SearchMenu(DynMenu):
    def __init__(self,label,searchFunc,*args,**kwargs):
        super(SearchMenu,self).__init__(label,None,*args,**kwargs)

        self.searchFunc = searchFunc
    
    def initMenu(self):
        pass
    
    def search(self,ans):
        return self.searchFunc(self,ans,*self.args,**self.kwargs)
    
class PageMenu(DynMenu):
    def __init__(self,label,itemInit,idx=0,pages=[],titleFunc=None,*args,**kwargs):
        super(PageMenu,self).__init__(label,None,*args,**kwargs)
        self.pages = pages
        self.idx = idx
        self.itemInit = itemInit
        self.length = len(pages)
        self.titleFunc = titleFunc

    #override DynMenu init
    def initMenu(self):
        #call init for listitem
        page = self.pages[self.idx]
        if self.titleFunc:
            self.title = self.titleFunc(page)
        else:
            self.title = str(page)
        self.itemInit(self,page,*self.args,**self.kwargs)
    
class ListMenu(PageMenu):
    def __init__(self,label,itemInit,size,list=[],labelFunc=None,titleFunc=None,*args,**kwargs):
        pages = []
        for i in range(0, len(list), size):
          pages.append(list[i:i+size])
        super(ListMenu,self).__init__(label,None,0,pages,*args,**kwargs)
        self.list = list
        self.size = size
        self.listLength = len(list)
        self.itemInit = itemInit
        self.labelFunc = labelFunc
        self.titleFunc = titleFunc

    def pageLen(self):
        return len(self.pages[self.idx])
        
    def initMenu(self):
        page = self.pages[self.idx]  # list of items
        i = 0
        for item in page:
            lbl = ''
            if self.labelFunc:
                lbl = self.labelFunc(item)
            else:
                lbl = str(item)
            idx = self.idx * self.size + i
            item = LinkMenu(lbl,self.itemInit,idx,self.list)
            if self.titleFunc:
                item.title = titleFunc(i)
            else:
                item.title = str(i)
            self.addItem(item)
            i += 1
        
class LinkMenu(PageMenu):
    def __init__(self,label,itemInit,idx,list=[],titleFunc=None,*args,**kwargs):
        super(LinkMenu,self).__init__(label,itemInit,idx,list,titleFunc,*args,**kwargs)
        self.itemInit = itemInit
        
    
class Menu(object):
    def __init__(self,title,cls=True):
        self.rootMenu = SubMenu(title)
        self.rootMenu.parent = None
        self.cls = cls
        self.menu = self.rootMenu
  
    def addItem(self,item,key=None):
        self.rootMenu.addItem(item,key)
  
    def reset(self):
        if isinstance(self.menu,DynMenu):
            self.menu.reset()
  
    def show(self):
        if self.cls:
            os.system('cls')
        if not isinstance(self.menu,SubMenu):
            raise Exception("self.menu not SubMenu")

        if isinstance(self.menu,ListMenu):
            firstidx = self.menu.idx * self.menu.size
            first = firstidx + 1
            last = firstidx+self.menu.pageLen()
            print("### %s [%s/%s] [%s-%s/%s] ###"%(self.menu.title,self.menu.idx + 1,self.menu.length,first,last,self.menu.listLength))
        elif isinstance(self.menu,PageMenu):
            print("### %s [%s/%s] ###"%(self.menu.title,self.menu.idx+1,self.menu.length))
        else:
            print("### %s ###"%(self.menu.title))

        if self.menu.hasMsg():
            print("{%s}"%(self.menu.getMsg().upper()))

        print() #newline after title

        if self.menu.text:
            print("ALL YOUR TEXT ARE BELONG TO US")  # everything is a textitem now
        itemCount = len(self.menu.navItems())
        keyOffset = 1
        if itemCount >= 100:
            keyOffset = 3
        elif itemCount >= 10:
            keyOffset = 2
        
        formatStr = "{:%sd}: [{}]"%(keyOffset)
        
        for item in self.menu.items:
            if type(item) is SpaceItem:
                print()
            elif type(item) is TextItem:
                print("%s" % (item.label))
            else:
                if item.key.isdigit():
                    print(formatStr.format(int(item.key),item.label))
                    # print("%s%s: [%s]" % (' '*(keyOffset - len(item.key) - 1),item.key,item.label))
                else:
                    print("%s: [%s]" % (item.key,item.label))

        print()
        if isinstance(self.menu,PageMenu):
            print("p: [Previous]")
            print("n: [Next]")
            print("o: [Go to page]\n")
        if isinstance(self.menu,DynMenu) and self.menu.updatable:
            print("u: [Update]\n")
            
        if self.menu.parent is not None:
            print("-: [Back]")
            
        print("0: [Home]")
        print("q: [Quit]")
  
    def read(self):
        ans = input('\n#?: ')
        print()
        print() #create space if cls = False

        #Navigation
        if ans == 'q':
            self.menu = None
            return
        elif ans == '0':
            self.menu = self.rootMenu
            return
        elif ans == '-':
            self.menu = self.menu.parent
            self.reset()
            return
        elif ans=='u' and isinstance(self.menu,DynMenu) and self.menu.updatable:
            self.reset()
            return
        elif isinstance(self.menu,PageMenu):
            if ans=='p':
                if self.menu.idx > 0:
                    self.menu.idx -= 1
                self.reset()
                return
            elif ans=='n':
                if self.menu.idx < len(self.menu.pages) - 1:
                    self.menu.idx += 1
                self.reset()
                return
            elif ans=='o':
                pi = input('#num?: ')
                if pi.isdigit():
                    pi = int(pi)
                    if pi > 0 and pi <= len(self.menu.pages):
                        self.menu.idx = pi - 1
                self.reset()
                return
          
        #Selection
        item = None

        if type(self.menu) is SearchMenu:
            item = self.menu.search(ans)
            if not item: #return None if search failed
                return
        else:
            navItems = self.menu.navItems()
            if ans in [i.key for i in navItems]:
                for i in navItems:
                    if i.key == ans:
                        item = i
                        break
            else:
                return

        if type(item) is ActionItem:
            item.action()
            self.reset()
            self.menu.msg=item.getMsg()      

        #Maybe change current menu
        if item != None:
            if type(item) is SubMenu:
                self.menu = item
            elif isinstance(item,DynMenu):
                self.menu = item
                self.reset()
                return
        
    def run(self):
        run = True
        while(run):
            self.show()
            self.read()
            if self.menu == None:
                run = False