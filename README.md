# :giraffe: Giraffael :giraffe:

Long, but not alone.

Checkout Giraffael on [this repository](https://github.com/SpecialNoel/Giraffael).

Checkout Giraffael on [this Notion page](https://www.notion.so/Project-Giraffael-15fa829a7ea780a7a2cdf502792b7805).

Project Tree:

```
Giraffael
├─ .DS_Store
├─ .dockerignore
├─ LICENSE
├─ README.md
├─ client
│  ├─ requirements.txt
│  └─ src
│     └─ app
├─ compose.yaml
├─ frontend
├─ infra
│  └─ docker
│     ├─ client.Dockerfile
│     ├─ infra
│     │  └─ docker
│     │     └─ redis.conf
│     ├─ redis.conf
│     └─ server.Dockerfile
└─ server
   ├─ requirements.txt
   └─ src
      ├─ __init__.py
      ├─ db
      │  └─ mongo
      ├─ main.py
      ├─ routers
      │  └─ websocket_routes.py
      ├─ schemas
      │  └─ definitions.py
      └─ services
         ├─ client_service.py
         ├─ connection_manager.py
         └─ pub_sub_service.py
         
```
