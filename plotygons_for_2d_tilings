import matplotlib.pyplot as plt
from matplotlib.path import Path
import matplotlib.patches as patches



def find_extreme_value(polygons, x_y_or_z = 'x', min_or_max = 'max'):
    auxillary_dictionary = dict([('x',0),('y',1),('z',2)])
    list_of_x_y_or_z = []
    for polygon in polygons:
        for vertex in polygon:
            list_of_x_y_or_z.append(vertex[auxillary_dictionary[x_y_or_z]])
    if min_or_max == 'min':
        return min(list_of_x_y_or_z)
    else :
        return max(list_of_x_y_or_z)
    
    
def describe_polygon_path(polygon): #Polygon should be a list of verticies of form [(a,b),(c,d)....(x,y)]
    vertices = []
    for vertex in polygon:
        vertices.append(vertex)
    vertices.append(polygon[0])
    codes = [Path.MOVETO] + [Path.LINETO]*(len(polygon)-1) + [Path.CLOSEPOLY]
    return Path(vertices, codes)



def plot_polygons(polygons, figure_size = 8, grid_on = True,ticks_on = True,colours = \
    ['r','b','g','y','cyan','darkblue','lightblue','aqua',\
     'grey','pink','purple','gold','orange','darkred','orangered','lime','darkgreen']):
    '''
    
    Polygons should be a list of list of verticies of form [[(x1,y1),(x2,y2), ... ,(xn,yn)],...,[(X1,Y1),(X2,Y2), ... ,(Xn,Yn)]]
    where each polygon's vertices are described in an order s.t. one could connect the dots in order to draw the shape (but not last edge). 
    
    Eg To describe the rectangle with points (0,0),(1,2),(1,0),(0,2) 
    
    The input for this polygon must be [(0,0),(1,0),(1,2),(0,2)]
    or some other order where any two consecutive points an edge
    and all points communicate (as if last point and first point are joined also.
    
    '''
    kwds = dict(ec='k', alpha = 0.85) #alpha determines transluscency.
    figure = plt.figure()
    figure.set_size_inches(figure_size,figure_size)
    axis = figure.add_subplot(111)
    list_of_patches = [patches.PathPatch(describe_polygon_path(polygon),  \
                                         facecolor = colours[polygons.index(polygon)%len(colours)], lw = 1.3,**kwds) \
                       for polygon in polygons]
    for patch in list_of_patches:
        axis.add_patch(patch)
    plt.axis('scaled')
    axis.set_xlim(find_extreme_value(polygons,'x','min')-1,find_extreme_value(polygons,'x','max')+1)
    axis.set_ylim(find_extreme_value(polygons,'y','min')-1,find_extreme_value(polygons,'y','max')+1)
    if grid_on == True :
        axis.grid(True)   
    if ticks_on == False:
        axis.set_xticks([])
        axis.set_yticks([])
    plt.show()
    return None

#The following functions are used to convert a given face in a tiling2()
#into connect the dot form for plotting.

def face_into_co_ordinates(face): 
    '''
    Should take a face from tiling2.faces.keys() and convert into the form
    [[(x_1,y_1),(x_2,y_2)],...,[(x_{n-1},y_{n-1}),(x_n,y_n)]] 
    where (x_i,y_i) are the values of the corresponding vertex
    as well as rounding these values.
    '''
    new_face_of_co_ordinates = []
    for edge in list(face):
        new_face_of_co_ordinates += [[[(list(edge)[0].x),(list(edge)[0].y)],[(list(edge)[1].x),(list(edge)[1].y)]]]
    return new_face_of_co_ordinates







def face_edges_in_order(face, safety_limit = 100000000): 
    '''
    Should take a face that has been converted into co-ordinate form
    and return it with the edges in order of connection 
    for a closed path of the shape with out considering the directionof an edge yet.
    
    
    Eg. For the rectangle with points (0,0),(0,1),(3,0),(3,1)
    the function takes the list of edges [[(0,0),(0,1)],[(3,1),(3,0)],[(0,1),(3,1)],[(0,0),(3,0)]]
    and returns them in the order [[(0,0),(0,1)],[(0,1),(3,1)],[(3,1),(3,0)],[(0,0),(3,0)]]
    as these edges communicate in this order (without considering direction of edge).
    
    '''
    list_of_ordered_edges =[face[0]] # Take first edge of given face.
    list_of_potential_edges = face[1:] # Consider the remaining edges.
    count = 0
    while len(list_of_ordered_edges) < len(face): # Keep repeating proccess until completion.
        for potential_edge in list_of_potential_edges:
            count += 1
            for vertex in potential_edge:
                if vertex in list_of_ordered_edges[::-1][0]: 
                    #Checks all potential edges to see if they comunicate then removes from the list of potential edges and repeats.
                    list_of_ordered_edges += [potential_edge]
                    list_of_potential_edges.pop(list_of_potential_edges.index(potential_edge))
                    break
            if count >  safety_limit: # While loop safeguard.
                print "The Safety Limit has been reached."
                return None
    return list_of_ordered_edges


def face_vertices_in_order(face): 
    '''
    Now we need to make sure all the vertices are in correct order for communication of edges.
    
    This function will take face of the form 
    
    [[(x1,y1),(x2,y2)],[(x3,y3), (x2,y2)],...,[(x_n,y_n),(x_{n-1},y_{n-1}))]]
    where the edges are in order but the vertices may not be
    
    and return it with vertices in order
    
    [[(x1,y1),(x2,y2)],[(x2,y2),(x3,y3), ],...,[(x_{n-1},y_{n-1}),(x_n,y_n)]]
    '''
    if face[0][1]  in  face[1]:
        new_ordered_list = [face[0]]
    else :
        new_ordered_list = [face[0][::-1]]
    for index in range(1,len(face)):
        if list(face)[index][0] != new_ordered_list[index-1][1] :
            new_ordered_list += [face[index][::-1]]
        else :
            new_ordered_list += [face[index]]
    return new_ordered_list

def turn_prepared_face_into_plotygon_path(prepared_face):
    '''
    Takes [[(x1,y1),(x2,y2)],[(x2,y2),(x3,y3), ],...,[(x_{n-1},y_{n-1}),(x_n,y_n)]]
    (with ordered edges and vertices)
    and returns the vertices in connect the dots order :
    [(x1,y1),(x2,y2), ... , (xn,yn)]
    
    '''
    plotygon_path = [tuple(vertex) for vertex in prepared_face[0][1:2]]
    for edge in prepared_face[1:]:
        plotygon_path += [tuple(edge[1])]
    return plotygon_path


def prepare_tiling2_face(face):
    return turn_prepared_face_into_plotygon_path(face_vertices_in_order(face_edges_in_order(face_into_co_ordinates(face))))

def plot_faces_of_tiling2(faces):
    list_of_prepared_faces = []
    for face in faces:
        list_of_prepared_faces += [prepare_tiling2_face(face)]
    plot_polygons(list_of_prepared_faces)
    return None
