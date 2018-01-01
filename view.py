from tkinter import *
import tkinter.tix as tk
from graph import *
from alhorythm import *
import random as rnd

global CURRENT_NODE_NUMBER
global CHANNEL_WEIGHTS


class Node:
    def __init__(self, canvas, name, x, y):
        self.x = x
        self.y = y
        self.radius = 20
        self.color = 'powderblue'
        self.outline = 'black'
        self.active_color = 'greenyellow'
        self.disabled_color = 'grey'
        self.width = 1
        self.canvas = canvas

        self.selected = False
        self.disabled = False
        self.related_channels = []
        self.name = name
        queue = []

        self.draw()
        self.canvas.tag_bind(self.view, '<B1-Motion>', self.move)
        self.canvas.tag_bind(self.view, '<Button-1>', self.select)
        self.canvas.tag_bind(self.view, '<Double-Button-1>', self.disable)

    def draw(self):
        x1 = self.x - self.radius
        x2 = self.x + self.radius
        y1 = self.y - self.radius
        y2 = self.y + self.radius
        self.view = self.canvas.create_oval(x1, y1, x2, y2, tag='node', outline=self.outline, width=self.width,
                                            fill=self.color)
        self.text = self.canvas.create_text(self.x, self.y - 10, font=("Arial", 12), text=str(self.name))

    def move(self, event):
        self.canvas.move(self.view, event.x - self.x, event.y - self.y)
        self.canvas.move(self.text, event.x - self.x, event.y - self.y)
        for element in self.related_channels:
            if (element.x1, element.y1) == (self.x, self.y):
                element.canvas.coords(element.view, event.x, event.y, element.x2, element.y2)
                element.canvas.coords(element.text, (element.x2 + event.x) // 2, (element.y2 + event.y) // 2)
                element.x1 = event.x
                element.y1 = event.y
            elif (element.x2, element.y2) == (self.x, self.y):
                element.canvas.coords(element.view, element.x1, element.y1, event.x, event.y)
                element.canvas.coords(element.text, (element.x1 + event.x) // 2, (element.y1 + event.y) // 2)
                element.x2 = event.x
                element.y2 = event.y
        self.x = event.x
        self.y = event.y

    def select(self, event):
        if self.selected and not self.disabled:
            self.canvas.itemconfig(self.view, fill=self.color)
            self.selected = False
        elif not self.selected and not self.disabled:
            self.canvas.itemconfig(self.view, fill=self.active_color)
            self.selected = True

    def disable(self, event):
        if self.disabled:
            self.canvas.itemconfig(self.view, fill=self.color)
            self.disabled = False
        else:
            self.canvas.itemconfig(self.view, fill=self.disabled_color)
            self.disabled = True

    def delete(self):
        self.canvas.delete(self.view)
        self.canvas.delete(self.text)


class Channel:
    def __init__(self, canvas, nodes, channel_type, positions, weight):
        self.node1, self.node2 = nodes
        self.x1, self.y1, self.x2, self.y2 = positions
        self.canvas = canvas
        self.duplex_color = 'orange'
        self.half_duplex_color = 'purple'
        self.active_color = 'limegreen'
        self.disabled_color = 'dimgrey'
        self.path_color = 'crimson'
        self.path_width = 5
        self.width = 3
        self.active_width = 5
        self.current_color = "grey"

        self.selected = False
        self.disabled = False
        self.type = channel_type
        self.weight = weight
        self.error_prob = 0.1

        self.draw()
        self.canvas.tag_bind(self.view, '<Button-1>', self.select)
        self.canvas.tag_bind(self.view, '<Double-Button-1>', self.disable)

    def draw(self):
        if self.type == 'duplex':
            self.current_color = self.duplex_color
        elif self.type == 'half-duplex':
            self.current_color = self.half_duplex_color
        self.view = self.canvas.create_line(self.x1, self.y1, self.x2, self.y2,
                                            fill=self.current_color, activefill=self.active_color,
                                            width=self.width, activewidth=self.active_width)
        self.text = self.canvas.create_text(int((self.x1 + self.x2) / 2), int((self.y1 + self.y2) / 2 - 14),
                                            font=("Arial", 10), text=str(self.weight))

    def select(self, event):
        if self.selected and not self.disabled:
            self.canvas.itemconfig(self.view, fill=self.current_color)
            self.selected = False
        elif not self.selected and not self.disabled:
            self.canvas.itemconfig(self.view, fill=self.active_color)
            self.selected = True

    def disable(self, event):
        if self.disabled:
            self.canvas.itemconfig(self.view, fill=self.current_color)
            self.disabled = False


        else:
            self.canvas.itemconfig(self.view, fill=self.disabled_color)
            self.disabled = True

    def delete(self):
        self.canvas.delete(self.view)
        self.canvas.delete(self.text)


class Package:
    def __init__(self, size, number):
        self.number = number
        self.size = size
        self.header = 24


class Main:
    def __init__(self):

        self.node_list = []
        self.channel_list = []

        self.root = Tk()
        self.root["bg"] = "white"
        self.root.title("Course Work")
        self.root.geometry("1000x600")

        self.canvas = Canvas(width=800, height=600, bg='lightgrey')
        self.canvas.pack(side=RIGHT)

        self.add_node_button = Button(self.root, width=20, bg="mediumturquoise")
        self.add_node_button["text"] = "Add Node"
        self.add_node_button.place(x=0, y=0)
        self.add_node_button.bind('<Button-1>', self.add_node_event)

        self.add_channel_button = Button(self.root, width=20, bg="mediumturquoise")
        self.add_channel_button["text"] = "Add Channel"
        self.add_channel_button.place(x=0, y=30)
        self.add_channel_button.bind('<Button-1>', self.add_channel)

        self.delete_node_button = Button(self.root, width=20, bg="mediumturquoise")
        self.delete_node_button["text"] = "Delete Node"
        self.delete_node_button.place(x=0, y=60)
        self.delete_node_button.bind('<Button-1>', self.delete_node)

        self.delete_channel_button = Button(self.root, width=20, bg="mediumturquoise")
        self.delete_channel_button["text"] = "Delete Channel"
        self.delete_channel_button.place(x=0, y=90)
        self.delete_channel_button.bind('<Button-1>', self.delete_channel)

        self.send_message_button = Button(self.root, width=20, bg="mediumturquoise")
        self.send_message_button["text"] = "Send message"
        self.send_message_button.place(x=0, y=120)
        self.send_message_button.bind('<Button-1>', self.send_message)

        self.root.mainloop()

    def add_node_event(self, event):
        self.clear()
        self.canvas.bind('<Button-1>', self.add_node)

    def add_node(self, event):
        global CURRENT_NODE_NUMBER
        new_view_node = Node(self.canvas, CURRENT_NODE_NUMBER, event.x, event.y)
        self.node_list.append(new_view_node)
        CURRENT_NODE_NUMBER += 1
        self.canvas.unbind('<Button-1>')

    def add_channel(self, event):
        self.clear()
        self.nodes_for_channel = []
        for element in self.node_list:
            if element.selected:
                self.nodes_for_channel.append(element)
        if len(self.nodes_for_channel) == 2:

            self.choose_label_1 = Label(self.root, text="Choose channel type:", font="Arial 12", bg="white")
            self.choose_label_1.place(x=0, y=150)

            self.channel_type = IntVar()
            self.channel_type.set(0)
            self.duplex = Radiobutton(self.root, text="Duplex", variable=self.channel_type, value=0)
            self.half_duplex = Radiobutton(self.root, text="Half-Duplex", variable=self.channel_type, value=1)
            self.duplex.place(x=0, y=180)
            self.half_duplex.place(x=0, y=210)

            self.choose_label_2 = Label(self.root, text="Choose how to set weight:", font="Arial 12", bg="white")
            self.choose_label_2.place(x=0, y=240)

            self.weight_type = IntVar()
            self.weight_type.set(0)
            self.random = Radiobutton(self.root, text="Random", variable=self.weight_type, value=0)
            self.manually = Radiobutton(self.root, text="Manually", variable=self.weight_type, value=1)
            self.random.place(x=0, y=270)
            self.manually.place(x=0, y=300)

            self.confirm_button = Button(self.root)
            self.confirm_button["text"] = "OK"
            self.confirm_button.place(x=0, y=330)
            self.confirm_button.bind('<Button-1>', self.confirm_channel)

    def confirm_channel(self, event):
        if self.channel_type.get() == 0:
            self.channel_type = "duplex"
        else:
            self.channel_type = "half-duplex"

        self.weight_type = self.weight_type.get()
        self.choose_label_1.destroy()
        self.choose_label_2.destroy()
        self.confirm_button.destroy()
        self.random.destroy()
        self.manually.destroy()
        self.duplex.destroy()
        self.half_duplex.destroy()

        if self.weight_type == 0:
            new_channel = Channel(self.canvas, [self.nodes_for_channel[0].name, self.nodes_for_channel[1].name],
                                  self.channel_type, [self.nodes_for_channel[0].x, self.nodes_for_channel[0].y,
                                                      self.nodes_for_channel[1].x, self.nodes_for_channel[1].y],
                                                      rnd.choice(CHANNEL_WEIGHTS))
            for element in self.node_list:
                if element in self.nodes_for_channel:
                    element.related_channels.append(new_channel)
            self.channel_list.append(new_channel)

            for element in self.node_list:
                if element.selected:
                    element.selected = False
                    self.canvas.itemconfig(element.view, fill=element.color)
        else:
            self.choose_label_3 = Label(self.root, text="Choose channel weight:", font="Arial 12", bg="white")
            self.choose_label_3.place(x=0, y=150)

            self.chosen_weight = StringVar(self.root)
            self.chosen_weight.set(CHANNEL_WEIGHTS[0])
            self.weight_list = OptionMenu(self.root, self.chosen_weight, 3, 5, 6, 7, 8, 10, 11, 15, 18, 21, 26, 31)
            self.weight_list.place(x=0, y=180)

            self.confirm_button = Button(self.root)
            self.confirm_button["text"] = "OK"
            self.confirm_button.place(x=130, y=180)
            self.confirm_button.bind('<Button-1>', self.confirm_channel_weight)

    def confirm_channel_weight(self, event):
        self.choose_label_3.destroy()
        self.weight_list.destroy()
        self.confirm_button.destroy()
        self.chosen_weight = int(self.chosen_weight.get(), 10)
        new_channel = Channel(self.canvas, [self.nodes_for_channel[0].name, self.nodes_for_channel[1].name],
                              self.channel_type, [self.nodes_for_channel[0].x, self.nodes_for_channel[0].y,
                                                  self.nodes_for_channel[1].x, self.nodes_for_channel[1].y],
                                                  self.chosen_weight)
        for element in self.node_list:
            if element in self.nodes_for_channel:
                element.related_channels.append(new_channel)
        self.channel_list.append(new_channel)

        for element in self.node_list:
            if element.selected:
                element.selected = False
                self.canvas.itemconfig(element.view, fill=element.color)

    def delete_channel(self, event):
        self.clear()
        for channel in self.channel_list:
            if channel.selected:
                channel.delete()
                self.channel_list.remove(channel)
                break
        for element in self.node_list:
            if channel in element.related_channels:
                element.related_channels.remove(channel)

    def delete_node(self, event):
        self.clear()
        channels_for_delete = []
        for element in self.node_list:
            if element.selected:
                element.delete()
                for channel in self.channel_list:
                    if channel in element.related_channels:
                        element.related_channels.remove(channel)
                        channels_for_delete.append(channel)
                        channel.delete()
                self.node_list.remove(element)
            for channel in channels_for_delete:
                self.channel_list.remove(channel)

    def clear(self):
        for channel in self.channel_list:
            channel.canvas.itemconfig(channel.view, fill=channel.current_color, width=channel.width)

    def send_message(self, event):
        self.clear()
        self.nodes_for_message = []
        for element in self.node_list:
            if element.selected:
                self.nodes_for_message.append(element)
        if len(self.nodes_for_message) == 1:
            self.size_label = Label(self.root, text="Message Size:", font="Arial 12")
            self.size_label.place(x=0, y=150)

            self.size_enter = Entry(self.root, width=5, bd=3)
            self.size_enter.place(x=115, y=150)

            self.package_size_label = Label(self.root, text="Package Size:", font="Arial 12")
            self.package_size_label.place(x=0, y=180)

            self.package_size_enter = Entry(self.root, width=5, bd=3)
            self.package_size_enter.place(x=115, y=180)

            self.send_type = IntVar()
            self.send_type.set(0)
            self.datagram = Radiobutton(self.root, text="Datagram", variable=self.send_type, value=0)
            self.connection = Radiobutton(self.root, text="Connection", variable=self.send_type, value=1)
            self.datagram.place(x=105, y=210)
            self.connection.place(x=105, y=240)

            self.confirm_button = Button(self.root)
            self.confirm_button["text"] = "OK"
            self.confirm_button.place(x=105, y=270)
            self.confirm_button.bind('<Button-1>', self.confirm_send)

    def create_graph(self, graph):
        for channel in self.channel_list:
            if not channel.disabled:
                flag = True
                for node in self.node_list:
                    if (node.name == channel.node2 and node.disabled) or (node.name == channel.node1 and node.disabled):
                        flag = False
                        break
                if flag:
                    graph.add_edge(channel.node1, channel.node2, channel.weight)
        return graph.edges
    

    def transform_route(self, route):
        i = 0
        route_channels = []
        for element in route:
            if i == 0:
                pass
            else:
                for channel in self.channel_list:
                    if (channel.node1 == route[i - 1] and channel.node2 == route[i]) or (channel.node2 == route[i - 1] and channel.node1 == route[i]):
                        route_channels.append(channel)
                        break
            i += 1
        return route_channels

    def confirm_send(self, event):
        self.message_size = self.size_enter.get()
        self.package_size = self.package_size_enter.get()
        if self.message_size == "" or self.package_size == "":
            self.warning = Tk()
            self.warning.title("Warning")
            self.warning_message = Label(self.warning, text="Fill all fields!!!", font="Arial 14", bg="red")
            self.warning_message.pack()
            self.warning.mainloop()
        else:
            self.message_size = int(self.message_size, 10)
            self.package_size = int(self.package_size, 10)
            if self.message_size < 1 or self.message_size > 65532:
                self.warning = Tk()
                self.warning.title("Warning")
                self.warning_message = Label(self.warning, text="Wrong message size!!!", font="Arial 14", bg="red")
                self.warning_message.pack()
                self.warning.mainloop()
            elif self.package_size < 1 or self.package_size > self.message_size:
                self.warning = Tk()
                self.warning.title("Warning")
                self.warning_message = Label(self.warning, text="Wrong package size!!!", font="Arial 14", bg="red")
                self.warning_message.pack()
                self.warning.mainloop()
            else:
                self.confirm_button.destroy()
                self.datagram.destroy()
                self.connection.destroy()
                self.size_label.destroy()
                self.package_size_label.destroy()
                self.size_enter.destroy()
                self.package_size_enter.destroy()
                for element in self.node_list:
                    if element.selected:
                        element.selected = False
                        self.canvas.itemconfig(element.view, fill=element.color)


                self.info_package_quantity = 0
                if self.message_size % self.package_size == 0:
                    self.info_package_quantity = self.message_size // self.package_size
                else:
                    self.info_package_quantity = self.message_size // self.package_size + 1

                self.package_list = []
                i = 1
                while i <= self.info_package_quantity:
                    if i != self.info_package_quantity:
                        self.package_list.append(Package(self.package_size, i))
                    else:
                        if self.message_size % self.package_size != 0:
                            self.package_list.append(Package(self.message_size % self.package_size, i))
                        else:
                            self.package_list.append(Package(self.package_size, i))
                    i += 1


                app = tk.Tk()
                app.title("Results")
                app.minsize(300, 300)
                app.maxsize()
                app.rowconfigure(0, weight=1)
                app.columnconfigure(0, weight=1)

                tab = tk.HList(app, columns=2, header=True)
                tab.grid(row=0, column=0, sticky="nswe")

                scroll = tk.Scrollbar(app, command=tab.yview)
                tab['yscrollcommand'] = scroll.set
                scroll.grid(row=0, column=1, sticky="nwse")

                # Создаем заголовки.
                tab.header_create(0, text="To node")
                tab.header_create(1, text="Time")

                counter = 0
                for finish_node in self.node_list:

                    self.graph = Graph()
                    self.graph_edges = self.create_graph(self.graph)

                    if self.nodes_for_message[0].name == finish_node.name:
                        continue
                    print("From ", self.nodes_for_message[0].name, " to ", finish_node.name)
                    self.route = dijkstra(self.graph.edges, self.nodes_for_message[0].name, finish_node.name)
                    counter += 1

                    self.route_channels = self.transform_route(self.route) 

                    #генерация ошибки в каналах маршрута
                    for channel in self.route_channels:
                        if rnd.random() <= channel.error_prob:
                            print ("Error in channel:" , channel.node1, channel.node2)

                            #удаление аз графа каналов с ошибкой
                            for edge in self.graph.edges:
                                if (edge[0]==channel.node1 and edge[1]==channel.node2):
                                    self.graph.edges.remove(edge)
                                    break
                            for edge in self.graph.edges:
                                if (edge[0]==channel.node2 and edge[1]==channel.node1):
                                    self.graph.edges.remove(edge)
                                    break

                            #поиск ноды, от которой нужно построить новый маршрут
                            i=0
                            for element in self.route:
                                if i==0:
                                    pass
                                else:
                                    if (channel.node1 == self.route[i - 1] and channel.node2 == self.route[i]):
                                        self.new_start_node = channel.node1
                                        break
                                    elif(channel.node2 == self.route[i - 1] and channel.node1 == self.route[i]):
                                        self.new_start_node = channel.node2
                                        break
                                i+=1
                                
                            #удаление лишнего ошибочного куска маршрута
                            self.old_route = self.route
                            self.route = []
                            for element in self.old_route:
                                if element != self.new_start_node:
                                    self.route.append(element)
                                else:
                                    break

                            #построение новой части маршрута и добавление её в основной маршрут вместо старой части
                            self.new_route_part = dijkstra(self.graph.edges, self.new_start_node, finish_node.name)
                            for element in self.new_route_part:
                                self.route.append(element)
                            self.route_channels = self.transform_route(self.route) 

                    print("Result route: ", self.route)
                                    

                    self.time = 0
                    self.service_data_size = 0
                    if self.send_type.get() == 0:
                        for channel in self.route_channels:
                            i = 1
                            for package in self.package_list:
                                self.time += (package.size + package.header) // 100 * channel.weight
                                if (package.size + package.header) % 100 != 0:
                                    self.time += ((package.size + package.header) % 100) / 100 * channel.weight
                        for package in self.package_list:
                            self.service_data_size += 24
                        print()


                    elif self.send_type.get() == 1:
                        for channel in self.route_channels:
                            self.time += 4 * 24 / 100 * channel.weight
                            for package in self.package_list:
                                self.time += (package.size + package.header) // 100 * channel.weight
                                if (package.size + package.header) % 100 != 0:
                                    self.time += ((package.size + package.header) % 100) / 100 * channel.weight
                                self.time += 24 / 100 * channel.weight
                        self.service_data_size += 24 * 4
                        for package in self.package_list:
                            self.service_data_size += 24 * 2
                        print()
                    index = '%s' % counter
                    tab.add(index, data="--<%s>--" % counter)
                    tab.item_create(index, 0, text=(finish_node.name))
                    if self.route != []:
                        tab.item_create(index, 1, text=(self.time))
                    else:
                        tab.item_create(index, 1, text=("Can't find route!"))

                    pack_quantity_lab1 = Label(app, text="Package quantity: ", font="Arial 14")
                    pack_quantity_lab1.place(x=0, y=0)
                    pack_quantity_lab2 = Label(app, text=str(self.info_package_quantity), font="Arial 14")
                    pack_quantity_lab2.place(x=155, y=0)

                    servise_data_lab1 = Label(app, text="Service data size: ", font="Arial 14")
                    servise_data_lab1.place(x=0, y=30)
                    servise_data_lab2 = Label(app, text=str(self.service_data_size), font="Arial 14")
                    servise_data_lab2.place(x=155, y=30)

                    from_node_lab1 = Label(app, text="From node: ", font="Arial 14")
                    from_node_lab1.place(x=0, y=60)
                    from_node_lab2 = Label(app, text=str(finish_node.name), font="Arial 14")
                    from_node_lab2.place(x=105, y=60)
                    
                        
                    tab.place(x=0, y=90)
                    self.route_channels = []
                    self.route = []


if __name__ == '__main__':
    CHANNEL_WEIGHTS = [3, 5, 6, 7, 8, 10, 11, 15, 18, 21, 26, 31]
    CURRENT_NODE_NUMBER = 0
    ITERATION = 1
    Main()
