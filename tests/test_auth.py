# def test_register_user(client):
#     res = client.post("/users/", json={"email": "a@b.com", "password": "pass123"})
#     assert res.status_code == 201
#     assert res.json()["email"] == "a@b.com"

# def test_register_duplicate_email_fails(client):
#     client.post("/users/", json={"email": "a@b.com", "password": "pass123"})
#     res = client.post("/users/", json={"email": "a@b.com", "password": "pass123"})
#     assert res.status_code == 409
    
# def test_register_bad_email_returns_422(client):
#     res= client.post('/users/',json={
#         "email":"abc.com",
#         "password":"222"
#     })   
#     assert res.status_code==422 
    
# def test_login_success(client):
#         client.post("/users/",json={"email":"a@b.com","password":"123"})
#         res=client.post("/login",data={"username":"a@b.com","password":"123"})
#         assert res.status_code== 200
        
# def test_login_wrong_password_fail(client):
#         client.post("/users/",json={"email":"a@b.com","password":"123"})
#         res=client.post("/login",data={"username":"a@b.com","password":"1234"})
#         assert res.status_code== 403
        