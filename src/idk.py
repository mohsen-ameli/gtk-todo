import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class TreeViewExample(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="TreeView Example")
        self.set_border_width(10)
        self.set_default_size(400, 200)

        # Create a ListStore with two columns: one for the item and one for the toggle button
        self.liststore = Gtk.ListStore(str, bool)
        self.liststore.append(["Item 1", False])
        self.liststore.append(["Item 2", False])
        self.liststore.append(["Item 3", False])

        treeview = Gtk.TreeView(model=self.liststore)

        # Add the item column
        renderer_text = Gtk.CellRendererText()
        column_text = Gtk.TreeViewColumn("Items", renderer_text, text=0)
        treeview.append_column(column_text)

        # Add the toggle button column
        renderer_toggle = Gtk.CellRendererToggle()
        renderer_toggle.connect("toggled", self.on_button_toggled)
        column_toggle = Gtk.TreeViewColumn("Remove", renderer_toggle, active=1)
        treeview.append_column(column_toggle)

        self.add(treeview)

    def on_button_toggled(self, widget, path):
        # Convert the path to a TreeIter
        iter = self.liststore.get_iter(Gtk.TreePath(path))
        # Remove the corresponding row
        self.liststore.remove(iter)

win = TreeViewExample()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
