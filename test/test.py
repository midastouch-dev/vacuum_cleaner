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
Normally clean the rooms. The rooms of batch aren't in the prioriy_rooms.
The vacuum cleaner is located on room 1.
"""
def test_clean_step1():
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    data = {
        "cleaning_batches": [[5,3,4],[5,8,4],[9,3,6]],
        "priority_rooms": [7,1,2]
    }
    res = app.test_client().post('/clean', data=json.dumps(data), headers=headers)
    assert res.status_code == 200
    assert res.json['cleaned_rooms'] == [5,3,4,5,8,4,9,3,6]
    assert res.json['final_room'] == 6
    assert res.json['rooms_passed_without_cleaning'] == 20
    assert res.json['total_batches'] == 3
    assert res.json['total_cleaned_rooms'] == 9
    assert res.json['traverse_path'] == [1,2,3,4,5,4,3,4,5,6,7,8,7,6,5,4,5,6,7,8,9,8,7,6,5,4,3,4,5,6]


"""
Clean the rooms of priority_rooms first. 
The room 4 is in priority, it's cleaned first in batch 1, 2.
The vacuum cleaner is located on room 6.
"""
def test_clean_step2():
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    data = {
        "cleaning_batches": [[5,3,4],[5,4,8],[9,3,6]],
        "priority_rooms": [7,4,2]
    }
    res = app.test_client().post('/clean', data=json.dumps(data), headers=headers)
    assert res.status_code == 200
    assert res.json['cleaned_rooms'] == [4,5,3,4,5,8,9,3,6]
    assert res.json['final_room'] == 6
    assert res.json['rooms_passed_without_cleaning'] == 11
    assert res.json['total_batches'] == 3
    assert res.json['total_cleaned_rooms'] == 9
    assert res.json['traverse_path'] == [6,5,4,5,4,3,4,5,6,7,8,9,8,7,6,5,4,3,4,5,6]

"""
If the index of rooms is different in batch and priority, the priority's index is priority.
The room 2 is located on before room 4 in 2nd batch. But the room 4 cleans first in that batch.
The vacuum cleaner is located on room 6.
"""
def test_clean_step3():
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    data = {
        "cleaning_batches": [[5,3,4],[8,2,4],[9,3,6]],
        "priority_rooms": [7,4,2]
    }
    res = app.test_client().post('/clean', data=json.dumps(data), headers=headers)
    assert res.status_code == 200
    assert res.json['cleaned_rooms'] == [4,5,3,4,2,8,9,3,6]
    assert res.json['final_room'] == 6
    assert res.json['rooms_passed_without_cleaning'] == 15
    assert res.json['total_batches'] == 3
    assert res.json['total_cleaned_rooms'] == 9
    assert res.json['traverse_path'] == [6,5,4,5,4,3,4,3,2,3,4,5,6,7,8,9,8,7,6,5,4,3,4,5,6]

"""
If the rooms are repeated continuously, the vacuum cleaner cleans once that room. 
The room 4 was repeated 3 times on the following example. But the vacuum cleaner cleans the room 4 once.
The vacuum cleaner is located on room 6.
"""
def test_clean_step4():
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    data = {
        "cleaning_batches": [[5,2,4],[4,4,8],[9,3,6]],
        "priority_rooms": [7,1,2]
    }
    res = app.test_client().post('/clean', data=json.dumps(data), headers=headers)
    assert res.status_code == 200
    assert res.json['cleaned_rooms'] == [2,5,4,8,9,3,6]
    assert res.json['final_room'] == 6
    assert res.json['rooms_passed_without_cleaning'] == 15
    assert res.json['total_batches'] == 3
    assert res.json['total_cleaned_rooms'] == 7
    assert res.json['traverse_path'] == [6,5,4,3,2,3,4,5,4,5,6,7,8,9,8,7,6,5,4,3,4,5,6]

"""
If the room of priority are repeated in one batch, the vacuum cleaner cleans once that room. 
The room 1 is repeated twice in 2nd batch, room 2 is repeated twice in 3rd batch. But these rooms are clean once in each batch.
The vacuum cleaner is located on room 6.
"""
def test_clean_step5():
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    data = {
        "cleaning_batches": [[5,2,4],[1,4,1],[5,2,6,2]],
        "priority_rooms": [7,1,2]
    }
    res = app.test_client().post('/clean', data=json.dumps(data), headers=headers)
    assert res.status_code == 200
    assert res.json['cleaned_rooms'] == [2,5,4,1,4,2,5,6]
    assert res.json['final_room'] == 6
    assert res.json['rooms_passed_without_cleaning'] == 12
    assert res.json['total_batches'] == 3
    assert res.json['total_cleaned_rooms'] == 8
    assert res.json['traverse_path'] == [6,5,4,3,2,3,4,5,4,3,2,1,2,3,4,3,2,3,4,5,6]

"""
If the starting clean room is same as current room, the vacuum clean that room.
The current room is 6. The vacuum cleaner have to start the cleaning at number 6.
The vacuum cleaner is located on room 6.
"""
def test_clean_step6():
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    data = {
        "cleaning_batches": [[5,6,4],[1,4,1],[5,2,6,2]],
        "priority_rooms": [7,1,6]
    }
    res = app.test_client().post('/clean', data=json.dumps(data), headers=headers)
    assert res.status_code == 200
    assert res.json['cleaned_rooms'] == [6,5,4,1,4,6,5,2]
    assert res.json['final_room'] == 2
    assert res.json['rooms_passed_without_cleaning'] == 7
    assert res.json['total_batches'] == 3
    assert res.json['total_cleaned_rooms'] == 8
    assert res.json['traverse_path'] == [6,5,4,3,2,1,2,3,4,5,6,5,4,3,2]

"""
Clean the rooms with long batches and priority rooms.
The vacuum cleaner is located on room 2.
"""
def test_clean_step7():
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    data = {
        "cleaning_batches": [[5,6,4,7, 9,2,6,2,7],[1,4,1,8,12,3,5,6],[5,2,6,2],[13,4,2,6,8,3,2,7,7],[2,4,9,3,2,4,7,8,4]],
        "priority_rooms": [7,1,6, 5, 2, 9, 3]
    }
    res = app.test_client().post('/clean', data=json.dumps(data), headers=headers)
    assert res.status_code == 200
    assert res.json['cleaned_rooms'] == [7,6,5,2,9,4,1,6,5,3,4,8,12,6,5,2,7,6,2,3,13,4,8,7,2,9,3,4,8,4]
    assert res.json['final_room'] == 4
    assert res.json['rooms_passed_without_cleaning'] == 84
    assert res.json['total_batches'] == 5
    assert res.json['total_cleaned_rooms'] == 30
    assert res.json['traverse_path'] == [2,3,4,5,6,7,6,5,4,3,2,3,4,5,6,7,8,9,8,7,6,5,4,3,2,1,2,3,4,5,6,5,4,3,4,5,6,7,8,9,10,11,12,11,10,9,8,7,6,5,4,3,2,3,4,5,6,7,6,5,4,3,2,3,4,5,6,7,8,9,10,11,12,13,12,11,10,9,8,7,6,5,4,5,6,7,8,7,6,5,4,3,2,3,4,5,6,7,8,9,8,7,6,5,4,3,4,5,6,7,8,7,6,5,4]

