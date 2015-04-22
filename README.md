# Peon

A front-end develop helper.

1. Start dev server with SimpleHTTPServer or Harp.
2. Watching file changes for coffee less and jade.
3. Build static files from task config.
4. Create backups.
5. Packing and uploads
6. Transport data so supmice system.

==============
I build peon is becuase we are python project team, sometime grunt or gulp can't full fill our needs, custom nodejs scripts is too hard for my team, but python is much more easier...


## Usage
You have to place a 'peon.json' intro the project root folder first.
* peon.json: Config peon's tasks, see the example.

`peon [-s] [-c] [-w]`

=======================
### -c: Construct

Must with a peon.json in same folder when run this command.

##### task: Rev

Revision to md5 by 'pattern' find in given files.
Use it after grunt relese, because grunt litte bit hard to convert md5 filename.

```
  "rev":{
    "src":"/*.html",
    "cwd":"release/",
    "find":"?md5=null",
    "pattern":"null"
  }
```
rev: The key of task options.

src: Source file path.

cwd: Root dir of file path.

pattern: Replacement pattern, peon will replace those string intro md5 code.

[optional]

find:  Specify the exact scope of a pattern. Peon will find those string and  replace pattern with that string.

##### task: Copy

Copy files from src to dest.

```
  "copy": {
    "libs":{
      "flatten": true,
      "src":[
        "lodash/dist/lodash.js",
        "angular/angular.js",
        "**/**/*.js",
      ],
      "cwd":"bower_components/",
      "dest":"src/libs"
    }
  }
```
copy: The key of task options.

<group>: A group name of copy files. 'libs' is group name in the sample above. usual define different package. You can define multiple groups with different options. and you have to make different group name by your self.

src: Source file path.

cwd: Root dir of file path.

dest: Dest for copy files.

[optional]

flatten: Those files will not keep their folder while copy to the dest.

=======================
### -z:  Packing

Make a zip package for all files in current folder, or specific folder.
You can also chose upload to a restapi.

##### task: Zip

*** This cmd can runing with our peon.json tasks. 

***cli:*** `--exclude` for exclude files pattern.

```
  "zip":{
    "include_hidden":false,
    "include_peon_config":false,
    "excludes":[],
  }

```
`file` file name you want to specific. default is current folder name.
`include_hidden` include start with '.'.
`include_peon_config` include 'peon.json'.
`excludes` excludes files as list. pattern supported.

##### task: Upload

*** This cmd can only work with peon.json tasks. 
make sure there is `zip` task before, otherwise will get a error.

```
  "upload":{
    "headers":{
      "SecretKey":"1d02aa814dc64db3a6494624ca35a03a"
    },
    "url":"http://localhost:5000/ws/test/develop_theme",
    "data":null,
    "params":null
  }

```

`headers` anything you need put intro headers.
`url` request api url.
`data` request data
`params` request params
`file` file name you want to specific. default is current folder name.


## -b: Backup
Backup file and db.

```
  "backup":{
    "redis":{
      "src":"/Users/redy/dump.rdb",
      "dbname":"dev",
      "dbhost":null,
      "port":null,
      "user":null,
      "pwd":null,
      "dest":null
    },
    "mongodb":{
      "dbname":"dev",
      "dbhost":null,
      "port":null,
      "user":null,
      "pwd":null,
      "src":null,
      "dest":null
    },
    "files":{
      "src":[
        "/Users/redy/deployment_data/",
        "/Users/redy/etc/nginx/sites-available/",
        "/Users/redy/etc/supervisor/conf.d/"
      ]
    }
  }

```

## -w: Watcher

`peon` -w

Wactching Coffee jade less. If it's changed than compile a new file.

files start or end with undescore '_' is changed will compile all files but it self.



## -s: Server

`peon` -s [port] or just `peon`

if you got coffee jade or less, will automaticly start with harp.

`peon` -s --harp, start server with harp directly.
`peon` -s --http, start server with simplehttp directly.


Please make sure you have node npm harp kind stuff ...

## -t : Transport

`peon` -t [upload] or `peon` -t [download]

Trassport pyco content file and site data to supmice system

'dest' or 'cwd' is define the content folder for upload or download.


```
  "transport":{
    "upload":{
      "cwd":".",
      "headers":{
        "SecretKey":"1d02aa814dc64db3a6494624ca35a03a"
      },
      "url":"http://localhost:5000/ws/123123/develop_sync_sitedata"
    },
    "download":{
      "dest":".",
      "headers":{
        "SecretKey":"1d02aa814dc64db3a6494624ca35a03a"
      },
      "url":"http://localhost:5000/ws/123123/develop_sync_sitedata"
    }
  }
```

*** Content sample ***
```
  content/
    content_type/
      somepage.md
      ...
    site.json
    index.md
    error_404.md
    somepage.md
    ...
    
```

*** Site.json smaple ***
```
{
  "meta": {
    "author": "redy",
    "copyright": "2015 © Soopro tech Co., Ltd.",
    "description": "...",
    "license": "#license",
    "locale": "en_US",
    "logo": null,
    "register": {
      "placeholder": "Email address for register",
      "text": "Free Register",
      "url": ""
    },
    "title": "Soopro",
    "translates": {
      "en_US": {
        "name": "English",
        "url": "#"
      },
      "zh_CN": {
        "name": "汉语",
        "url": "#"
      }
    }
  },
  "content_types": {
    "_feature": "Features",
    "_gallery": "Gallery",
    "page": "Pages"
  },
  "menus": {
    "primary": [
      {
        "alias": "home",
        "meta": {},
        "nodes": [],
        "title": "Back to home",
        "url": "/"
      },
      {
        "alias": "video",
        "meta": {},
        "nodes": [],
        "title": "Watch Video",
        "url": "/video"
      }
    ]
  },
  "terms": {
    "category": [
      {
        "alias": "inneral",
        "meta": {
          "parent": "",
          "pic": ""
        },
        "priority": 0,
        "title": "INNERAL"
      },
      {
        "alias": "forign",
        "meta": {
          "parent": "",
          "pic": ""
        },
        "priority": 0,
        "title": "FORGIN"
      }
    ]
  }
}
```


## Installation
python setup.py install

