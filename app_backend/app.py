from flask import  Flask, jsonify, request
from flask_sqlalchemy import  SQLAlchemy
import datetime
from flask_marshmallow import  Marshmallow
from flask_cors import  CORS



# settings
app = Flask(__name__)
CORS(app)



app.config['SQLALCHEMY_DATABASE_URI']  =  'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']  = False

db = SQLAlchemy(app)
ma = Marshmallow(app)



# table
class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description= db.Column(db.Text(), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.datetime.now)

    def __init__(self, title, description):
        self.title = title
        self.description = description

# schema
class BlogSchema(ma.Schema):
    class  Meta:
        fields = ("id", "title", "description", "date_created")


# schema obj
blog_schema = BlogSchema() 
blogs_schema = BlogSchema(many=True) 

# routes

#  ------------------ get all
@app.route('/get', methods=['GET'])
def get_blogs():
    all_blogs = Blog.query.all()
    return blogs_schema.jsonify(all_blogs) if all_blogs else "No blogs available!"
   


#  ------------------ get by ID
@app.route('/get/<id>/', methods=['GET'])
def blog_details(id):
    blog_detail = Blog.query.get(id)
    return blog_schema.jsonify(blog_detail) if blog_detail else "No blog post with that ID"
  
    


#  ------------------ post or add new 
@app.route('/add', methods=['POST'])
def add_blog():
    title = request.json['title']
    description = request.json['description']
    blogs = Blog(title, description)
    db.session.add(blogs)
    db.session.commit()
    return blog_schema.jsonify(blogs)

#  ------------------ update individual
@app.route('/update/<id>/', methods=['PUT'])
def update_blog(id):
    update_blog = Blog.query.get(id)
    update_blog.title = request.json['title']
    update_blog.description = request.json['description']
    db.session.commit()
    return blog_schema.jsonify(update_blog)


#  ------------------ delete individual
@app.route('/delete/<id>/', methods=['DELETE'])
def delete_blog(id):
    delete_blog = Blog.query.get(id)
    db.session.delete(delete_blog)
    db.session.commit()
    return blog_schema.jsonify(delete_blog)


    


if __name__ == '__main__':
    app.run(debug=True)
