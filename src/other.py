import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class TreeViewExample(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="TreeView Example")
        self.set_border_width(10)
        self.set_default_size(400, 200)

        # Create a ListStore with two columns: one for the item and one for the button text
        self.liststore = Gtk.ListStore(str, str)
        self.liststore.append(["Item 1", "X"])
        self.liststore.append(["Item 2", "X"])
        self.liststore.append(["Item 3", "X"])

        treeview = Gtk.TreeView(model=self.liststore)

        # Add the item column
        renderer_text = Gtk.CellRendererText()
        column_text = Gtk.TreeViewColumn("Items", renderer_text, text=0)
        treeview.append_column(column_text)

        # Add the button column
        renderer_button = Gtk.CellRendererText()
        renderer_button.set_property("foreground", "red")
        renderer_button.set_property("editable", True)
        renderer_button.connect("edited", self.on_button_clicked)
        column_button = Gtk.TreeViewColumn("Remove", renderer_button, text=1)
        treeview.append_column(column_button)

        self.add(treeview)

    def on_button_clicked(self, cell, path, new_text):
        # Remove the corresponding row
        iter = self.liststore.get_iter(Gtk.TreePath(path))
        self.liststore.remove(iter)

win = TreeViewExample()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
