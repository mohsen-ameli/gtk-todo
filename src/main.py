import gi
import json

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

class InputWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title="Todo App")
        self.set_size_request(500, 200)
        self.set_border_width(10)

        self.NAME_COL = 1
        self.DUE_COL = 2
        self.FINISHED_COL = 3

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.add(vbox)

        self.load_db()

        # View todo list
        self.todo_list = Gtk.ListStore(bool, str, str, bool)
        for todo in self.todo_db:
            self.todo_list.append([False, todo["name"], todo["due"], todo["finished"]])

        todo_tree = Gtk.TreeView(model=self.todo_list)
        
        # Delete column
        renderer_rm = Gtk.CellRendererToggle()
        renderer_rm.connect("toggled", self.del_todo)
        column_icon = Gtk.TreeViewColumn("X", renderer_rm, active=0)
        todo_tree.append_column(column_icon)

        # Name
        renderer_text = Gtk.CellRendererText()
        renderer_text.set_property("editable", True)
        renderer_text.connect("edited", self.todo_change_name)
        column = Gtk.TreeViewColumn("Name", renderer_text, text=self.NAME_COL)
        column.set_sort_column_id(1)
        todo_tree.append_column(column)

        # Due date
        renderer_text = Gtk.CellRendererText()
        renderer_text.set_property("editable", True)
        renderer_text.connect("edited", self.todo_change_due)
        column = Gtk.TreeViewColumn("Due Date", renderer_text, text=self.DUE_COL)
        column.set_sort_column_id(2)
        todo_tree.append_column(column)
        
        # Finished column
        renderer_toggle = Gtk.CellRendererToggle()
        renderer_toggle.connect("toggled", self.on_cell_toggled)
        column_toggle = Gtk.TreeViewColumn("Finished", renderer_toggle, active=self.FINISHED_COL)
        column_toggle.set_sort_column_id(self.FINISHED_COL)
        todo_tree.append_column(column_toggle)

        vbox.pack_start(todo_tree, True, True, 0)

        # Add a new todo
        hbox0 = Gtk.Box(spacing=4)
        vbox.pack_start(hbox0, True, True, 0)
        name = Gtk.Label()
        due = Gtk.Label()
        name.set_label("Name")
        due.set_label("Due Date")
        hbox0.pack_start(name, True, True, 0)
        hbox0.pack_start(due, True, True, 0)
        vbox.pack_start(hbox0, True, True, 0)

        hbox1 = Gtk.Box(spacing=4)
        vbox.pack_start(hbox1, True, True, 0)

        self.name = Gtk.Entry()
        self.due = Gtk.Entry()
        self.name.set_size_request(100, -1)
        self.due.set_size_request(100, -1)
        hbox1.pack_start(self.name, True, True, 0)
        hbox1.pack_start(self.due, True, True, 0)

        self.add = Gtk.Button()
        self.add.set_size_request(100, -1)
        self.add.set_label("Add")
        self.add.connect("clicked", self.add_todo)
        vbox.pack_start(self.add, True, True, 0)
        
    def add_todo(self, widget):
        new_todo = {
            "name": self.name.get_text(),
            "due": self.due.get_text(),
            "finished": False
        }
        with open("todo.json", "w") as f:
            self.todo_db.insert(0, new_todo)
            self.todo_list.insert(0, [False, new_todo["name"], new_todo["due"], new_todo["finished"]])
            f.write(json.dumps(self.todo_db))
        
        f.close()
    
    def del_todo(self, widget, path):
        iter = self.todo_list.get_iter(Gtk.TreePath(path))
        self.todo_db.pop(int(path))
        with open("todo.json", "w") as f:
            f.write(json.dumps(self.todo_db))
        self.todo_list.remove(iter)

    def on_cell_toggled(self, widget, path):
        self.todo_list[path][self.FINISHED_COL] = not self.todo_list[path][self.FINISHED_COL]

    def load_db(self):
        with open("todo.json", "r") as f:
            self.todo_db = json.loads(''.join(f.readlines()))
        f.close()

    def todo_change_name(self, cell, path, new_text):
        self.todo_list[path][self.NAME_COL] = new_text
        self.todo_db[int(path)]["name"] = new_text
        with open("todo.json", "w") as f:
            f.write(json.dumps(self.todo_db))
    
    def todo_change_due(self, cell, path, new_text):
        self.todo_list[path][self.DUE_COL] = new_text
        self.todo_db[int(path)]["due"] = new_text
        with open("todo.json", "w") as f:
            f.write(json.dumps(self.todo_db))

win = InputWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
