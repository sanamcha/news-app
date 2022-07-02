from flask import Flask, render_template, redirect, session, flash, jsonify, request, url_for
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, db, User, Comment, Post, News
from forms import UserForm , PostForm, AddNewsForm, EditNewsForm, DeleteForm, CommentForm
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import Unauthorized
import json 
import requests 
from flask_sqlalchemy import SQLAlchemy

# from secrets import API_SECRET_KEY 

from news import  get_general_news, get_technology_news, get_health_news, get_business_news, get_entertainment_news, get_sports_news, get_science_news, get_bitcoin_news, get_jobs_news, get_travel_news, get_animals_news, get_military_news, get_fitness_news, get_pets_news, get_beauty_news, get_tech_news, get_relationships_news, get_stocks_news, get_weather_news
import os




app = Flask(__name__)

API_SECRET_KEY = '92782db9a8a24a56a2aee9a018266277'
uri = os.getenv("DATABASE_URL")  
if uri and uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL',"postgresql:///news_app") 

# app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///news_app"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['SQLALCHEMY_RECORD_QUERIES'] = True
# app.config['SECRET_KEY'] = '1234567890secret'
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY','1234567890secret')



app.config['DEBUG'] = True

# db = SQLAlchemy(app)

# toolbar = DebugToolbarExtension(app)
connect_db(app)
db.create_all()



@app.errorhandler(404)
def page_not_found(e):
    """Show 404 NOT FOUND page."""

    return render_template('404.html'), 404

@app.route('/')
def index_page():
    """The home page"""

  
    url =f'https://newsapi.org/v2/top-headlines?country=us&apiKey={API_SECRET_KEY}'
    
    response = requests.get(url).json()
    article = {
        'articles' : response["articles"]
    }
   

    url2=f"https://newsapi.org/v2/top-headlines/sources?apiKey={API_SECRET_KEY}"

    res = requests.get(url2).json()

    source = {
        'sources' : res["sources"]
    }

    return render_template('home-page.html', article=article, source=source)



@app.route('/general')
def general_news():
    general_articles = get_general_news()
   
    return render_template("news.html", articles=general_articles)

@app.route('/sports')
def sports_news():
    sports_articles = get_sports_news()
  
    return render_template("news.html", articles=sports_articles)

@app.route('/technology')
def technology_news():
    technology_articles = get_technology_news()
   
    return render_template("news.html", articles=technology_articles)

@app.route('/science')
def science_news():
    science_articles = get_science_news()
   
    return render_template("news.html", articles=science_articles)

@app.route('/entertainment')
def entertainment_news():
    entertainment_articles = get_entertainment_news()

    return render_template("news.html", articles=entertainment_articles)

@app.route('/health')
def health_news():
    health_articles = get_health_news()
  
    return render_template("news.html", articles=health_articles)

@app.route('/business')
def business_news():
    business_articles = get_business_news()
 
    return render_template("news.html", articles=business_articles)

@app.route('/bitcoin')
def bitcoin_news():
    bitcoin_articles = get_bitcoin_news()

    return render_template("news.html", articles=bitcoin_articles)

@app.route('/jobs')
def jobs_news():
    jobs_articles = get_jobs_news()
   
    return render_template("news.html", articles=jobs_articles)

@app.route('/travel')
def travel_news():
    travel_articles = get_travel_news()
   
    return render_template("news.html", articles=travel_articles)

@app.route('/stocks')
def stocks_news():
    stocks_articles = get_stocks_news()
  
    return render_template("news.html", articles=stocks_articles)

@app.route('/fitness')
def fitness_news():
    fitness_articles = get_fitness_news()
    
    return render_template("news.html", articles=fitness_articles)

@app.route('/pets')
def pets_news():
    pets_articles = get_pets_news()
   
    return render_template("news.html", articles=pets_articles)

@app.route('/military')
def military_news():
    military_articles = get_military_news()
   
    return render_template("news.html", articles=military_articles)

@app.route('/tech')
def tech_news():
    tech_articles = get_tech_news()
   
    return render_template("news.html", articles=tech_articles)

@app.route('/animals')
def animals_news():
    animals_articles = get_animals_news()
   
    return render_template("news.html", articles=animals_articles)

@app.route('/relationships')
def relationships_news():
    relationships_articles = get_relationships_news()
    
    return render_template("news.html", articles=relationships_articles)

@app.route('/beauty')
def beauty_news():
    beauty_articles = get_beauty_news()
   
    return render_template("news.html", articles=beauty_articles)

@app.route('/weather')
def weather_news():
    weather_articles = get_weather_news()
   
    return render_template("news.html", articles=weather_articles)

# #########   search page ############

@app.route('/search', methods=['POST', 'GET'])
def search():
 
    if request.method =='POST':
        search = request.form['search']
  
        url =(f'https://newsapi.org/v2/everything?q={search}&apiKey={API_SECRET_KEY}')

        response = requests.get(url)
        data = response.json()
        articles = data['articles']
        
        return render_template('search.html', articles=articles, search=search)



@app.route('/news')
def login_news_page():
    """The home page"""
  
    url = f"https://newsapi.org/v2/everything?domains=wsj.com&apiKey={API_SECRET_KEY}" 
   
    response = requests.get(url)
    data = response.json()
    articles = data['articles']

    return render_template('news.html', articles=articles)

@app.route("/covid")
def covid_news():
   
    url=f"https://newsapi.org/v2/top-headlines?q=covid&apiKey={API_SECRET_KEY}"
    

    response = requests.get(url).json()

    article = {
        'articles' : response["articles"]
    }
    return render_template ("/covid-news.html", article=article)




#   ###############  for user register  ###############

@app.route('/register', methods=['GET', 'POST'])
def register_user():
 
    form = UserForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        new_user = User.register(username, password)

        db.session.add(new_user)
        try:
            db.session.commit()
        except IntegrityError:
            form.username.errors.append('Username taken.  Please pick another')
            return render_template('register.html', form=form)
        session['user_id'] = new_user.id
        flash('Welcome! Successfully Created Your Account!', "success")
        return redirect('/news')

    return render_template('register.html', form=form)




################ for user login###############

@app.route('/login', methods=['GET', 'POST'])
def login_user():

    form = UserForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)
        if user:
            flash(f"Welcome Back, {user.username}!", "primary")
            session['user_id'] = user.id
            return redirect('/news')
        else:
            form.username.errors = ['Invalid username/password.']

    return render_template('login.html', form=form)




######## for logout ###############
@app.route('/logout')
def logout_user():
    session.pop('user_id')
    flash("Goodbye!", "info")
    return redirect('/')

# ########  username ############
@app.route("/users/<user_id>")
def user_show(user_id):

    if "user_id" not in session or user_id != session['user_id']:
        raise Unauthorized()
   
    user = User.query.get(user_id)
   
    form = PostForm()

    return render_template("post/post-news.html", user=user, form=form)



# ######## user_id delete ########
@app.route("/users/<user_id>/delete", methods=["POST"])
def user_remove(user_id):

    if "user_id" not in session or user_id != session['user_id']:
        raise Unauthorized()

    user = User.query.get(user_id)
    db.session.delete(user)

    db.session.commit()
    session.pop("user_id")

    return redirect("/login")




# ############### Post News ############

@app.route('/post-news')
def post_news():
    """posting news"""
  
    posts = Post.query.all()

    if "user_id" not in session:
        
        flash("Please login first!", "danger")
        return redirect('/')
    
    return render_template('post/post-news.html', posts=posts)



@app.route('/post-news/add', methods=["GET", "POST"])
def add_news():
    """adding news"""

    form = AddNewsForm()

    if form.validate_on_submit():
        data = {k: v for k, v in form.data.items() if k != "csrf_token"}
        
        posts_news = Post(image_url = form.image_url.data, 
                    author = form.author.data, 
                    title = form.title.data, 
                    description = form.description.data,
                    )

        db.session.add(posts_news)
        db.session.commit()

        flash(f"{posts_news.title} added.")
        return redirect("/post-news")
        # return redirect(f"/users/{posts.user_id}")

    else:
        return render_template("post/add-news.html", form=form)


@app.route("/post-news/<int:post_id>/update", methods=["GET", "POST"])
def edit_news(post_id):
    """Edit pet."""

    post = Post.query.get_or_404(post_id)

    form = EditNewsForm(obj=post)

    if form.validate_on_submit():
        post.image_url = form.image_url.data
        post.author = form.author.data
        post.title = form.title.data
        post.description = form.description.data
        
       
        db.session.commit()

        flash(f"{post.title} updated.")
        return redirect("/post-news")
       

    else:
        return render_template("post/edit-news.html", form=form, post=post)



@app.route("/post-news/<int:post_id>/delete", methods=["POST"])
def delete_news(post_id):
    """To Delete news post..."""

    post = Post.query.get_or_404(post_id)
   
    db.session.delete(post)
    db.session.commit()

    flash(f"Post {post.title} deleted.")

    return redirect("/post-news")
 
# ######## add comment #######



@app.route("/post-news/<int:post_id>/comment", methods=["GET", "POST"])

def comment_post(post_id):

    post = Post.query.get_or_404(post_id)
    comment = Comment.query.filter_by(post_id=post.id).all()
    

    form = CommentForm()
    if request.method == 'POST':

        if form.validate_on_submit():
            comment = Comment(text=form.text.data, post_id=post.id)
            db.session.add(comment)
            db.session.commit()
            flash("Your comment has been added to the post", "success")
            return redirect(url_for("show_post_comment", post_id=post.id))

    return render_template("post/comment-post.html", form=form, post_id=post_id, comment=comment, post=post)


@app.route("/post-news/<int:post_id>", methods=["GET", "POST"])
def show_post_comment(post_id):

 
    post = Post.query.get_or_404(post_id)
    comments = Comment.query.filter_by(post_id=post.id).all()

    return render_template("post/show-comment-post.html", post_id=post_id, comments=comments, post=post)

@app.route("/post-news/<int:comment_id>/delete", methods=["POST"])
def delete_comment(comment_id):
    """To Delete feedback."""

    comment = Comment.query.get(comment_id)
  
   
    db.session.delete(comment)
    db.session.commit()

    return redirect("/post-news")



# ###########################  news comment page ###############

@app.route('/news-lists')
def news_list():
    """lists of news"""

    news = News.query.all()
 

    # db.session.add(news)
    db.session.commit()
    return render_template('news-lists/news-lists.html', news=news)


@app.route("/news-lists/<int:news_id>", methods=["GET", "POST"])
def show_news_detail(news_id):

    news = News.query.get_or_404(news_id)
    
    comments = Comment.query.filter_by(news_id=news.id).all()

    return render_template("/news-lists/show-comment-news.html", news_id=news.id, comments=comments, news=news)



@app.route("/news-lists/<int:news_id>/comment", methods=["GET", "POST"])

def comment_news(news_id):
  
    news = News.query.get_or_404(news_id)
    comments = Comment.query.filter_by(news_id=news.id).all()
    
    
    form = CommentForm()
    if request.method == 'POST':

        if form.validate_on_submit():
            comment = Comment(text=form.text.data, news_id=news.id)
            db.session.add(comment)
            db.session.commit()
            flash("Your comment has been added to the post", "success")
            return redirect(url_for("show_news_detail", news_id=news.id))

    return render_template("/news-lists/comment-news.html", form=form, news_id=news_id, comments=comments)


@app.route("/news-lists/<int:comment_id>/delete", methods=["POST"])

def delele_news_comment(comment_id):
    """to delete comments.."""

    

    comment = Comment.query.get_or_404(comment_id)

    db.session.delete(comment)
    db.session.commit()

    flash('Comment has deleted ','success')

    return redirect("/news-lists")

