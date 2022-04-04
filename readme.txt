How to run
---------------------------------------------------
1. Run "pip install flask", "pip install flask_sqlalchemy", and "pip install flasgger" 
   I have included the dependencies in this repos
2. If on WINDOWS run: "set FLASK_APP=index.py" and "set FLASK_ENV=development"
   If on *nix run: "export FLASK_APP=index.py" and "export FLASK_ENV=development"
3. Run: "python -m flask run"
(may have to "pip install -r requirements.txt" if doesnt run after step 3)

API is now able to take GET and Post Requests

Examples:
    GET all vehicles
    - curl "http://127.0.0.1:5000/vehicles"

    POST add a vehicle
    - curl --location --request POST "http://127.0.0.1:5000/vehicles" --header "Content-Type: application/json" --data-raw "{\"make\": \"Toyata\", \"model\": \"Avalon\", \"year\": 2021,\"color\": \"White\", \"price\": 17000, \"miles\": 0}"

    GET by search request
    - curl "http://127.0.0.1:5000/searchbymake/Toyata"
    - curl "http://127.0.0.1:5000/searchbymodel/Prius"
    - curl "http://127.0.0.1:5000/searchbyyear/2020"
    - curl "http://127.0.0.1:5000/searchbycolor/Red"

    GET by search request with pagination
    - curl "http://127.0.0.1:5000/searchbymake/Toyata/s=0e=1"
    - curl "http://127.0.0.1:5000/searchbymodel/Prius/s=0e=1"
    - curl "http://127.0.0.1:5000/searchbyyear/2020/s=0e=1"
    - curl "http://127.0.0.1:5000/searchbycolor/Red/s=0e=1"
