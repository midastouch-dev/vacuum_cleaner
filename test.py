import pytest
import json
from app import app

"""
Test the default url
@Resp   status_code: 200
@Resp   data: '<h1>Hello, Vacuum Cleaner!</h1>'
"""
def test_default_route():
    res = app.test_client().get('/')
    assert res.status_code == 200
    assert res.data.decode('utf-8') == '<h1>Hello, Vacuum Cleaner!</h1>'

"""
Test the wrong url
@Resp   status_code: 404
"""
def test_wrong_route():
    res = app.test_client().get('/wrong-url')
    assert res.status_code == 404
    assert '404 Not Found' in res.data.decode('utf-8')

"""
Test the clean url without parameters
@Resp   status_code: 400
@Resp   err: 'Missing data'
"""
def test_clean_without_parameters():
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    data = {}
    res = app.test_client().post('/clean', data=json.dumps(data), headers=headers)
    assert res.status_code == 400
    assert res.json['error'] == 'Missing data'

"""
Test the clean url withwout cleaning_batches paramter
@Param  priority: [7,4, 2]
@Resp   status_code: 400
@Resp   err: 'Missing data' 
"""
def test_clean_without_cleaning_batches():
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    data = {
        "priority_rooms": [7,4, 2]
    }
    res = app.test_client().post('/clean', data=json.dumps(data), headers=headers)
    assert res.status_code == 400
    assert res.json['error'] == 'Missing data'

"""
Test the clean url withwout priority_rooms paramter
@Param  cleaning_batches: [[5,2,4],[2,8,4],[4,6,4,9]]
@Resp   status_code: 400
@Resp   err: 'Missing data' 
"""
def test_clean_without_priority_rooms():
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    data = {
        "cleaning_batches": [[5,2,4],[2,8,4],[4,6,4,9]]
    }
    res = app.test_client().post('/clean', data=json.dumps(data), headers=headers)
    assert res.status_code == 400
    assert res.json['error'] == 'Missing data'

"""
Test the clean url of step 1
@Param  cleaning_batches:   [[5,2,4],[2,8,4],[4,6,4,9]]
@Param  priority_rooms: [7,4, 2]
@Resp   status_code: 200
@Resp   cleaned_rooms: [4,2,5,4,2,8,4,6,9]
@Resp   final_room: 9
@Resp   rooms_passed_without_cleaning: 17
@Resp   total_batches: 3
@Resp   total_cleaned_rooms: 9
@Resp   traverse_path: [2,3,4,3,2,3,4,5,4,3,2,3,4,5,6,7,8,7,6,5,4,5,6,7,8,9]
"""
def test_clean_step1():
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    data = {
        "cleaning_batches": [[5,2,4],[2,8,4],[4,6,4,9]],
        "priority_rooms": [7,4, 2]
    }
    res = app.test_client().post('/clean', data=json.dumps(data), headers=headers)
    assert res.status_code == 200
    assert res.json['cleaned_rooms'] == [4,2,5,4,2,8,4,6,9]
    assert res.json['final_room'] == 9
    assert res.json['rooms_passed_without_cleaning'] == 17
    assert res.json['total_batches'] == 3
    assert res.json['total_cleaned_rooms'] == 9
    assert res.json['traverse_path'] == [2,3,4,3,2,3,4,5,4,3,2,3,4,5,6,7,8,7,6,5,4,5,6,7,8,9]


"""
Test the clean url of step 2
@Param  cleaning_batches:   [[5,2,4],[3,6,2],[4,6,3,7]]
@Param  priority_rooms: [7,4, 3]
@Resp   status_code: 200
@Resp   cleaned_rooms: [4,5,2,3,6,2,7,4,3,6]
@Resp   final_room: 6
@Resp   rooms_passed_without_cleaning: 19
@Resp   total_batches: 3
@Resp   total_cleaned_rooms: 10
@Resp   traverse_path: [8,7,6,5,4,5,4,3,2,3,4,5,6,5,4,3,2,3,4,5,6,7,6,5,4,3,4,5,6]
"""
def test_clean_step2():
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    data = {
        "cleaning_batches": [[5,2,4],[3,6,2],[4,6,3,7]],
        "priority_rooms": [7,4, 3]
    }
    res = app.test_client().post('/clean', data=json.dumps(data), headers=headers)
    assert res.status_code == 200
    assert res.json['cleaned_rooms'] == [4,5,2,3,6,2,7,4,3,6]
    assert res.json['final_room'] == 6
    assert res.json['rooms_passed_without_cleaning'] == 19
    assert res.json['total_batches'] == 3
    assert res.json['total_cleaned_rooms'] == 10
    assert res.json['traverse_path'] == [8,7,6,5,4,5,4,3,2,3,4,5,6,5,4,3,2,3,4,5,6,7,6,5,4,3,4,5,6]

"""
Test the clean url of step 3
@Param  cleaning_batches:   [[2,5,3, 8, 6],[4,5,4,6],[6,3,1,9],[10, 3, 2,1,4]]
@Param  priority_rooms: [1,6, 2, 8, 3]
@Resp   status_code: 200
@Resp   cleaned_rooms: [2,8,3,5,6,4,5,4,1,6,3,9,1,2,3,10,4]
@Resp   final_room: 4
@Resp   rooms_passed_without_cleaning: 45
@Resp   total_batches: 4
@Resp   total_cleaned_rooms: 18
@Resp   traverse_path: [5,4,3,2,3,4,5,6,7,8,7,6,5,4,3,4,5,6,5,4,5,4,3,2,1,2,3,4,5,6,5,4,3,4,5,6,7,8,9,8,7,6,5,4,3,2,1,2,3,4,5,6,7,8,9,10,9,8,7,6,5,4]
"""
def test_clean_step3():
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    data = {
        "cleaning_batches": [[2,5,3, 8, 6],[4,5,4,6],[6,3,1,9],[10, 3, 2,1,4]],
        "priority_rooms": [1,6, 2, 8, 3]
    }
    res = app.test_client().post('/clean', data=json.dumps(data), headers=headers)
    assert res.status_code == 200
    assert res.json['cleaned_rooms'] == [2,8,3,5,6,4,5,4,1,6,3,9,1,2,3,10,4]
    assert res.json['final_room'] == 4
    assert res.json['rooms_passed_without_cleaning'] == 45
    assert res.json['total_batches'] == 4
    assert res.json['total_cleaned_rooms'] == 18
    assert res.json['traverse_path'] == [5,4,3,2,3,4,5,6,7,8,7,6,5,4,3,4,5,6,5,4,5,4,3,2,1,2,3,4,5,6,5,4,3,4,5,6,7,8,9,8,7,6,5,4,3,2,1,2,3,4,5,6,7,8,9,10,9,8,7,6,5,4]


