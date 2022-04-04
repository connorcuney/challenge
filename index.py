from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flasgger import Swagger

# Set up local server
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
swagger = Swagger(app)


# Set up local DB
db = SQLAlchemy(app)


# config route for landing page
@app.route('/')
def index():
    return "Index local server landing page - Go to <a href='http://127.0.0.1:5000/apidocs/#/' >http://127.0.0.1:5000/apidocs/ </a> for docs"

# all vehicles page
@app.route('/vehicles')
def get_all_vehicles():
    """Example endpoint returning a list of all vehicles.
        ---
        definitions:
          Vehicle:
            type: object
            properties:
                Make:
                  type: string
                  example: Honda
                Model:
                  type: string
                  example: Civic
                Year:
                  type: integer
                  example: 2001
                Color:
                  type: string
                  example: Red
                Price:
                  type: number
                  example: 2000
                Miles:
                  type: integer

        responses:
          200:
            description: A bulk list of vehicles
            schema:
              $ref: '#/definitions/Vehicle'
        """

    # query all vehicles
    vehicles = Vehicle.query.all()

    # add data from query to output
    temp = []
    for i in vehicles:
        temp.append({"ID": i.id, "Make": i.make, "Model": i.model, "Year": i.year,
                     "Color": i.color, "Price": i.price, "Miles": i.miles})

    # return output
    return {"List of Vehicles": temp}


# Handling post request on vehicle page
@app.route('/vehicles', methods=['POST'])
def add_vehicle():
    """Example adding a vehicle to DB.
            ---
            parameters:
              - name: make
                type: string
                description: Make of the vehicle
              - name: model
                type: string
                description: Model of the vehicle
              - name: year
                type: integer
                description: Year of the vehicle
              - name: color
                type: string
                description: Color of the vehicle
              - name: price
                type: number
                description: Price of the vehicle
              - name: miles
                type: integer
                description: Mileage of the vehicle
            definitions:
              Vehicle:
                type: object
                properties:
                    id:
                      type: integer
                      example: 1
            responses:
              200:
                description: Returns id of vehicle added
                schema:
                  $ref: '#/definitions/Vehicle'
            """

    # query the post request
    vehicle = Vehicle(make=request.json['make'], model=request.json['model'], year=request.json['year'],
                       color=request.json['color'], price=request.json['price'], miles=request.json['miles'])
    db.session.add(vehicle)
    db.session.commit()
    return {'ID': vehicle.id}


# Handling search by make
@app.route('/searchbymake/<make>')
def get_vehicles_by_make(make):
    """Example searching for make in DB.
                ---
                parameters:
                  - name: make
                    type: string
                    description: Make of the vehicle
                definitions:
                  Vehicle:
                    type: object
                    properties:
                        Make:
                          type: string
                          example: Honda
                        Model:
                          type: string
                          example: Civic
                        Year:
                          type: integer
                          example: 2001
                        Color:
                          type: string
                          example: Red
                        Price:
                          type: number
                          example: 2000
                        Miles:
                          type: integer
                responses:
                  200:
                    description: Returns the vehicle searched for
                    schema:
                      $ref: '#/definitions/Vehicle'
                """

    # get all vehicles that have a like make of request
    vehicles = Vehicle.query.filter(Vehicle.make.like("%" + make + "%")).all()

    # add data from query to output
    temp = []
    for i in vehicles:
        temp.append({"ID": i.id, "Make": i.make, "Model": i.model, "Year": i.year,
                     "Color": i.color, "Price": i.price, "Miles": i.miles})

    # return output
    return {"List of Vehicles with make of " + make + " - Showing all result(s)": temp}


# Handling search by make with pagination
@app.route('/searchbymake/<make>/s=<start>e=<end>')
def get_vehicles_by_make_paginated(make, start, end):
    """Example searching for make in DB.
                    ---
                    parameters:
                      - name: make
                        type: string
                        description: Make of the vehicle
                      - name: start
                        type: integer
                        description: What index to start on
                      - name: end
                        type: integer
                        description: What index to end on
                    definitions:
                      Vehicle:
                        type: object
                        properties:
                            Make:
                              type: string
                              example: Honda
                            Model:
                              type: string
                              example: Civic
                            Year:
                              type: integer
                              example: 2001
                            Color:
                              type: string
                              example: Red
                            Price:
                              type: number
                              example: 2000
                            Miles:
                              type: integer
                    responses:
                      200:
                        description: Returns the vehicle searched for
                        schema:
                          $ref: '#/definitions/Vehicle'
                    """
    # check if search query is numbers
    if start.isdigit() is False or end.isdigit() is False:
        return "Not valid search query parameter input"

    # get all vehicles that have a like make of request
    vehicles = Vehicle.query.filter(Vehicle.make.like("%" + make + "%")).all()

    # add data from query to output with corresponding amount starting at index start and ending at index end
    temp = []
    results = 0
    for i in vehicles[int(start):int(end)]:
        temp.append({"ID": i.id, "Make": i.make, "Model": i.model, "Year": i.year,
                     "Color": i.color, "Price": i.price, "Miles": i.miles})
        results += 1

    # return output
    return {"List of Vehicles with make of " + make + " - Showing " + str(results) + " result(s)": temp}


# Handling search by model
@app.route('/searchbymodel/<model>')
def get_vehicles_by_model(model):
    """Example searching for model in DB.
                    ---
                    parameters:
                      - name: model
                        type: string
                        description: model of the vehicle
                    definitions:
                      Vehicle:
                        type: object
                        properties:
                            Make:
                              type: string
                              example: Honda
                            Model:
                              type: string
                              example: Civic
                            Year:
                              type: integer
                              example: 2001
                            Color:
                              type: string
                              example: Red
                            Price:
                              type: number
                              example: 2000
                            Miles:
                              type: integer
                    responses:
                      200:
                        description: Returns the vehicle searched for
                        schema:
                          $ref: '#/definitions/Vehicle'
                    """

    # get all vehicles that have a like make of request
    vehicles = Vehicle.query.filter(Vehicle.model.like("%" + model + "%")).all()

    # add data from query to output
    temp = []
    for i in vehicles:
        temp.append({"ID": i.id, "Make": i.make, "Model": i.model, "Year": i.year,
                     "Color": i.color, "Price": i.price, "Miles": i.miles})

    # return output
    return {"List of Vehicles with model of " + model + " - Showing all result(s)": temp}


# Handling search by model with pagination
@app.route('/searchbymodel/<model>/s=<start>e=<end>')
def get_vehicles_by_model_paginated(model, start, end):
    """Example searching for model in DB.
                        ---
                        parameters:
                          - name: model
                            type: string
                            description: model of the vehicle
                          - name: start
                            type: integer
                            description: What index to start on
                          - name: end
                            type: integer
                            description: What index to end on
                        definitions:
                          Vehicle:
                            type: object
                            properties:
                                Make:
                                  type: string
                                  example: Honda
                                Model:
                                  type: string
                                  example: Civic
                                Year:
                                  type: integer
                                  example: 2001
                                Color:
                                  type: string
                                  example: Red
                                Price:
                                  type: number
                                  example: 2000
                                Miles:
                                  type: integer
                        responses:
                          200:
                            description: Returns the vehicle searched for
                            schema:
                              $ref: '#/definitions/Vehicle'
                        """
    # check if search query is numbers
    if start.isdigit() is False or end.isdigit() is False:
        return "Not valid search query parameter input"

    # get all vehicles that have a like make of request
    vehicles = Vehicle.query.filter(Vehicle.model.like("%" + model + "%")).all()

    # add data from query to output with corresponding amount starting at index start and ending at index end
    temp = []
    results = 0
    for i in vehicles[int(start):int(end)]:
        temp.append({"ID": i.id, "Make": i.make, "Model": i.model, "Year": i.year,
                     "Color": i.color, "Price": i.price, "Miles": i.miles})
        results += 1

    # return output
    return {"List of Vehicles with model of " + model + " - Showing " + str(results) + " result(s)": temp}


# Handling search by year
@app.route('/searchbyyear/<year>')
def get_vehicles_by_year(year):
    """Example searching for year in DB.
                        ---
                        parameters:
                          - name: year
                            type: string
                            description: year of the vehicle
                        definitions:
                          Vehicle:
                            type: object
                            properties:
                                Make:
                                  type: string
                                  example: Honda
                                Model:
                                  type: string
                                  example: Civic
                                Year:
                                  type: integer
                                  example: 2001
                                Color:
                                  type: string
                                  example: Red
                                Price:
                                  type: number
                                  example: 2000
                                Miles:
                                  type: integer
                        responses:
                          200:
                            description: Returns the vehicle searched for
                            schema:
                              $ref: '#/definitions/Vehicle'
                        """

    # get all vehicles that have a like make of request
    vehicles = Vehicle.query.filter(Vehicle.year.like("%" + year + "%")).all()

    # add data from query to output
    temp = []
    for i in vehicles:
        temp.append({"ID": i.id, "Make": i.make, "Model": i.model, "Year": i.year,
                     "Color": i.color, "Price": i.price, "Miles": i.miles})

    # return output
    return {"List of Vehicles with year of " + year + " - Showing all result(s)": temp}


# Handling search by year with pagination
@app.route('/searchbyyear/<year>/s=<start>e=<end>')
def get_vehicles_by_year_paginated(year, start, end):
    """Example searching for year in DB.
                        ---
                        parameters:
                          - name: year
                            type: string
                            description: year of the vehicle
                          - name: start
                            type: integer
                            description: What index to start on
                          - name: end
                            type: integer
                            description: What index to end on
                        definitions:
                          Vehicle:
                            type: object
                            properties:
                                Make:
                                  type: string
                                  example: Honda
                                Model:
                                  type: string
                                  example: Civic
                                Year:
                                  type: integer
                                  example: 2001
                                Color:
                                  type: string
                                  example: Red
                                Price:
                                  type: number
                                  example: 2000
                                Miles:
                                  type: integer
                        responses:
                          200:
                            description: Returns the vehicle searched for
                            schema:
                              $ref: '#/definitions/Vehicle'
                        """
    # check if search query is numbers
    if start.isdigit() is False or end.isdigit() is False:
        return "Not valid search query parameter input"

    # get all vehicles that have a like make of request
    vehicles = Vehicle.query.filter(Vehicle.year.like("%" + year + "%")).all()

    # add data from query to output with corresponding amount starting at index start and ending at index end
    temp = []
    results = 0
    for i in vehicles[int(start):int(end)]:
        temp.append({"ID": i.id, "Make": i.make, "Model": i.model, "Year": i.year,
                     "Color": i.color, "Price": i.price, "Miles": i.miles})
        results += 1

    # return output
    return {"List of Vehicles with year of " + year + " - Showing " + str(results) + " result(s)": temp}



# Handling search by color
@app.route('/searchbycolor/<color>')
def get_vehicles_by_color(color):
    """Example searching for color in DB.
                    ---
                    parameters:
                      - name: color
                        type: string
                        description: color of the vehicle
                    definitions:
                      Vehicle:
                        type: object
                        properties:
                            Make:
                              type: string
                              example: Honda
                            Model:
                              type: string
                              example: Civic
                            Year:
                              type: integer
                              example: 2001
                            Color:
                              type: string
                              example: Red
                            Price:
                              type: number
                              example: 2000
                            Miles:
                              type: integer
                    responses:
                      200:
                        description: Returns the vehicle searched for
                        schema:
                          $ref: '#/definitions/Vehicle'
                    """

    # get all vehicles that have a like make of request
    vehicles = Vehicle.query.filter(Vehicle.color.like("%" + color + "%")).all()

    # add data from query to output
    temp = []
    for i in vehicles:
        temp.append({"ID": i.id, "Make": i.make, "Model": i.model, "Year": i.year,
                     "Color": i.color, "Price": i.price, "Miles": i.miles})

    # return output
    return {"List of Vehicles with color of " + color + " - Showing all result(s)": temp}


# Handling search by color with pagination
@app.route('/searchbycolor/<color>/s=<start>e=<end>')
def get_vehicles_by_color_paginated(color, start, end):
    """Example searching for color in DB.
                            ---
                            parameters:
                              - name: color
                                type: string
                                description: color of the vehicle
                              - name: start
                                type: integer
                                description: What index to start on
                              - name: end
                                type: integer
                                description: What index to end on
                            definitions:
                              Vehicle:
                                type: object
                                properties:
                                    Make:
                                      type: string
                                      example: Honda
                                    Model:
                                      type: string
                                      example: Civic
                                    Year:
                                      type: integer
                                      example: 2001
                                    Color:
                                      type: string
                                      example: Red
                                    Price:
                                      type: number
                                      example: 2000
                                    Miles:
                                      type: integer
                            responses:
                              200:
                                description: Returns the vehicle searched for
                                schema:
                                  $ref: '#/definitions/Vehicle'
                            """
    # check if search query is numbers
    if start.isdigit() is False or end.isdigit() is False:
        return "Not valid search query parameter input"

    # get all vehicles that have a like make of request
    vehicles = Vehicle.query.filter(Vehicle.color.like("%" + color + "%")).all()

    # add data from query to output with corresponding amount starting at index start and ending at index end
    temp = []
    results = 0
    for i in vehicles[int(start):int(end)]:
        temp.append({"ID": i.id, "Make": i.make, "Model": i.model, "Year": i.year,
                     "Color": i.color, "Price": i.price, "Miles": i.miles})
        results += 1

    # return output
    return {"List of Vehicles with color of " + color + " - Showing " + str(results) + " result(s)": temp}


# Vehicle class for DB
class Vehicle(db.Model):
    # Vehicle properties
    id = db.Column(db.Integer, primary_key=True)
    make = db.Column(db.String(60))
    model = db.Column(db.String(60))
    year = db.Column(db.Integer)
    color = db.Column(db.String(60))
    price = db.Column(db.Float)
    miles = db.Column(db.Integer)

    # represent class as id
    def __repr__(self):
        return f"{self.id}"
