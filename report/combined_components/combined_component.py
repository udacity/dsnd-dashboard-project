from fastcore.xml import FT
from fasthtml.common import Div


class CombinedComponent:

    outer_div_type = Div(cls='container')

    def __call__(self, userid, model):

        called_children = self.call_children(userid, model)
        div_args = self.div_args(userid, model)

        return self.outer_div(called_children, div_args)

    def call_children(self, userid, model):

        called = []
        for child in self.children:
            if isinstance(child, FT):
                called.append(child())

            else:
                called.append(child(userid, model))

        return called

    def div_args(self, userid, model):
        return {}

    def outer_div(self, children, div_args):

        self.outer_div_type.children = ()

        return self.outer_div_type(
            *children,
            **div_args
        )
