def test_create_expenses(client):
    client.post("/users/",json={"email":"a@b.com","password":"123"})
    login_res= client.post("/login",data={"username":"a@b.com","password":"123"})
    token=login_res.json()["access_token"]
    res=client.post("/expenses/",json={"title":"Lunch","amount":120,"category":"food","date": "2026-09-03T12:00:00"},
        headers={"Authorization":f"Bearer {token}"})
    assert res.status_code==201

def test_get_expenses_empty(client):
    client.post("/users/",json={"email":"a@b.com","password":"123"}) #creating user
    login_res=client.post("/login",data={"username":"a@b.com","password":"123"})
    token = login_res.json()["access_token"]

    res = client.get("/expenses/", headers={"Authorization": f"Bearer {token}"})
    
    assert res.status_code == 404
    
    
def test_get_expenses_with_data(client):
    client.post("/users/",json={"email":"a@b.com","password":"123"})
    login_res=client.post("/login",data={"username":"a@b.com","password":"123"})
    token=login_res.json()["access_token"]
    client.post("/expenses/",json={"title":"Lunch","amount":120,"category":"food","date": "2026-09-03T12:00:00"},
        headers={"Authorization":f"Bearer {token}"})
    res= client.get("/expenses",headers={"Authorization":f"Bearer {token}"})
    assert res.status_code==200
    assert isinstance(res.json(),list)    
        
def test_expenses_update(client):
    client.post("/users",json={"email":"a@b.com","password":"123"}) 
    login_res=client.post("/login",data={"username":"a@b.com","password":"123"})
 
    token=login_res.json()["access_token"]
    create_res=client.post("/expenses/",json={"title":"Lunch","amount":120,"category":"food","date": "2026-09-03T12:00:00"},
            headers={"Authorization":f"Bearer {token}"})   
    expense_id=create_res.json()["id"]
    res=client.put(f"/expenses/{expense_id}",json={"title":"Lunch","amount":220,"category":"food","date": "2026-09-03T12:00:00"},
            headers={"Authorization":f"Bearer {token}"})     
    assert res.status_code==200
    
def test_expenses_delete(client):
    client.post("/users",json={"email":"a@b.com","password":"123"}) 
    login_res=client.post("/login",data={"username":"a@b.com","password":"123"})
 
    token=login_res.json()["access_token"]
    create_res=client.post("/expenses/",json={"title":"Lunch","amount":120,"category":"food","date": "2026-09-03T12:00:00"},
            headers={"Authorization":f"Bearer {token}"})   
    expense_id=create_res.json()["id"]
    res=client.delete(f"/expenses/{expense_id}",
            headers={"Authorization":f"Bearer {token}"})     
    assert res.status_code==204