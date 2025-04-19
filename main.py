import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.widgets import Button
from matplotlib.widgets import TextBox
import random


class GraphSketchpad:
    def __init__(self):
        self.G = nx.MultiGraph(arrows=True)
        self.fig, self.ax = plt.subplots(figsize=(10, 8))
        self.fig.subplots_adjust(bottom=0.2, right=0.8)

        self.pos = nx.spring_layout(self.G)
        self.selected_node = None
        self.dragging = False
        self.current_node = None

        # Setup text display boxes
        self.nodeName_ax = plt.axes([0.85, 0.8, 0.15, 0.075])
        self.nodeName_ax.axis('off')

        self.counts_ax = plt.axes([0.05, 0.9, 0.15, 0.075])
        self.counts_ax.axis('off')

        # setup new label input
        self.ax_label_input = plt.axes([0.925, 0.3, 0.05, 0.05])
        self.label_input = TextBox(
            self.ax_label_input,
            'New Label: ',
            initial=""
        )
        self.label_input.on_submit(self.changeLabel)

        # Setup button areas
        self.ax_show_bridges = plt.axes([0.025, 0.125, 0.15, 0.05])
        self.ax_add_node = plt.axes([0.225, 0.125, 0.15, 0.05])
        self.ax_add_edge = plt.axes([0.425, 0.125, 0.15, 0.05])
        self.ax_remove = plt.axes([0.625, 0.125, 0.15, 0.05])
        self.ax_clear = plt.axes([0.825, 0.125, 0.15, 0.05])
        self.ax_yellow = plt.axes([0.825, 0.7, 0.15, 0.075])
        self.ax_green = plt.axes([0.825, 0.6, 0.15, 0.075])
        self.ax_blue = plt.axes([0.825, 0.5, 0.15, 0.075])
        self.ax_changeLabel = plt.axes([0.825, 0.4, 0.15, 0.075])
        self.ax_bipartite = plt.axes([0.025, 0.025, 0.15, 0.05])
        self.ax_coloring = plt.axes([0.225, 0.025, 0.15, 0.05])

        # Create button objects
        self.btn_show_bridges = Button(self.ax_show_bridges, 'Show Bridges')
        self.btn_add_node = Button(self.ax_add_node, 'Add Node')
        self.btn_add_edge = Button(self.ax_add_edge, 'Add Edge')
        self.btn_remove = Button(self.ax_remove, 'Remove')
        self.btn_clear = Button(self.ax_clear, 'Clear All')
        self.btn_yellow = Button(self.ax_yellow, 'Yellow')
        self.btn_green = Button(self.ax_green, 'Green')
        self.btn_blue = Button(self.ax_blue, 'Blue')
        self.btn_changeLabel = Button(self.ax_changeLabel, 'Change Label')
        self.btn_bipartite = Button(self.ax_bipartite, 'Check Bipartite')
        self.btn_coloring = Button(self.ax_coloring, 'Minimal Coloring')


        # Connect button click handlers
        self.btn_show_bridges.on_clicked(self.showBridges)
        self.btn_add_node.on_clicked(self.on_addNode)
        self.btn_add_edge.on_clicked(lambda event: self.setMode(self.ADD_EDGE_MODE))
        self.btn_remove.on_clicked(lambda event: self.setMode(self.REMOVE_MODE))
        self.btn_clear.on_clicked(self.on_clear)
        self.btn_yellow.on_clicked(self.makeYellow)
        self.btn_green.on_clicked(self.makeGreen)
        self.btn_blue.on_clicked(self.makeBlue)
        self.btn_changeLabel.on_clicked(self.changeLabel)
        self.btn_bipartite.on_clicked(self.check_bipartite)
        self.btn_coloring.on_clicked(self.minimal_coloring)

        self.buttonColors()
        self.updateNodeMenu()
        self.updateCounts()

        self.activeMode = 0
        self.MOVE_MODE = 0
        self.ADD_EDGE_MODE = 1
        self.REMOVE_MODE = 2

        self.setMode(0)
        self.next_node_id = 0
        self.firstNodeEdge = -1

        self.draw_graph()

        # Connect mouse event handlers
        self.fig.canvas.mpl_connect('button_press_event', self.on_press)
        self.fig.canvas.mpl_connect('button_release_event', self.on_release)
        self.fig.canvas.mpl_connect('motion_notify_event', self.on_motion)

    # changes all buttons to the normal gray color
    def buttonColors(self):
        default_color = '0.85'
        default_hover = '0.95'

        self.btn_add_node.color = default_color
        self.btn_add_node.hovercolor = default_hover
        self.btn_add_edge.color = default_color
        self.btn_add_edge.hovercolor = default_hover
        self.btn_remove.color = default_color
        self.btn_remove.hovercolor = default_hover
        self.btn_clear.color = default_color
        self.btn_clear.hovercolor = default_hover
        self.btn_yellow.color = default_color
        self.btn_yellow.hovercolor = default_hover
        self.btn_green.color = default_color
        self.btn_green.hovercolor = default_hover
        self.btn_blue.color = default_color
        self.btn_blue.hovercolor = default_hover

    # used to change program the mode when a button is pressed
    def setMode(self, modeNum):
        if self.activeMode == modeNum:
            self.buttonColors()
            self.activeMode = self.MOVE_MODE
        elif modeNum == self.ADD_EDGE_MODE:
            self.buttonColors()
            self.btn_add_edge.color = 'lightgreen'
            self.btn_add_edge.hovercolor = 'green'
            self.activeMode = self.ADD_EDGE_MODE
        elif modeNum == self.REMOVE_MODE:
            self.buttonColors()
            self.btn_remove.color = 'lightcoral'
            self.btn_remove.hovercolor = 'red'
            self.activeMode = self.REMOVE_MODE

        self.fig.canvas.draw_idle()

    # changes the current node to yellow
    def makeYellow(self, event):
        if self.current_node is not None:
            self.G.nodes[self.current_node]['color'] = 'yellow'
            self.draw_graph()

    # changes the current node to green
    def makeGreen(self, event):
        if self.current_node is not None:
            self.G.nodes[self.current_node]['color'] = 'green'
            self.draw_graph()

    # changes the current node to blue
    def makeBlue(self, event):
        if self.current_node is not None:
            self.G.nodes[self.current_node]['color'] = 'skyblue'
            self.draw_graph()

    # changes the label of the current node
    def changeLabel(self, event):
        if self.current_node is not None and self.label_input.text != "None" and self.label_input != "" and len(self.label_input.text) <= 10:
            new_label = self.label_input.text
            self.G.nodes[self.current_node]['label'] = new_label
            self.draw_graph()
            self.updateNodeMenu()

    # updates the node information on the side menu (node name, node label, node degree)
    def updateNodeMenu(self):
        # remove previous text
        for textbox in self.nodeName_ax.artists + self.nodeName_ax.texts:
            textbox.remove()

        # set node text
        if self.current_node is None:
            self.nodeName_output = self.nodeName_ax.text(
                0.05, 0.95,
                f"Node: None\nLabel: None\nDegree: None",
                ha='left', va='top',
                wrap=True,
                fontsize=10,
                transform=self.nodeName_ax.transAxes
            )
        else:
            self.nodeName_output = self.nodeName_ax.text(
                0.05, 0.95, f"Node: {self.current_node}\nLabel: {self.G.nodes[self.current_node].get('label', '')}\nDegree: {self.G.degree[self.current_node]}",
                ha='left', va='top',
                wrap=True,
                fontsize=10,
                transform=self.nodeName_ax.transAxes
            )

    # updates the text output in the top left (number of nodes, number of edges, is connected, etc.)
    def updateCounts(self):
        # remove previous text
        for textbox in self.counts_ax.artists + self.counts_ax.texts:
            textbox.remove()

        # find the minimum coloring
        min_color = nx.coloring.greedy_color(self.G, 'largest_first')
        vals = [-1] if len(min_color.values()) == 0 else min_color.values()
        required_colors = max(vals) + 1

        # determine what to print for is connected
        is_connected = "No Graph" if self.G.order() == 0 else nx.is_connected(self.G)

        # update counts text
        self.counts_output = self.counts_ax.text(
            0.05, 0.95,
            f"Node Count: {self.G.order()}    Edge Count: {self.G.size()}\n"
            f"Is Connected: {is_connected}    Component Count: {nx.number_connected_components(self.G)}\n"
            f"Is Planar: {nx.is_planar(self.G)}    Is Bipartite: {nx.is_bipartite(self.G)}\n"
            f"Minimal Coloring: {required_colors} (can show up to 5)",
            ha='left', va='top',
            wrap=True,
            fontsize=10,
            transform=self.counts_ax.transAxes
        )

        self.resetEdgeColors()

    # turns bridges red, so they can be easily seen in the graph
    def showBridges(self, event):
        bridges = list(nx.bridges(self.G))

        for bridge in bridges:
            self.G[bridge[0]][bridge[1]][0]['color'] = 'red'

    # changes all edge colors to black
    def resetEdgeColors(self):
        for u, v, key in self.G.edges(keys=True):
            self.G.edges[u, v, key]['color'] = 'black'

    # draw the graph
    def draw_graph(self):
        self.ax.clear()

        nodeColors = [self.G.nodes[n]['color'] for n in self.G.nodes()]

        # Draw nodes
        nx.draw_networkx_nodes(self.G, self.pos, ax=self.ax, node_size=500,
                               node_color=nodeColors)

        # Draw edges with curvature to show parallel edges
        for u, v, key, data in self.G.edges(keys=True, data=True):
            edge_color = data.get('color', 'black')

            if self.G.number_of_edges(u, v) > 1:
                rad = 0.2 + 0.1 * key
                nx.draw_networkx_edges(
                    self.G, self.pos, ax=self.ax,
                    edgelist=[(u, v)],
                    edge_color=edge_color,
                    connectionstyle=f'arc3,rad={rad}',
                    width=2,
                    arrows=True
                )
            else:
                nx.draw_networkx_edges(
                    self.G, self.pos, ax=self.ax,
                    edgelist=[(u, v)],
                    edge_color=edge_color,
                    width=2
                )

        # Highlight selected node if exists
        if self.selected_node is not None:
            nx.draw_networkx_nodes(self.G, self.pos, ax=self.ax,
                                   nodelist=[self.selected_node],
                                   node_size=500, node_color='red')

        # Draw labels
        labels = {n: self.G.nodes[n].get('label', str(n)) for n in self.G.nodes()}
        nx.draw_networkx_labels(self.G, self.pos, labels=labels, ax=self.ax)

        plt.draw()

    # colors the graph bipartite if possible
    def check_bipartite(self, event):
        if nx.is_bipartite(self.G):
            coloring = nx.bipartite.color(self.G)
            for key in coloring.keys():
                if coloring[key] == 0:
                    self.G.nodes[key]['color'] = 'green'
                else:
                    self.G.nodes[key]['color'] = 'yellow'
        self.draw_graph()

    # color the graph with its minimal coloring (up to 5)
    def minimal_coloring(self, event):
        coloring = nx.coloring.greedy_color(self.G, strategy='largest_first')
        for key in coloring.keys():
            if coloring[key] == 0:
                self.G.nodes[key]['color'] = 'green'
            elif coloring[key] == 1:
                self.G.nodes[key]['color'] = 'yellow'
            elif coloring[key] == 2:
                self.G.nodes[key]['color'] = 'purple'
            elif coloring[key] == 3:
                self.G.nodes[key]['color'] = 'orange'
            else:
                self.G.nodes[key]['color'] = 'skyblue'
        self.draw_graph()

    # check if a node was clicked
    def is_node_clicked(self, event, node, threshold=0.05):
        node_x, node_y = self.pos[node]
        distance_squared = (node_x - event.xdata) ** 2 + (node_y - event.ydata) ** 2
        return distance_squared < threshold ** 2

    # Check if an edge was clicked
    def is_edge_clicked(self, event, u, v, threshold=0.03):
        u_pos = self.pos[u]
        v_pos = self.pos[v]

        # Simple line segment distance calculation
        line_vec = (v_pos[0] - u_pos[0], v_pos[1] - u_pos[1])
        click_vec = (event.xdata - u_pos[0], event.ydata - u_pos[1])
        line_len = (line_vec[0] ** 2 + line_vec[1] ** 2) ** 0.5

        if line_len == 0:
            return False

        # Projection of click point onto the line
        t = max(0, min(1, (click_vec[0] * line_vec[0] + click_vec[1] * line_vec[1]) / line_len ** 2))
        proj = (u_pos[0] + t * line_vec[0], u_pos[1] + t * line_vec[1])

        # Distance from click to projection
        distance = ((event.xdata - proj[0]) ** 2 + (event.ydata - proj[1]) ** 2) ** 0.5
        return distance < threshold

    # called every time the mouse is clicked to determine how the graph should be updated
    def on_press(self, event):
        if event.inaxes != self.ax:
            return

        # check each edge for click and delete if in remove mode
        for edge in self.G.edges():
            if self.is_edge_clicked(event, edge[0], edge[1]):
                if self.activeMode == self.REMOVE_MODE:
                    self.G.remove_edge(edge[0], edge[1])
                    break

        # Check each node for clicks and handle based on mode
        for node in self.G.nodes():
            if self.is_node_clicked(event, node):
                if event.button == 1:  # left click
                    self.add_edge(node)
                    if self.activeMode == self.MOVE_MODE:
                        self.selected_node = node
                        self.dragging = True
                        self.draw_graph()
                    elif self.activeMode == self.REMOVE_MODE:
                        self.G.remove_node(node)
                elif event.button == 3:  # right click
                    self.current_node = node
                    self.updateNodeMenu()
                break
        self.updateCounts()

    # called when the add edge mode is used and a node is clicked. adds an edge when the second node is clicked.
    def add_edge(self, node):
        if self.activeMode != self.ADD_EDGE_MODE:
            return

        # if there is no first node set the first node
        if self.firstNodeEdge == -1:
            self.firstNodeEdge = node
        else: # otherwise add an edge
            self.G.add_edge(self.firstNodeEdge, node)
            self.firstNodeEdge = -1
            self.draw_graph()
        self.updateCounts()


    # handles mouse release
    def on_release(self, event):
        self.dragging = False
        self.selected_node = None
        self.draw_graph()

    # handles mouse movement
    def on_motion(self, event):
        if not self.dragging or self.selected_node is None:
            return

        # Update node position while moving
        if event.inaxes == self.ax:
            self.pos[self.selected_node] = (event.xdata, event.ydata)
            self.draw_graph()

    def on_addNode(self, event):
        pos_x = random.uniform(-1, 1)
        pos_y = random.uniform(-1, 1)
        self.G.add_node(self.next_node_id, pos=(pos_x, pos_y), color='skyblue')
        self.pos[self.next_node_id] = (pos_x, pos_y)
        self.next_node_id += 1
        self.draw_graph()
        self.updateCounts()

    def on_clear(self, event):
        self.next_node_id = 0
        self.G.clear()
        self.draw_graph()
        self.updateCounts()


# Run the sketchpad
sketchpad = GraphSketchpad()
plt.show()