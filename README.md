# setting-up-interop


## setting up the server side 

```
cd interop/server
```
Create the interop server's database.

```
sudo ./interop-server.sh create_db
```

```
sudo ./interop-server.sh load_test_data
```

## run the server

```
sudo ./interop-server.sh up
```


## run the client side  

```
sudo ./interop-client.sh run
```

this will start a root terminal in the docker constiner

## get data

in the docker container

```
./tools/interop_cli.py \
    --url http://127.0.0.1:8000 \
    --username testuser \
    teams
 ```
 
 ## get mission file
 
 in client folder there are three python scripts get_mission_file.py,auvsi_server_params.py
 
 send them to the docker container using this command
 
 in a differnt terminal cd into interop/client
 
 ```
 sudo docker cp get_mission_file.py <container id>:/interop/client/
 sudo docker cp auvsi_server_params.py <container id>:/interop/client/
 ```
 
 now go into the root docker terminal and run 
 
 ``` 
 python3 get_mission_file.py
 ```
 
 a condensed_mission2.json file will appear in the container 
 
 u can get it to local by 
 
 ```
 sudo docker cp <container id>:/interop/client/condensed_mission2.json ~/main/manas/interop/interop/client

 
 

 
 






