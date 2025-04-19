# Features

I completed my graph theorist’s sketchpad using the Networkx and Matplotlib libraries for Python. This application can show the vertices and edges of a graph, and the vertices can be moved while keeping adjacencies. Parallel edges are shown as curved lines so that several can be shown at the same time. Loops also appear in the graph.

Under the main display window for the graph several buttons allow the user to show bridges in the graph, add a node, add edges, remove nodes or edges, clear the graph, color the graph bipartite (only if it is bipartite), or color the graph with its minimal coloring (up to 5 colors).

On the right side of the main display there is a node specific menu that can be used to change the color or label of a node. A node can be selected by right clicking it. This side menu will display the node’s ID number, label, and degree while allowing the user to change its color to yellow, green, or blue. A new label can also be entered for the node under these buttons.

Above the display in the top left corner there is a text box that shows how many nodes and edges the graph has, whether the graph is connected, the number of components, whether the graph is planar or bipartite, and the minimal coloring for the graph.

# Functions

__init__()
This project is in a class called GraphSketchpad. When an instance of this object is created, the application begins working. The __init__() function creates the graph, display window, buttons, and text display boxes. The selected_node and current_node are set to none. Selected_node is used to keep track of a node that is being moved using the left click on the mouse. Current_node is the node that will be modified by the side menu (change color or label). The current_node is selected by using right click on the mouse.

activeMode (initialized in __init__()) is used to keep track of what the program should do when a node or edge is clicked. Using the left click while the “move” mode is active allows the user to move a node around the display window while keeping its adjacencies. The program is in move mode if the “remove” and “add edge” buttons are both gray. When the program is in “add edge” mode, the user can select two nodes to create an edge between them. The user can also select the same edge twice to create a loop. The “add edge” mode is active when the “add edge” button is green. When the program is in “remove” mode the user can select a vertex or edge to remove it. The user can tell this mode is active because the “remove” button will be red.

The __init__() function also connects buttons and mouse clicks to their corresponding functions.

buttonColors()
The buttonColors() function sets all buttons to their default gray color. This is used to change all buttons back after the mode is changed. This function is called in setMode(), where the mode is changed and button colors are set to indicate the mode.

setMode()
This function changes the activeMode for the program between “move” mode, “add edge” mode, and “remove” mode. This function also changes the button colors so the user knows which mode they are currently using. setMode() is called when the “add edge” or “remove” buttons are clicked to set the active mode to the corresponding value.

makeYellow(), makeGreen(), MakeBlue()
These three functions are used to change the current_node to the corresponding color. Once the color of the current node is changed the graph is redrawn to display the change. These functions are called by the appropriate buttons on the side menu.

ChangeLabel()
This function is used to change the label of the current node. The new label is taken from the input textbox on the side menu and checked to make sure it isn’t an empty string or larger than 10 characters. After this, the label for the current node is set to the new value, and the draw_graph() and updateNodeMenu() functions are called to update the new label in the graph and side menu.

updateNodeMenu()
The updateNodeMenu() function is used to update the text output that shows the current node’s name, label, and degree in the side menu. It starts by removing the text that was previously in this location, then sets the text to show none for these values if the current node is none, otherwise, the proper values are displayed.

updateCounts()
The updateCounts() function resets the text output in the top left of the window. This includes the number of nodes, the number of edges, and whether the graph is planar. The function first removes any text in its location, then determines the proper values to print using functions in the Networkx library, including is_bipartite(), is_planar(), and coloring.greedy_color().

showBridges()
This function gets a list of bridges from the graph using the Networkx bridges() function. Then, each edge that was identified as a bridge is colored red. showBridges() is called when the “show bridges” button is pressed.

resetEdgeColors()
resetEdgeColors() changes all edge colors to black. This is called in the updateCounts() function to make sure edge colors are reset to black after every change to the graph. This ensures that if a change is made that turns edges into links all edges will be reset, and the “show bridges” button will need to be pressed again to find and highlight bridges.

draw_graph()
This function is used to draw the graph in the display window. First, it clears the window and then gets a list of colors to display the nodes. Next, the nodes are printed, followed by the edges. If there are parallel edges, each one is displayed with a different curve so that more than one can be seen. Labels are also printed, and if one node is selected, it gets turned red.

check_bipartite()
This function checks to see whether the graph is bipartite using the Networkx is_bipartite() function. If the graph is bipartite, the Networkx function bipartite.color() is used to get a coloring for the graph. Then the graph is colored yellow and green based on the bipartite coloring.

minimal _coloring()
This function gets the minimal coloring for the graph using Networkx coloring.greedy_color() function with the “largest first” strategy. Then the graph is colored based on the returned coloring, up to 5 different colors.

is_node_clicked()
This function checks to see if a node was clicked. It is called in on_press() to check each time the mouse is clicked.

is_edge_clicked()
This function checks to see if an edge was clicked. It is called in on_press().

on_press()
This function is called every time the mouse is clicked. First, the function checks to see if the click was in the window. If it was, then the edges are checked using the is_edge_clicked() function and deleted if in remove mode. After this nodes are checked and the graph is updated depending on the mode and whether the click was left or right.

add_edge()
This function is called when a node is clicked in the on_press() function. The first node is saved as firstNodeEdge, then when the next node is chosen, an edge is created, and the firstNodeEdge is reset.

On_release()
Handles when the mouse is released. Dragging is set to false and the selected_node is set to None.

on_motion()
Updates the position of a node that is being moved and calls draw_graph() to update the graph.

on_addNode()
Adds a new node to the screen in a random location. This function is called when the “add node” button is pressed.

on_clear()
Clears the graph and calls draw_graph() to update the window.
