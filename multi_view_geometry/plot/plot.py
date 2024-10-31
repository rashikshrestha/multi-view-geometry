import numpy as np
import plotly.graph_objects as go
from ..conversion import q2R

def toy_intrinsics():
    return {'w':6, 'h':4, 'fx':10, 'fy':10, 'cx': 3, 'cy': 2}

def get_identity_cam(scale=1, cam_orientation=(1,1,1), params=toy_intrinsics()):
    """
    Gets an identity camera plot

    Parameters
    ----------
    scale: int
        Scale of the camera plot

    Returns
    -------
    cam_plot: np.ndarray
        (11, 3) Sequence of points to make camera plot
    axis: np.ndarray
        (4,3) Axis points of camera
    params: dict
        Camera intirisic parameters
    """
    f = params['fx']
    w = params['w']/2
    h = params['h']/2

    cam_orientation = np.array(cam_orientation)
    unit_cam = np.array([
        [0,0,0],
        [w,-h,f],
        [w,h,f],
        [-w,h,f],
        [-w,-h,f],
        [0,-2*h,f]
    ])
    unit_cam *= cam_orientation

    seq = np.array([3,4,1,2,0,1,5,4,0,3,2])
    draw_cam = unit_cam[seq]

    axis = np.array([
        [0,0,0],
        [3,0,0],
        [0,3,0],
        [0,0,3]
    ])

    return draw_cam*scale, axis*scale


def get_cam_plot(qvec, tvec, unit_cam, axis):
    """
    Gets camera plot, pose defined by given quaternion and translation

    Parameters
    ----------
    qvec: np.ndarray
        (4,) Quaternion of Camera Pose
    tvec: np.ndarray
        (3,) Translation of Camera Pose
    unit_cam: np.ndarray
        (11,3) Ideal camera sequence

    Returns
    -------
    cam: np.ndarray
        (11,3) Sequence of corrdinates to draw given camera pose
    axis: np.ndarray
        (4,3) Axis points of camera
    """
    R = q2R(qvec)
    rotated_cam = (R@unit_cam.T + tvec.reshape(3,1)).T
    rotated_axis = (R@axis.T + tvec.reshape(3,1)).T
    return rotated_cam, rotated_axis


def plot_cam_poses(poses: np.ndarray,  ax, cam_orientation=(1,1,1), scale=0.02, 
                   alpha=1, color=None, linestyle='-' , linewidth=1,
                   plot_axis=False, axis_alpha=1):
    """
    Plot Camera Poses and Camera Axis (optional)

    Parameters
    ----------
    poses: np.ndarray
        (N,7) Camera Poses
    ax: matplotlib.axes
        Matplot axes where poses are drawn

    Returns
    -------
    None
    """
    identity_cam, identity_axis = get_identity_cam(scale, cam_orientation)
    for pos in poses:
        cam, axis = get_cam_plot(pos[:4], pos[4:], identity_cam, identity_axis)
        if color is None:
            ax.plot(cam[:,0], cam[:,1], cam[:,2], alpha=alpha, linestyle=linestyle, linewidth=linewidth)
        else:
            ax.plot(cam[:,0], cam[:,1], cam[:,2], alpha=alpha, color=color, linestyle=linestyle, linewidth=linewidth)

        if plot_axis:
            axis_idx = np.array([[0,1], [0,2], [0,3]]).astype(int)
            colors = ('red', 'green', 'blue')
            for idx, clr in zip(axis_idx, colors):
                ax.plot(axis[idx,0], axis[idx,1], axis[idx,2], alpha=axis_alpha, color=clr, linewidth=1)


def plotly_single_cam(cam, cam_name=None, color='black'):
    """
    Get Plotly Camera plot for one camera

    Parameters
    ----------
    cam: np.ndarray
        (11,3) Sequence of corrdinates to draw given camera pose

    Returns
    -------
    cam_plot: go.Scatt3d
        Camera Plot
    """
    cam_plot_complete = []

    cam_plot = go.Scatter3d(
        x=cam[:,0],
        y=cam[:,1],
        z=cam[:,2],
        mode='lines',
        marker=dict(
            size=2,
            opacity=1
        ),
        line=dict(
            width=7,
            color=color
        ),
        showlegend=False,
    )
    cam_plot_complete.append(cam_plot)

    if cam_name is not None:
        cam_name_plot = go.Scatter3d(
            x=cam[4,0][None],
            y=cam[4,1][None],
            z=cam[4,2][None],
            mode='text',
            marker=dict(
                size=2,
                opacity=1
            ),
            showlegend=False,
            text=cam_name
        )
        cam_plot_complete.append(cam_name_plot)

    return cam_plot_complete


def plotly_cam_poses(poses: np.ndarray, cam_orientation=(1,1,1), scale=0.02, 
                     params=toy_intrinsics(),
                     alpha=1, color=None, linestyle='-' , linewidth=1,
                     plot_axis=False, axis_alpha=1):
    """
    Plot Camera Poses and Camera Axis (optional)

    Parameters
    ----------
    poses: np.ndarray
        (N,7) Camera Poses

    Returns
    -------
    all_cams_plot: go.Scatter3d
        List of Plotly graph object Scatter Plot
    """
    
    identity_cam, identity_axis = get_identity_cam(scale, cam_orientation, params)
    all_cams_plot = []
    for count, pos in enumerate(poses):
        cam, axis = get_cam_plot(pos[:4], pos[4:], identity_cam, identity_axis)
        if color is None:
            all_cams_plot += plotly_single_cam(cam, cam_name=str(count))
        else:
            all_cams_plot += plotly_single_cam(cam, cam_name=str(count), color=color)

    #TODO axis plot

    return all_cams_plot