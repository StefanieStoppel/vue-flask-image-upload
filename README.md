# vue-flask-image-upload
This repo contains an example application for uploading *.png images
from the Vue.js frontend to a simple flask REST server at which saves them to a local directory.
<img src="./src/assets/screenshot.png" alt="Screenshot of the application" width="500px" height="auto">

## Project setup
You need to start both the Python web server and the Vue.js frontend for the application to work.

#### Prerequisites
- [Python3](https://www.python.org/)
- [Yarn](https://classic.yarnpkg.com/en/docs/getting-started)

### Python Flask backend
#### Create a virtual environment
```
cd server
python3 -m venv .venv
. .venv/bin/activate
```

#### Install dependencies
```
pip install -r requirements.txt
```

#### Launch the web server
It will listen to file uploads at <http://localhost:5000/upload-images/>.
```
python app.py
```
The application will upload the images to `$HOME/Desktop/vue-flask-image-upload`.

### Vue.js Frontend
```
yarn install
```

#### Compiles and hot-reloads for development
Runs the development server on <http://localhost:8080/>.
```
yarn serve
```

#### Compiles and minifies for production
```
yarn build
```

#### Lints and fixes files
```
yarn lint
```

#### Customize configuration
See [Configuration Reference](https://cli.vuejs.org/config/).


##### Kudos
Styling kudos go mostly to the author of [this CodePen](https://codepen.io/wallaceerick/pen/fEdrz)