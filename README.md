# compsci279r-hw5

## How to access hosted version

Navigate to 
https://radiant-scrubland-87346.herokuapp.com/ in a web browser.

## How to setup development environment

```sh
conda env create -f environment.yml
```

## How to run locally

```sh
conda activate compsci279r-hw5
python app.py
```

Open http://localhost:5000

## How to deploy to heroku

```sh
heroku login
heroku create
git push heroku main
heroku ps:scale web=1
heroku open
```

## Resources

To create this todo list, I used the tutorial at https://www.python-engineer.com/posts/flask-todo-app/

I also used:
- https://github.com/heroku/python-getting-started
- https://devcenter.heroku.com/articles/getting-started-with-python#deploy-the-app