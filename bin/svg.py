# SVG (Cell Plot) Tab
import os
from ipywidgets import Layout, Label, Text, Checkbox, Button, HBox, VBox, Box, \
    FloatText, BoundedIntText, BoundedFloatText, HTMLMath, Dropdown, interactive, Output
from collections import deque
import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
#from matplotlib.patches import Circle, Ellipse, Rectangle
from matplotlib.patches import Circle
from matplotlib.collections import PatchCollection
import matplotlib.colors as mplc
import numpy as np
import zipfile
import glob
import platform
# from debug import debug_view

hublib_flag = True
if platform.system() != 'Windows':
    try:
#        print("Trying to import hublib.ui")
        from hublib.ui import Download
    except:
        hublib_flag = False
else:
    hublib_flag = False


class SVGTab(object):

    def __init__(self):
        # tab_height = '520px'
        # tab_layout = Layout(width='900px',   # border='2px solid black',
        #                     height=tab_height, overflow_y='scroll')

        self.output_dir = '.'

        constWidth = '180px'

#        self.fig = plt.figure(figsize=(6, 6))
        # self.fig = plt.figure(figsize=(7, 7))

        max_frames = 1
        self.svg_plot = interactive(self.plot_svg, frame=(0, max_frames), continuous_update=False)

# https://ipywidgets.readthedocs.io/en/latest/examples/Widget%20List.html#Play-(Animation)-widget
        # play = widgets.Play(
        # #     interval=10,
        #     value=50,
        #     min=0,
        #     max=100,
        #     step=1,
        #     description="Press play",
        #     disabled=False
        # )
        # slider = widgets.IntSlider()
        # widgets.jslink((play, 'value'), (slider, 'value'))
        # widgets.HBox([play, slider])

        # "plot_size" controls the size of the tab height, not the plot (rf. figsize for that)
        plot_size = '500px'  # small: 
        plot_size = '750px'  # medium
        plot_size = '700px'  # medium
        plot_size = '600px'  # medium
        self.svg_plot.layout.width = plot_size
        self.svg_plot.layout.height = plot_size
        self.use_defaults = True
        self.show_nucleus = 1  # 0->False, 1->True in Checkbox!
        self.show_edge = 1  # 0->False, 1->True in Checkbox!
        self.show_tracks = 1  # 0->False, 1->True in Checkbox!
        self.trackd = {}  # dictionary to hold cell IDs and their tracks: (x,y) pairs
        # self.scale_radius = 1.0
        self.axes_min = 0.0
        self.axes_max = 2000   # hmm, this can change (TODO?)

        self.max_frames = BoundedIntText(
            min=0, max=99999, value=max_frames,
            description='Max',
            layout=Layout(width='160px'),
#            layout=Layout(flex='1 1 auto', width='auto'),  #Layout(width='160px'),
        )
        self.max_frames.observe(self.update_max_frames)

        self.show_nucleus_checkbox= Checkbox(
            description='nucleus', value=True, disabled=False,
            layout=Layout(width=constWidth),
#            layout=Layout(flex='1 1 auto', width='auto'),  #Layout(width='160px'),
        )
        self.show_nucleus_checkbox.observe(self.show_nucleus_cb)

        self.show_edge_checkbox= Checkbox(
            description='edge', value=True, disabled=False,
            layout=Layout(width=constWidth),
#            layout=Layout(flex='1 1 auto', width='auto'),  #Layout(width='160px'),
        )
        self.show_edge_checkbox.observe(self.show_edge_cb)

        self.show_tracks_checkbox= Checkbox(
            description='tracks', value=True, disabled=False,
            layout=Layout(width=constWidth),
#            layout=Layout(flex='1 1 auto', width='auto'),  #Layout(width='160px'),
        )
        self.show_tracks_checkbox.observe(self.show_tracks_cb)

#        row1 = HBox([Label('(select slider: drag or left/right arrows)'), 
#            self.max_frames, VBox([self.show_nucleus_checkbox, self.show_edge_checkbox])])
#            self.max_frames, self.show_nucleus_checkbox], layout=Layout(width='500px'))

#        self.tab = VBox([row1,self.svg_plot], layout=tab_layout)

        items_auto = [Label('select slider: drag or left/right arrows'), 
            self.max_frames, 
            self.show_nucleus_checkbox,  
            self.show_edge_checkbox, 
            self.show_tracks_checkbox, 
         ]
#row1 = HBox([Label('(select slider: drag or left/right arrows)'), 
#            max_frames, show_nucleus_checkbox, show_edge_checkbox], 
#            layout=Layout(width='800px'))
        box_layout = Layout(display='flex',
                    flex_flow='row',
                    align_items='stretch',
                    width='70%')
        row1 = Box(children=items_auto, layout=box_layout)

        if (hublib_flag):
            self.download_button = Download('svg.zip', style='warning', icon='cloud-download', 
                                            tooltip='You need to allow pop-ups in your browser', cb=self.download_cb)
            download_row = HBox([self.download_button.w, Label("Download all cell plots (browser must allow pop-ups).")])
    #        self.tab = VBox([row1, self.svg_plot, self.download_button.w], layout=tab_layout)
    #        self.tab = VBox([row1, self.svg_plot, self.download_button.w])
            self.tab = VBox([row1, self.svg_plot, download_row])
        else:
            self.tab = VBox([row1, self.svg_plot])


    # def update(self, rdir=''):
    def update(self, rdir=''):
        # with debug_view:
        #     print("SVG: update rdir=", rdir)        

        if rdir:
            self.output_dir = rdir

        all_files = sorted(glob.glob(os.path.join(self.output_dir, 'snapshot*.svg')))
        if len(all_files) > 0:
            last_file = all_files[-1]
            # Note! the following will trigger: self.max_frames.observe(self.update_max_frames)
            self.max_frames.value = int(last_file[-12:-4])  # assumes naming scheme: "snapshot%08d.svg"

        # with debug_view:
        #     print("SVG: added %s files" % len(all_files))


    def download_cb(self):
        file_str = os.path.join(self.output_dir, '*.svg')
        # print('zip up all ',file_str)
        with zipfile.ZipFile('svg.zip', 'w') as myzip:
            for f in glob.glob(file_str):
                myzip.write(f, os.path.basename(f))   # 2nd arg avoids full filename path in the archive

    def show_nucleus_cb(self, b):
        global current_frame
        if (self.show_nucleus_checkbox.value):
            self.show_nucleus = 1
        else:
            self.show_nucleus = 0
#        self.plot_svg(self,current_frame)
        self.svg_plot.update()

    def show_edge_cb(self, b):
        if (self.show_edge_checkbox.value):
            self.show_edge = 1
        else:
            self.show_edge = 0
        self.svg_plot.update()

    def show_tracks_cb(self, b):
        if (self.show_tracks_checkbox.value):
            self.show_tracks = 1
        else:
            self.show_tracks = 0
        # print('--- show_tracks_cb: calling svg_plot.update()')
        # if (not self.show_tracks):
        #     self.svg_plot.update()
        # else:
        if (self.show_tracks):
            self.create_all_tracks()
        self.svg_plot.update()


    # Note! this is called for EACH change to "Max" frames, which is with every new .svg file created!
    def update_max_frames(self,_b): 
        self.svg_plot.children[0].max = self.max_frames.value
        # if (self.show_tracks):
        #     print('--- update_max_frames: calling create_all_tracks')
        #     self.create_all_tracks()

    #-----------------------------------------------------
    def circles(self, x, y, s, c='b', vmin=None, vmax=None, **kwargs):
        """
        See https://gist.github.com/syrte/592a062c562cd2a98a83 

        Make a scatter plot of circles. 
        Similar to plt.scatter, but the size of circles are in data scale.
        Parameters
        ----------
        x, y : scalar or array_like, shape (n, )
            Input data
        s : scalar or array_like, shape (n, ) 
            Radius of circles.
        c : color or sequence of color, optional, default : 'b'
            `c` can be a single color format string, or a sequence of color
            specifications of length `N`, or a sequence of `N` numbers to be
            mapped to colors using the `cmap` and `norm` specified via kwargs.
            Note that `c` should not be a single numeric RGB or RGBA sequence 
            because that is indistinguishable from an array of values
            to be colormapped. (If you insist, use `color` instead.)  
            `c` can be a 2-D array in which the rows are RGB or RGBA, however. 
        vmin, vmax : scalar, optional, default: None
            `vmin` and `vmax` are used in conjunction with `norm` to normalize
            luminance data.  If either are `None`, the min and max of the
            color array is used.
        kwargs : `~matplotlib.collections.Collection` properties
            Eg. alpha, edgecolor(ec), facecolor(fc), linewidth(lw), linestyle(ls), 
            norm, cmap, transform, etc.
        Returns
        -------
        paths : `~matplotlib.collections.PathCollection`
        Examples
        --------
        a = np.arange(11)
        circles(a, a, s=a*0.2, c=a, alpha=0.5, ec='none')
        plt.colorbar()
        License
        --------
        This code is under [The BSD 3-Clause License]
        (http://opensource.org/licenses/BSD-3-Clause)
        """

        if np.isscalar(c):
            kwargs.setdefault('color', c)
            c = None

        if 'fc' in kwargs:
            kwargs.setdefault('facecolor', kwargs.pop('fc'))
        if 'ec' in kwargs:
            kwargs.setdefault('edgecolor', kwargs.pop('ec'))
        if 'ls' in kwargs:
            kwargs.setdefault('linestyle', kwargs.pop('ls'))
        if 'lw' in kwargs:
            kwargs.setdefault('linewidth', kwargs.pop('lw'))
        # You can set `facecolor` with an array for each patch,
        # while you can only set `facecolors` with a value for all.

        zipped = np.broadcast(x, y, s)
        patches = [Circle((x_, y_), s_)
                for x_, y_, s_ in zipped]
        collection = PatchCollection(patches, **kwargs)
        if c is not None:
            c = np.broadcast_to(c, zipped.shape).ravel()
            collection.set_array(c)
            collection.set_clim(vmin, vmax)

        ax = plt.gca()
        ax.add_collection(collection)
        ax.autoscale_view()
        # plt.draw_if_interactive()
        if c is not None:
            plt.sci(collection)
        # return collection

    #-------------------------
    def create_all_tracks(self, rdir=''):
        if rdir:
            print('create_all_tracks():  rdir=',rdir)
            self.output_dir = rdir

        # current_frame = frame
        # check: if 0th .svg snapshot file doesn't exist, exit
        fname = "snapshot%08d.svg" % 0  # assume [0:max] snapshots exist
        full_fname = os.path.join(self.output_dir, fname)
        if not os.path.isfile(full_fname):
            print('create_all_tracks():  0th svg missing, return')
            return

        self.trackd.clear()
        # print("----- create_all_tracks") 
        for frame in range(self.max_frames.value):
            fname = "snapshot%08d.svg" % frame  # assume [0:max] snapshots exist
            full_fname = os.path.join(self.output_dir, fname)
            # with debug_view:
            #     print("plot_svg:", full_fname) 
            # if not os.path.isfile(full_fname):
            #     print("Once output files are generated, click the slider.")   
            #     return

            #  print('\n---- ' + fname + ':')
            tree = ET.parse(full_fname)
            root = tree.getroot()
            numChildren = 0
            for child in root:
                if ('id' in child.attrib.keys()):
                    # print('-------- found tissue!!')
                    tissue_parent = child
                    break

            # print('------ search tissue')
            cells_parent = None

            for child in tissue_parent:
                # print('attrib=',child.attrib)
                if (child.attrib['id'] == 'cells'):
                    # print('-------- found cells, setting cells_parent')
                    cells_parent = child
                    break
                numChildren += 1

            num_cells = 0
            for child in cells_parent:
                for circle in child:  # two circles in each child: outer + nucleus
                    #  circle.attrib={'cx': '1085.59','cy': '1225.24','fill': 'rgb(159,159,96)','r': '6.67717','stroke': 'rgb(159,159,96)','stroke-width': '0.5'}
                    #      print('  --- cx,cy=',circle.attrib['cx'],circle.attrib['cy'])
                    xval = float(circle.attrib['cx'])

                    # test for bogus x,y locations (rwh TODO: use max of domain?)
                    too_large_val = 10000.
                    if (np.fabs(xval) > too_large_val):
                        print("bogus xval=", xval)
                        break
                    yval = float(circle.attrib['cy'])
                    if (np.fabs(yval) > too_large_val):
                        print("bogus xval=", xval)
                        break

                    # if this cell ID (and x,y) is not yet in our trackd dict, add it
                    if (child.attrib['id'] in self.trackd.keys()):
                        self.trackd[child.attrib['id']] = np.vstack((self.trackd[child.attrib['id']], [ xval, yval ]))
                    else:
                        self.trackd[child.attrib['id']] = np.array( [ xval, yval ])

                    # xlist.append(xval)
                    # ylist.append(yval)

                    # if (self.show_nucleus == 0):
                    break  # we don't care about the 2nd circle (nucleus)

                num_cells += 1

                # if num_cells > 3:   # for debugging
                #   print(fname,':  num_cells= ',num_cells," --- debug exit.")
                #   sys.exit(1)
                #   break

                # print(fname,':  num_cells= ',num_cells)

            # xvals = np.array(xlist)
            # yvals = np.array(ylist)

        # print('-- self.trackd=',self.trackd)
        # if (self.show_tracks):
        #     # print('len(trackd.keys()) = ',len(trackd.keys()))
        #     print('self.trackd= ',self.trackd)
        #     for key in self.trackd.keys():
        #         if (len(self.trackd[key].shape) == 2):
        #             print('plotting tracks')
        #             xtracks = self.trackd[key][:,0]
        #             ytracks = self.trackd[key][:,1]
        #             plt.plot(xtracks,ytracks)

    #-------------------------
    # def plot_svg(self, frame, rdel=''):
    def plot_svg(self, frame):
        # global current_idx, axes_max
        global current_frame
        current_frame = frame
        fname = "snapshot%08d.svg" % frame
        full_fname = os.path.join(self.output_dir, fname)
        # with debug_view:
            # print("plot_svg:", full_fname) 
        # print("-- plot_svg:", full_fname) 
        if not os.path.isfile(full_fname):
            print("Once output files are generated, click the slider.")   
            return

        xlist = deque()
        ylist = deque()
        rlist = deque()
        rgb_list = deque()

        #  print('\n---- ' + fname + ':')
#        tree = ET.parse(fname)
        tree = ET.parse(full_fname)
        root = tree.getroot()
        #  print('--- root.tag ---')
        #  print(root.tag)
        #  print('--- root.attrib ---')
        #  print(root.attrib)
        #  print('--- child.tag, child.attrib ---')
        numChildren = 0
        for child in root:
            #    print(child.tag, child.attrib)
            #    print("keys=",child.attrib.keys())
            if self.use_defaults and ('width' in child.attrib.keys()):
                self.axes_max = float(child.attrib['width'])
                # print("debug> found width --> axes_max =", axes_max)
            if child.text and "Current time" in child.text:
                svals = child.text.split()
                # title_str = "(" + str(current_idx) + ") Current time: " + svals[2] + "d, " + svals[4] + "h, " + svals[7] + "m"
                # title_str = "Current time: " + svals[2] + "d, " + svals[4] + "h, " + svals[7] + "m"
                title_str = svals[2] + "d, " + svals[4] + "h, " + svals[7] + "m"

            # print("width ",child.attrib['width'])
            # print('attrib=',child.attrib)
            # if (child.attrib['id'] == 'tissue'):
            if ('id' in child.attrib.keys()):
                # print('-------- found tissue!!')
                tissue_parent = child
                break

        # print('------ search tissue')
        cells_parent = None

        for child in tissue_parent:
            # print('attrib=',child.attrib)
            if (child.attrib['id'] == 'cells'):
                # print('-------- found cells, setting cells_parent')
                cells_parent = child
                break
            numChildren += 1

        num_cells = 0
        #  print('------ search cells')
        for child in cells_parent:
            #    print(child.tag, child.attrib)
            #    print('attrib=',child.attrib)
            for circle in child:  # two circles in each child: outer + nucleus
                #  circle.attrib={'cx': '1085.59','cy': '1225.24','fill': 'rgb(159,159,96)','r': '6.67717','stroke': 'rgb(159,159,96)','stroke-width': '0.5'}
                #      print('  --- cx,cy=',circle.attrib['cx'],circle.attrib['cy'])
                xval = float(circle.attrib['cx'])

                s = circle.attrib['fill']
                # print("s=",s)
                # print("type(s)=",type(s))
                if (s[0:3] == "rgb"):  # if an rgb string, e.g. "rgb(175,175,80)" 
                    rgb = list(map(int, s[4:-1].split(",")))  
                    rgb[:] = [x / 255. for x in rgb]
                else:     # otherwise, must be a color name
                    rgb_tuple = mplc.to_rgb(mplc.cnames[s])  # a tuple
                    rgb = [x for x in rgb_tuple]

                # test for bogus x,y locations (rwh TODO: use max of domain?)
                too_large_val = 10000.
                if (np.fabs(xval) > too_large_val):
                    print("bogus xval=", xval)
                    break
                yval = float(circle.attrib['cy'])
                if (np.fabs(yval) > too_large_val):
                    print("bogus xval=", xval)
                    break

                rval = float(circle.attrib['r'])
                # if (rgb[0] > rgb[1]):
                #     print(num_cells,rgb, rval)
                xlist.append(xval)
                ylist.append(yval)
                rlist.append(rval)
                rgb_list.append(rgb)

                # For .svg files with cells that *have* a nucleus, there will be a 2nd
                if (self.show_nucleus == 0):
                #if (not self.show_nucleus):
                    break

            num_cells += 1

            # if num_cells > 3:   # for debugging
            #   print(fname,':  num_cells= ',num_cells," --- debug exit.")
            #   sys.exit(1)
            #   break

            # print(fname,':  num_cells= ',num_cells)

        xvals = np.array(xlist)
        yvals = np.array(ylist)
        rvals = np.array(rlist)
        rgbs = np.array(rgb_list)
        # print("xvals[0:5]=",xvals[0:5])
        # print("rvals[0:5]=",rvals[0:5])
        # print("rvals.min, max=",rvals.min(),rvals.max())

        # rwh - is this where I change size of render window?? (YES - yipeee!)
        #   plt.figure(figsize=(6, 6))
        #   plt.cla()
        title_str += " (" + str(num_cells) + " agents)"
        #   plt.title(title_str)
        #   plt.xlim(axes_min,axes_max)
        #   plt.ylim(axes_min,axes_max)
        #   plt.scatter(xvals,yvals, s=rvals*scale_radius, c=rgbs)

        # TODO: make figsize a function of plot_size? What about non-square plots?
        # self.fig = plt.figure(figsize=(9, 9))
        # self.fig = plt.figure(figsize=(18, 18))
        # self.fig = plt.figure(figsize=(15, 15))  # 
        self.fig = plt.figure(figsize=(9, 9))  # 

#        axx = plt.axes([0, 0.05, 0.9, 0.9])  # left, bottom, width, height
#        axx = fig.gca()
#        print('fig.dpi=',fig.dpi) # = 72

        #   im = ax.imshow(f.reshape(100,100), interpolation='nearest', cmap=cmap, extent=[0,20, 0,20])
        #   ax.xlim(axes_min,axes_max)
        #   ax.ylim(axes_min,axes_max)

        # convert radii to radii in pixels
        # ax2 = self.fig.gca()
        # N = len(xvals)
        # rr_pix = (ax2.transData.transform(np.vstack([rvals, rvals]).T) -
        #             ax2.transData.transform(np.vstack([np.zeros(N), np.zeros(N)]).T))
        # rpix, _ = rr_pix.T

        # markers_size = (144. * rpix / self.fig.dpi)**2   # = (2*rpix / fig.dpi * 72)**2
        # markers_size = markers_size/4000000.
        # print('max=',markers_size.max())

        #rwh - temp fix - Ah, error only occurs when "edges" is toggled on
        if (self.show_edge):
            try:
                # plt.scatter(xvals,yvals, s=markers_size, c=rgbs, edgecolor='black', linewidth=0.5)
                self.circles(xvals,yvals, s=rvals, color=rgbs, edgecolor='black', linewidth=0.5)
                # cell_circles = self.circles(xvals,yvals, s=rvals, color=rgbs, edgecolor='black', linewidth=0.5)
                # plt.sci(cell_circles)
            except (ValueError):
                pass
        else:
            # plt.scatter(xvals,yvals, s=markers_size, c=rgbs)
            self.circles(xvals,yvals, s=rvals, color=rgbs)

        if (self.show_tracks):
            for key in self.trackd.keys():
                xtracks = self.trackd[key][:,0]
                ytracks = self.trackd[key][:,1]
                plt.plot(xtracks[0:frame],ytracks[0:frame],  linewidth=5)

        plt.xlim(self.axes_min, self.axes_max)
        plt.ylim(self.axes_min, self.axes_max)
        #   ax.grid(False)
#        axx.set_title(title_str)
        plt.title(title_str)

# video-style widget - perhaps for future use
# svg_play = widgets.Play(
#     interval=1,
#     value=50,
#     min=0,
#     max=100,
#     step=1,
#     description="Press play",
#     disabled=False,
# )
# def svg_slider_change(change):
#     print('svg_slider_change: type(change)=',type(change),change.new)
#     plot_svg(change.new)
    
#svg_play
# svg_slider = widgets.IntSlider()
# svg_slider.observe(svg_slider_change, names='value')

# widgets.jslink((svg_play, 'value'), (svg_slider,'value')) #  (svg_slider, 'value'), (plot_svg, 'value'))

# svg_slider = widgets.IntSlider()
# widgets.jslink((play, 'value'), (slider, 'value'))
# widgets.HBox([svg_play, svg_slider])

# Using the following generates a new mpl plot; it doesn't use the existing plot!
#svg_anim = widgets.HBox([svg_play, svg_slider])

#svg_tab = widgets.VBox([svg_dir, svg_plot, svg_anim], layout=tab_layout)

#svg_tab = widgets.VBox([svg_dir, svg_anim], layout=tab_layout)
#---------------------
