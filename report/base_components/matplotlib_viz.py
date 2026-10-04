from .base_component import BaseComponent

import matplotlib.pyplot
from fasthtml.common import Img
import matplotlib.pylab as plt
import matplotlib
import io
import base64

# This is necessary to prevent matplotlib from causing memory leaks
# https://stackoverflow.com/questions/31156578/matplotlib-doesnt-release-memory-after-savefig-and-close
matplotlib.use('Agg')
matplotlib.rcParams['savefig.transparent'] = True
matplotlib.rcParams['savefig.format'] = 'png'


def matplotlib2fasthtml(func):
    '''
    Copy of https://github.com/koaning/fh-matplotlib, which is currently hardcoding the
    image format as jpg. png or svg is needed here.
    '''
    def wrapper(*args, **kwargs):
        # Reset the figure to prevent accumulation. Maybe we need a setting for this?
        fig = plt.figure()

        # Run function as normal
        func(*args, **kwargs)

        # Store it as base64 and put it into an image.
        my_stringIObytes = io.BytesIO()
        plt.savefig(my_stringIObytes)
        my_stringIObytes.seek(0)
        my_base64_jpgData = base64.b64encode(my_stringIObytes.read()).decode()

        # Close the figure to prevent memory leaks
        plt.close(fig)
        plt.close('all')
        return Img(src=f'data:image/jpg;base64, {my_base64_jpgData}')
    return wrapper


class MatplotlibViz(BaseComponent):

    @matplotlib2fasthtml
    def build_component(self, entity_id, model):
        return self.visualization(entity_id, model)

    def visualization(self, entity_id, model):
        pass

    def set_axis_styling(self, ax, bordercolor='white', fontcolor='white'):

        ax.title.set_color(fontcolor)
        ax.xaxis.label.set_color(fontcolor)
        ax.yaxis.label.set_color(fontcolor)

        ax.tick_params(color=bordercolor, labelcolor=fontcolor)
        for spine in ax.spines.values():
            spine.set_edgecolor(bordercolor)

        for line in ax.get_lines():
            line.set_linewidth(4)
            line.set_linestyle('dashdot')
