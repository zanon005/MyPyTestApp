# if you get erros importing modules try this solution, create 'conftest.py' at you apps folder
# https://stackoverflow.com/questions/10253826/path-issue-with-pytest-importerror-no-module-named-yadayadayada
# Great tutorial on python testing
# https://semaphoreci.com/community/tutorials/testing-python-applications-with-pytest
# Great video tutorial 
# https://www.youtube.com/watch?v=LX2ksGYXJ80

import pytest
import pandas as pd
from app import app
from pathlib import Path

#Marks this function as a fixture
@pytest.fixture
def load_test_data():
    """
    Fixture to load custom city distances test data
    """
    # path current file, get this files parent, go back one directory, find 'test_data' folder
    example_data_path = Path(__file__).resolve().parent / '..' /'test_data'
    data_path = example_data_path / 'test_city_distances.csv'
    data = pd.read_csv(data_path, delimiter= ";")
    data.set_index(data.columns,inplace= True)
    return data

#
#   Example Starter Test
#
def test_title_case():
    # Setup
    in_string = "this is my test string"
    desired = "This Is My Test String"

    # Exercise
    actual = in_string.title()

    # Verify
    assert actual == desired

    # Cleanup
    # none necessary

def test_valid_user_input_for_config_cost_km(monkeypatch, load_test_data):
    # Setup
    # monkeypatch the "input" function, so that it returns  10.
    # This simulates the user entering  10  in the terminal:
    monkeypatch.setattr('builtins.input', lambda _: 10)
    desired = 10 #desired output for the actual output
    my_app = app.App(load_test_data)

    # Exercise
    #sets the value of 'cost_per_km' in app class to the monkeypatch value of 10
    my_app.config_cost_km() # Consume input from monkeypatch
    actual = my_app.cost_per_km

    # Verify
    #assert that the valid user input was stored in the class
    assert actual == desired

    # Cleanup
    #my_app.cost_per_km = None # reset value of cost_per_km

def test_invalid_user_input_for_config_cost_km(monkeypatch, load_test_data):
    # Setup
    # monkeypatch the "input" function, so that it returns  -1.
    # This simulates the user entering  -1  in the terminal:
    monkeypatch.setattr('builtins.input', lambda _: -1)
    my_app = app.App(load_test_data)

    # Exercise
    my_app.config_cost_km() # Consume input from monkeypatch

    # Verify
    #assert that the invalid user input was not stored  in the class
    assert my_app.cost_per_km == None

    # Cleanup
    # none necessary

def test_dist_CityA_CityB(load_test_data):
    # Setup
    my_app = app.App(load_test_data)
    city_a = "ARACAJU"
    city_b = "BELEM"
    desired = 2079

    # Exercise
    actual = my_app.dist_CityA_CityB(city_a, city_b)

    # Verify
    assert actual == desired

# def test_consult_segment(monkeypatch, load_test_data):
#     # Setup
#     # monkeypatch the "input" function, so that it returns  desired answers.
#     # This simulates the user entering "ARACAJU" and "BELEM" in the terminal, one after the other:
#     responses = iter(["ARACAJU, BELEM"])
#     monkeypatch.setattr('builtins.input', lambda _: next(responses))
#     desired = 2079

#     # Exercise