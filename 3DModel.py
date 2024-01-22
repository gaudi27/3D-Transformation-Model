import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Slider, RadioButtons
from matplotlib.collections import LineCollection

#############################
# MATPLOTLIB CONFIGURATIONS #
#############################

# set up subplots
fig, axes = plt.subplot_mosaic(
    [['main', 'log'],
     ['main', 'shape'],
     ['main', '.']],
    width_ratios=[3.5, 1.5],
    height_ratios=[2, 2, 1])

# make room in plot for sliders
fig.subplots_adjust(left=0.25, bottom=0.25, right=0.75)

# settings
axes['main'].set_xlim((-6, 6))
axes['main'].set_ylim((-6, 6))
axes['main'].set_aspect('equal')
axes['main'].set_autoscale_on(False)
axes['main'].xaxis.set_tick_params(labelbottom=False)
axes['main'].yaxis.set_tick_params(labelleft=False)
axes['main'].set_xticks([])
axes['main'].set_yticks([])
axes['main'].set_title("3D Graphics Demo")
axes['shape'].set_title("Shapes")
axes['log'].axis('off')

###############
# WIRE FRAMES #
###############

# a point is represented as a 3-element tuple
# a line segment is represented as a 2-element list of points
# a wireframe object is represented as list of line segments

cube = [[(-1, -1, -1), (1, -1, -1)],
        [(1, -1, -1), (1, 1, -1)],
        [(1, 1, -1), (-1, 1, -1)],
        [(-1, 1, -1), (-1, -1, -1)],
        [(-1, -1, -1), (-1, -1, 1)],
        [(1, -1, -1), (1, -1, 1)],
        [(1, 1, -1), (1, 1, 1)],
        [(-1, 1, -1), (-1, 1, 1)],
        [(-1, -1, 1), (1, -1, 1)],
        [(1, -1, 1), (1, 1, 1)],
        [(1, 1, 1), (-1, 1, 1)],
        [(-1, 1, 1), (-1, -1, 1)]]

pyramid = [[(-1, -1, -1), (-1, -1, 1)],
           [(-1, -1, 1), (1, -1, 1)],
           [(1, -1, 1), (1, -1, -1)],
           [(1, -1, -1), (-1, -1, -1)],
           [(-1, -1, -1), (0, 1, 0)],
           [(-1, -1, 1), (0, 1, 0)],
           [(1, -1, 1), (0, 1, 0)],
           [(1, -1, -1), (0, 1, 0)]]

extra_credit = [[(0, 0, 0), (1, 1, 1)]] # TODO: (extra credit) create your own wireframe

guide_axes = [[(-0.75, 0, 0), (0.75, 0, 0)],
              [(0, -0.75, 0), (0, 0.75, 0)],
              [(0, 0, -0.75), (0, 0, 0.75)]]

def shape_to_hom_matrix(shape):
    """converts a wireframe object matrix of points in homogeneous coordinates

    Parameters:

    shape: list line segments (see above)

    Returns:

    2D numpy array with shape (4, 2(n + 3)) where SHAPE has n line segments

    Each column is the homogeneous coordinates of an endpoint in SHAPE

    Example:

    >>> shape_to_home_matrix([])
    array([[-0.75,  0.75,  0.  ,  0.  ,  0.  ,  0.  ],
           [ 0.  ,  0.  , -0.75,  0.75,  0.  ,  0.  ],
           [ 0.  ,  0.  ,  0.  ,  0.  , -0.75,  0.75],
           [ 1.  ,  1.  ,  1.  ,  1.  ,  1.  ,  1.  ]])

    """
    shape = shape + guide_axes
    m = np.array(list(map(np.array, sum(shape, [])))).T
    return np.apply_along_axis(lambda p : np.append(p, [1]), 0, m)

shape_matrices = {'cube': shape_to_hom_matrix(cube),
                  'pyramid': shape_to_hom_matrix(pyramid),
                  'TODO': shape_to_hom_matrix(extra_credit)} # TODO: (extra credit) change the name of the shape

# the shape being viewed
base_matrix = shape_matrices['cube']

###################
# TRANSFORMATIONS #
###################

# dictionary of global parameters
# updated by the sliders
global_params = { 'd' : 10,    # distance (for perspective)
                  'tx' : 0.0,  # x-axis translation
                  'ty' : 0.0,  # y-axis translation
                  'tz' : 0.0,  # z-axis translation
                  'rx' : 0.0,  # roll rotation
                  'ry' : 0.0,  # pitch rotation
                  'rz' : 0.0 } # yaw rotation

def perspective(d):
    """Perspective matrix

    Parameters:

    d: float

    Returns:

    2D numpy array

    the perspective projection matrix for a viewpoint as (0, 0, d)

    """
    x = np.eye(4)
    x[2] = [0, 0, 0, 0]
    x[3] = [0, 0, (-1)/d, 1]
    # TODO: fill in this function and change its return value
    return x

def hom_rotate_x(theta):
    """Rotation about the x-axis for homogeneous coordinates

    Parameters:

    theta: float, representing an angle in radians

    Returns:

    2D numpy array

    the matrix which rotates THETA around the x-axis, in homogeneous coordinates

    """
    # TODO: fill in this function and change its return value

    x = np.eye(4)
    
    x[1] = [0, np.cos(theta), -(np.sin(theta)), 0]
    x[2] = [0, np.sin(theta), np.cos(theta), 0]
    return x

def hom_rotate_y(theta):
    """Rotation about the y-axis for homogeneous coordinates

    Parameters:

    theta: float, representing an angle in radians

    Returns:

    2D numpy array

    the matrix which rotates THETA around the y-axis, in homogeneous coordinates

    """
    # TODO: fill in this function and change its return value
    x = np.eye(4)
    x[0] = [np.cos(theta), 0, np.sin(theta), 0]
    x[2] = [-(np.sin(theta)), 0, np.cos(theta), 0]
    return x

def hom_rotate_z(theta):
    """Rotation about the z-axis for homogeneous coordinates

    Parameters:

    theta: float, representing an angle in radians

    Returns:

    2D numpy array

    the matrix which rotates THETA around the z-axis, in homogeneous coordinates

    """
    # TODO: fill in this function and change its return value
    x = np.eye(4)
    x[0] = [np.cos(theta), -(np.sin(theta)), 0, 0]
    x[1] = [np.sin(theta), np.cos(theta), 0, 0]
    return x

def translate(x, y, z):
    """Translation matrix

    Parameters:

    x: float
    y: float
    z: float

    Returns:

    2D numpy array

    the matrix which translates by the vector np.array([x, y, z])

    """
    # TODO: fill in this function and change its return value
    a = np.eye(4)
    a[0] = [1, 0, 0, x]
    a[1] = [0, 1, 0, y]
    a[2] = [0, 0, 1, z]
    return a

def full_transform_matrix():
    """Full transform with perspective projection

    Returns:

    2D numpy array

    the matrix which implements the general rotation, translation and
    perspective projection using the global parameters

    Note: This must be done so that translations move the rotation
    axes. In particular, the centerpoint the guide axes should remain
    fixed when rotating, even after translation

    """
    p = global_params # you will need to use this in your implementation
    # TODO: fill in this function and change its return value
    # NOTE: you MUST use the function np.linalg.multi_dot
    multiplication = np.linalg.multi_dot([ 
    perspective(p['d']),
    translate(p['tx'], p['ty'], p['tz']),
    hom_rotate_x(p['rx']), 
    hom_rotate_y(p['ry']), 
    hom_rotate_z(p['rz'])])
    return multiplication

def matrix_to_projection(m):
    """Converts a set of transformed homogeneous coordinates into a list of 2D line segments

    Parameters:

    m : 2D numpy array with 4 rows and even number of columns

    Returns:

    list of pairs of 2-element 1D numpy arrays

    each pair represents a line segment in 2 dimensions

    Example:

    >>> matrix_to_projection(np.array([[1, 1, 1, 1], [1, 1, 1, 1], [0, 0, 0, 0], [1, 2, 3, 4]]))
    [(array([1., 1.]), array([0.5, 0.5])), (array([0.33333333, 0.33333333]),array([0.25, 0.25]))]

    """
    assert(m.shape[0] == 4)                           # you may assume m has four rows
    assert(m.shape[1] % 2 == 0)                       # and an even number of columns
    # assert(np.allclose(m[2], np.zeros(m.shape[1]))) # and that its third row is all zeros
    # TODO: fill in this function and change its return value
    arr = []
    arr2 = []
    for i in range(0, len(m[0])):
        first = (m[0][i])/(m[3][i])
        second = (m[1][i])/(m[3][i])
        x = np.array([first, second])
        arr.append(x)
    j = 0
    while j < len(arr)-1:
        y = np.array([arr[j], arr[j+1]])
        arr2.append(y)
        print(j)
        j+=2
    return arr2

def full_transform(shape_matrix):
    return matrix_to_projection(full_transform_matrix() @ shape_matrix)

###########
# DISPLAY #
###########

lc = LineCollection(
    full_transform(base_matrix),
    linewidth=1,
    colors=(base_matrix.shape[1] // 2 - 3) * ['C0'] + ['r', 'g', 'b'])
s = axes['main'].add_collection(lc)

def update_curr_shape():
    s.set(segments=full_transform(base_matrix))

def set_curr_shape(m):
    global base_matrix
    base_matrix = m
    update_curr_shape()
    s.set(colors=(base_matrix.shape[1] // 2 - 3) * ['C0'] + ['r', 'g', 'b'])

#######
# LOG #
#######

def log():
    return f"""
Transformation (Homogeneous):
-----------------------------

{full_transform_matrix()}

"""

log_text = axes['log'].text(0, 0, log(), name='Courier', fontsize=9)
update_log = lambda: log_text.set(text=log())

###########
# SLIDERS #
###########

slider_position = lambda index: [0.25, 0.20 - 0.03 * index, 0.45, 0.03]
slider = lambda name, pos, r: Slider(
    ax=fig.add_axes(slider_position(pos)),
    label=name,
    valmin=-r,
    valmax=r,
    valinit=0.0,
    valstep=0.1)

theta_slider_x = slider('roll', 0, 7.0)
theta_slider_y = slider('pitch', 1, 7.0)
theta_slider_z = slider('yaw', 2, 7.0)
trans_slider_x = slider('x', 3, 5.0)
trans_slider_y = slider('y', 4, 5.0)
trans_slider_z = slider('z', 5, 5.0)

def set_update(pname, slider):
    def update(val):
        global_params[pname] = val
        update_curr_shape()
        update_log()
        fig.canvas.draw_idle()
    slider.on_changed(update)

updates = [('rx', theta_slider_x),
           ('ry', theta_slider_y),
           ('rz', theta_slider_z),
           ('tx', trans_slider_x),
           ('ty', trans_slider_y),
           ('tz', trans_slider_z)]

# connect sliders to functions
for name, slider in updates:
    set_update(name, slider)

#################
# RADIO BUTTONS #
#################

shape_radio = RadioButtons(axes['shape'] , list(shape_matrices.keys()))

def shapes(label):
    set_curr_shape(shape_matrices[label])
    fig.canvas.draw()

# connect radio buttons to functions
shape_radio.on_clicked(shapes)

#######
# FIN #
#######

plt.show()

