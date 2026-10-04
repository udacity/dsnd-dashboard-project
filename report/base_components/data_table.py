from .base_component import BaseComponent
from fasthtml.common import Table, Tr, Th, Td


class DataTable(BaseComponent):

    def build_component(self, entity_id, model):

        if model.name:

            data = self.component_data(entity_id, model)

            table = Table(
                Tr(
                    Th(column) for column in data.columns
                )
            )

            for data_row in data.to_numpy():

                table_row = Tr(
                    Td(val) for val in data_row
                )

                children = (*table.children, table_row)
                table.children = children

            return table
