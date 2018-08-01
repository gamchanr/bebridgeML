from flask import Flask, render_template,request
from main import MLprocessing
from flask_pymongo import PyMongo
from elasticsearch import Elasticsearch
import time

INDEX_NAME = "msg_index"  # the name of the index
DOC_TYPE = "doc"  # we have a single type of document, so it doesn't matter
INDEX_SETTINGS = {
  "settings": {
     "index" : {
         "number_of_shards" : 1,
         "number_of_replicas" : 1
         },
     "analysis": {
         "filter": {
                 "english_stop": {
                 "type": "stop",
                 "stopwords": "_english_"
             },
                 "english_stemmer": {
                 "type": "stemmer",
                 "Language": "english"
             },
                 "english_possessive_stemmer": {
                 "type": "stemmer",
                 "Language": "possessive_english"
             }
     },
     "analyzer": {
             "english": {
                 "type": "custom",
                 "tokenizer": "standard",
                 "filter": [
                     "english_possessive_stemmer",
                     "lowercase",
                     "english_stop",
                     "english_stemmer"
                 ]
             }
         }
     }
 },
 "mappings": {
    "doc": {
      "properties": {
        "question": {
          "type": "text",
          "fields": {
            "english": {
              "type":     "text",
              "analyzer": "english"
            }
          }
        }
      }
    }
  }
}

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://chatbot:chatbot123@52.210.176.89:27017/chatbot"
mongo = PyMongo(app)

@app.route('/',methods=['GET'])
def main():

    question=request.args.get('q', "Does Korean stil eat dog?")
    return MLprocessing(question)

if __name__ == "__main__":
    print("==========reload start=========")
    questions = mongo.db.questions.find({})

    for question in questions :
        # print(question['_id'])
        # print(MLprocessing(question['text']))
        mongo.db.questions.update_one({'_id':question['_id']}, {'$set': {'category':MLprocessing(question['text'])}})

    try :
        # es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
        es = Elasticsearch(['https://vpc-chatbot-5a7mbd7a6rma5a6vltvnrfxbdu.eu-west-1.es.amazonaws.com:443'])
        if es.indices.exists(INDEX_NAME):
            print("Delete previous index")
            es.indices.delete(index=INDEX_NAME)
        print("Sleep")
        time.sleep(5)
        print("Start")
        es.indices.create(index=INDEX_NAME, body=INDEX_SETTINGS)
        time.sleep(5)
        questions = mongo.db.questions.find({'answer_count': { '$gte': 1 }})
        for question in questions :
            # print(question['text'])
            body =  {
                "question" : question['text'],
                "tags" : [question['target_country'].replace(" ", "").replace("-", ""), question['category'].replace(" ", "").replace("-", "")]
              }
            print(body)
            es.index(index=INDEX_NAME, doc_type=DOC_TYPE, id=question['_id'], body=body)
    except :
        print("It won't work in the local machine")
    print("==========reload done=========")
    app.run(debug=True, host='0.0.0.0', port=9000)
