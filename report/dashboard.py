from fasthtml.common import *
import matplotlib.pyplot as plt

from employee_events import QueryBase, Employee, Team

# import the load_model function from the utils.py file
from utils import load_model

"""
Below, we import the parent classes
you will use for subclassing
"""
from base_components import (
    Dropdown,
    BaseComponent,
    Radio,
    MatplotlibViz,
    DataTable
    )

from combined_components import FormGroup, CombinedComponent


# Create a subclass of base_components/dropdown
# called `ReportDropdown`
class ReportDropdown(Dropdown):
       
    # Overwrite the build_component method
    # ensuring it has the same parameters
    # as the Report parent class's method
    def build_component(self, model):
                        
    
        #  Set the `label` attribute so it is set
        #  to the `name` attribute for the model
        self.label = model.name
        
        # Return the output from the
        # parent class's build_component method
        return super().build_component(model)
    
    # Overwrite the `component_data` method
    # Ensure the method uses the same parameters
    # as the parent class method
    def component_data(self, model):
        return model.names()
        # Using the model argument
        # call the employee_events method
        # that returns the user-type's
        # names and ids


# Create a subclass of base_components/BaseComponent
# called `Header`
class Header(BaseComponent):

    # Overwrite the `build_component` method
    # Ensure the method has the same parameters
    # as the parent class
    def build_component(self, model):
        
        # Using the model argument for this method
        # return a fasthtml H1 objects
        # containing the model's name attribute
        return H1(model.name)
          

# Create a subclass of base_components/MatplotlibViz
# called `LineChart`
class LineChart(MatplotlibViz):
    
    # Overwrite the parent class's `visualization`
    # method. Use the same parameters as the parent
    def visualization(self, model, asset_id):
        
        # Pass the `asset_id` argument to
        # the model's `event_counts` method to
        # receive the x (Day) and y (event count)
        df = model.event_counts(asset_id)
        
        # Use the pandas .fillna method to fill nulls with 0
        df = df.fillna(0)
        
        # User the pandas .set_index method to set
        # the date column as the index
        df = df.set_index("event_date")
        
        # Sort the index
        df = df.sort_index()
        
        # Use the .cumsum method to change the data
        # in the dataframe to cumulative counts
        df = df.cumsum()
        
        
        # Set the dataframe columns to the list
        # ['Positive', 'Negative']
        df.columns = ["Positive", "Negative"]
        
        # Initialize a pandas subplot
        # and assign the figure and axis
        # to variables
        fig, ax = plt.subplots()
        
        # call the .plot method for the
        # cumulative counts dataframe
        df.plot(ax=ax)
        
        # pass the axis variable
        # to the `.set_axis_styling`
        # method
        # Use keyword arguments to set 
        # the border color and font color to black. 
        # Reference the base_components/matplotlib_viz file 
        # to inspect the supported keyword arguments
        self.set_axis_styling(ax=ax, border_color="black", font_color="black")
        
        
        # Set title and labels for x and y axis
        ax.set_title("Cumulative Employee Events")
        ax.set_xlabel("Date")
        ax.set_ylabel("Event Count")
        return fig 

# Create a subclass of base_components/MatplotlibViz
# called `BarChart`
class BarChart(MatplotlibViz):

    # Create a `predictor` class attribute
    # assign the attribute to the output
    # of the `load_model` utils function
    predictor = load_model()

    # Overwrite the parent class `visualization` method
    # Use the same parameters as the parent
    def visualization(self, model, asset_id):

        # Using the model and asset_id arguments
        # pass the `asset_id` to the `.model_data` method
        # to receive the data that can be passed to the machine
        # learning model
        data = model.model_data(asset_id)
        
        # Using the predictor class attribute
        # pass the data to the `predict_proba` method
        pred_proba = self.predictor.predict_proba(data)

        # Index the second column of predict_proba output
        # The shape should be (<number of records>, 1)
        pred_proba = pred_proba[:, 1].reshape(-1, 1)        
        
        # Below, create a `pred` variable set to
        # the number we want to visualize
        #
        # If the model's name attribute is "team"
        # We want to visualize the mean of the predict_proba output
        if model.name == "team":
            pred = pred_proba.mean()
            
        # Otherwise set `pred` to the first value
        # of the predict_proba output
        else:
            pred = pred_proba[0][0]
      
        # Initialize a matplotlib subplot
        fig, ax = plt.subplots()
        
        # Run the following code unchanged
        ax.barh([''], [pred])
        ax.set_xlim(0, 1)
        ax.set_title('Predicted Recruitment Risk', fontsize=20)
        
        # pass the axis variable
        # to the `.set_axis_styling`
        # method
        self.set_axis_styling(ax=ax, border_color="black", font_color="black")

        return fig
 
# Create a subclass of combined_components/CombinedComponent
# called Visualizations       
class Visualizations(CombinedComponent):

    # Set the `children`
    # class attribute to a list
    # containing an initialized
    # instance of `LineChart` and `BarChart`
    children = [LineChart(), BarChart()]

    # Leave this line unchanged
    outer_div_type = Div(cls='grid')
            
# Create a subclass of base_components/DataTable
# called `NotesTable`
class NotesTable(DataTable):

    # Overwrite the `component_data` method
    # using the same parameters as the parent class
    def component_data(self, model, entity_id):
        
        # Using the model and entity_id arguments
        # pass the entity_id to the model's .notes 
        # method. Return the output
        return model.notes(entity_id)
    

class DashboardFilters(FormGroup):

    id = "top-filters"
    action = "/update_data"
    method="POST"

    children = [
        Radio(
            values=["Employee", "Team"],
            name='profile_type',
            hx_get='/update_dropdown',
            hx_target='#selector'
            ),
        ReportDropdown(
            id="selector",
            name="user-selection")
        ]
    
# Create a subclass of CombinedComponents
# called `Report`
class Report(CombinedComponent):


    # Set the `children`
    # class attribute to a list
    # containing initialized instances 
    # of the header, dashboard filters,
    # data visualizations, and notes table
    children = [Header(), ReportDropdown(), Visualizations(), NotesTable()]

# Initialize a fasthtml app 
app = FastHTML()

# Initialize the `Report` class
report = Report()


# Create a route for a get request
# Set the route's path to the root
@app.get("/")

    # Call the initialized report
    # pass the integer 1 and an instance
    # of the Employee class as arguments
    # Return the result
def index():
    return report(1, Employee())

# Create a route for a get request
# Set the route's path to receive a request
# for an employee ID so `/employee/2`
# will return the page for the employee with
# an ID of `2`. 
# parameterize the employee ID 
# to a string datatype
@app.get("/employee/{id:str}")

    # Call the initialized report
    # pass the ID and an instance
    # of the Employee SQL class as arguments
    # Return the result
def employee(id: str):
    return report(id, Employee())


# Create a route for a get request
# Set the route's path to receive a request
# for a team ID so `/team/2`
# will return the page for the team with
# an ID of `2`. 
# parameterize the team ID 
# to a string datatype
@app.get("/team/{id:str}")

    # Call the initialized report
    # pass the id and an instance
    # of the Team SQL class as arguments
    # Return the result
def team(id: str):
    return report(id, Team())


# Keep the below code unchanged!
@app.get('/update_dropdown{r}')
def update_dropdown(r):
    dropdown = DashboardFilters.children[1]
    print('PARAM', r.query_params['profile_type'])
    if r.query_params['profile_type'] == 'Team':
        return dropdown(None, Team())
    elif r.query_params['profile_type'] == 'Employee':
        return dropdown(None, Employee())


@app.post('/update_data')
async def update_data(r):
    from fasthtml.common import RedirectResponse
    data = await r.form()
    profile_type = data._dict['profile_type']
    id = data._dict['user-selection']
    if profile_type == 'Employee':
        return RedirectResponse(f"/employee/{id}", status_code=303)
    elif profile_type == 'Team':
        return RedirectResponse(f"/team/{id}", status_code=303)
    


serve()
