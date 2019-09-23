from menu import *

example_menu = Menu('Example menu')
submenu = SubMenu('SubMenuLabel', 'SubMenuTitle')
submenu.add_item(SubMenu('2ndLevelSubMenu', 'This is a second level sub menu'))
example_menu.add_item(submenu)
submenu.add_item(TextItem('Bascially a text placeholder inside menus'))
submenu.add_item(SpaceItem())
submenu.add_item(TextItem('Above this TextItem is a Spaceitem'))


def an_action(source_menu, arg):
    print("This is a test action! Your args was {}".format(arg))
    source_menu.msg = 'This is a response message. Shown once then deleted.'


example_menu.add_item(ActionItem('AnActionItem', an_action, 'an_argument'))


def dyn_menu_function(menu, count, kwarg):
    menu.add_text_item("The Count was %s and kwarg was '%s'\n" % (count, kwarg))
    menu.add_text_item("Some appended text")
    menu.msg = 'Important message to all!'
    menu.parent = menu  # mess up the menus parent, we can't get back!


example_menu.add_item(DynMenu('ADynMenu', dyn_menu_function, 10, kwarg='ten'))


def search_menu_function(menu, search_string):
    menu.add_text_item("You searched for '%s'" % search_string)
    if search_string == 'correct':
        nextmenu = SubMenu('', 'Correct Menu', "This is where you end up if you type 'correct'")
        nextmenu.parent = menu
        return nextmenu


example_menu.add_item(SearchMenu('SearchMenu', search_menu_function))

page_data = [
    {
        'title': 'The first title',
        'content': 'The first content'
     },
{
        'title': 'The second title',
        'content': 'The second content'
     }
]


def make_title(i):
    return i['title']


def make_page(m, p):
    m.add_text_item(p['content'])


example_menu.add_item(PageMenu('APageMenu', make_page, pages=page_data, title_func=make_title))


def make_label(i):
    return "Item #{}".format(i['idx'])


list_data = list()

for i in range(30):
    d = {
        'idx': i+1,
        'title': "Title for item #{}".format(i+1),
        'content': "Something about page #{}".format(i+1),
    }
    list_data.append(d)


example_menu.add_item(ListMenu('AListMenu', make_page, list_data, label_func=make_label, title_func=make_title))

example_menu.run()
