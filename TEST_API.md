## TEST API Example
#### GET https://127.0.0.1:5000/getallcache
```json
# response
{
	"n1": "ac4f913f9d97098f88e454ecee76f24e41b26bca18cf0cc7d018b61ba1f1a17e"
}
```

#### GET https://127.0.0.1:5000/auth/get_user_info
```json
# request
{
	"name": "n1",
	"email": "n1@gamil.com",
	"user": ["name", "business", "created_at"],
	"profile": ["nationality", "like", "comment"]
}
# response
{
	"data": "get user info",
	"info": {
		"business": false,
		"comment": [],
		"created_at": "Thu, 14 Mar 2024 01:48:28 GMT",
		"like": {},
		"name": "n1",
		"nationality": "ko"
	},
	"status": "success"
}
```

#### POST https://127.0.0.1:5000/auth/create_user
```json
# request
{
	"name": "n1",
	"email": "n1@gamil.com",
	"password": "Naszxqw1!",
	"nationality": "ko"
}
# response
{
	"data": "create user",
	"status": "success"
}
# fail request
{
	"name": "n2",
	"email": "n2@gamil.com",
	"password": "Naqw2!",
	"nationality": "ko"
}
# fail response
{
	"data": "password condition check failed",
	"status": "error"
}
```

#### POST https://127.0.0.1:5000/auth/delete_user
```json
# request
{
	"name": "n1",
	"email": "n1@gamil.com"
}
# response
{
	"data": "delete user",
	"status": "success"
}
```

#### POST https://127.0.0.1:5000/auth/login
```json
# request
{
    "name": "",
    "email": "n1@gamil.com",
	"password": "Naszxqw1!"
}
# response
{
	"data": "login",
	"status": "success"
}
```

#### POST https://127.0.0.1:5000/auth/update_profile
```json
# request
{
	"name": "n1",
    "email": "n1@gamil.com",
	"newprofile": {
		"nationality": "us",
		"clip": 550,
		"like": {
			"1post": 21
		}
	},
	"delprofile": {
		"clip": 551,
		"like": "3post"
	}
}
# response
{
	"data": "update profile",
	"status": "success"
}
```

#### POST https://127.0.0.1:5000/post/add_post
```json
# request
{
	"name": "n1",
	"title": "title1",
	"images": {
		"img1": "http://imgurl1"
	},
	"content": "content1",
	"amenity": ["am1", "am2"],
	"price": 123.456,
	"available_start_at": "2024-03-15 00:07:35",
	"available_end_at": "2024-03-17 23:59:59"
}
# response
{
	"data": "add post",
	"status": "success"
}
```
