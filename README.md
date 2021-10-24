# storyteller


### .env
This project controls secrets such as user id and password or API tokens via .env file on the root directory of the project.

`.env` file must have format like followings.
```
es_user={elasticsearch user name}
es_password={elasticsearch user password}
```

### Downloading data


### Indexing a corpus

```shell
python3 -m storyteller.main.index --i="gk" --b=1500
```

### Searching a phrase

```shell

python3 -m  storyteller.main.index --wisdom="산 넘어 산"
```

### Building wisdom2def or wisdom2eg 
