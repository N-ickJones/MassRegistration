
### Docker Compose Automates Compilation
    See Dockerfile in this directory or docker-compose in app directory

-
-
-

### To Manually Compile Sass
##### Install npm
    apt install npm
    dnf install npm
    ..etc
##### Install sass
    npm i -g sass  # Or you can create a Virtual Environment
##### To Watch for changes
    cd ~/mass-registration/static/scss/    where ~ depends on your setup
    sass --watch bootstrap.scss:bootstrap.min.css --style compressed
##### Single Compile
    sass bootstrap.scss bootstrap.min.css --style compressed