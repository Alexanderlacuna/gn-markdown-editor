# Gn-markdown-editor

Gn-markdown-editor  is a tiny web tool to preview Markdown formatted text.



##  Running only the UI
for quick setup without server processing run

python -m http.server





## Run local testing server

use guix;etc to load the requirements(python,flask and markdown)

```
python -m main

```



### example on how to edit a page as a server 

*NB:edit the config file to provide to your github access token*


```
{{SERVER_URL}}/?refresh_link=https://github.com/{{user_name}}/{{repo_name}}/blob/{{branch}}/{{file_name}}

e.g 
http://127.0.0.1:5000/?refresh_link=https://github.com/Alexanderlacuna/data-vault-2/blob/master/README.md

```



## License
see License File



## TODOS

[] add full resize functionality for browser and render page

[] full editor customization like color scheme,key bindings 