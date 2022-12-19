from csv import reader
import pymongo
import time
import pandas as pd
import re
from pyspark.sql import SparkSession
from pyspark.context import SparkContext
from pyspark.sql.functions import split
from pyspark.sql.functions import col
from pyspark.sql.functions import lower
from pyspark.sql.functions import regexp_extract
from pyspark.sql.functions import length



daten= pd.read_csv('C:\\Users\\Jan\\Desktop\\group_membership.tsv', delimiter='\t')

print(daten)
datenalsdict = daten.to_dict('records')

t = time.perf_counter()
for i, item in enumerate(datenalsdict):
    mycol.insert_one(item)
    print (i)
print(f"Time expired for experiment 1: {time.perf_counter() - t} sec")

######################################################################################### 1.1Redis Cheatsheet
""""
# Redis Cheatsheet
# All the commands you need to know


redis-server /path/redis.conf  # start redis with the related configuration file
redis-cli                      # opens a redis prompt


# Strings.


APPEND key value                  # append a value to a key
BITCOUNT key [start end]          # count set bits in a string
SET key value                     # set value in key
SETNX key value                   # set if not exist value in key
SETRANGE key offset value         # overwrite part of a string at key starting at the specified offset
STRLEN key                        # get the length of the value stored in a key
MSET key value [key value ...]    # set multiple keys to multiple values
MSETNX key value [key value ...]  # set multiple keys to multiple values, only if none of the keys exist
GET key                           # get value in key
GETRANGE key value                # get a substring value of a key and return its old value
MGET key [key ...]                # get the values of all the given keys
INCR key                          # increment value in key
INCRBY key increment              # increment the integer value of a key by the given amount
INCRBYFLOAT key increment         # increment the float value of a key by the given amount
DECR key                          # decrement the integer value of key by one
DECRBY key decrement              # decrement the integer value of a key by the given number
DEL key                           # delete key

EXPIRE key 120                    # key will be deleted in 120 seconds
TTL key                           # returns the number of seconds until a key is deleted


# Lists.
# A list is a series of ordered values.


RPUSH key value [value ...]           # put the new value at the end of the list
RPUSHX key value                      # append a value to a list, only if the exists
LPUSH key value [value ...]           # put the new value at the start of the list
LRANGE key start stop                 # give a subset of the list
LINDEX key index                      # get an element from a list by its index
LINSERT key BEFORE|AFTER pivot value  # insert an element before or after another element in a list
LLEN key                              # return the current length of the list
LPOP key                              # remove the first element from the list and returns it
LSET key index value                  # set the value of an element in a list by its index
LTRIM key start stop                  # trim a list to the specified range
RPOP key                              # remove the last element from the list and returns it
RPOPLPUSH source destination          # remove the last element in a list, prepend it to another list and return it
BLPOP key [key ...] timeout           # remove and get the first element in a list, or block until one is available
BRPOP key [key ...] timeout           # remove and get the last element in a list, or block until one is available


# Sets.
# A set is similar to a list, except it does not have a specific order and each element may only appear once. 


SADD key member [member ...]     # add the given value to the set
SCARD key                        # get the number of members in a set
SREM key member [member ...]     # remove the given value from the set
SISMEMBER myset value            # test if the given value is in the set.
SMEMBERS myset                   # return a list of all the members of this set
SUNION key [key ...]             # combine two or more sets and returns the list of all elements
SINTER key [key ...]             # intersect multiple sets
SMOVE source destination member  # move a member from one set to another
SPOP key [count]                 # remove and return one or multiple random members from a set


# Sorted Sets
# A sorted set is similar to a regular set, but now each value has an associated score.
# This score is used to sort the elements in the set.


ZADD key [NX|XX] [CH] [INCR] score member [score member ...]  # add one or more members to a sorted set, or update its score if it already exists

ZCARD key                           # get the number of members in a sorted set
ZCOUNT key min max                  # count the members in a sorted set with scores within the given values
ZINCRBY key increment member        # increment the score of a member in a sorted set
ZRANGE key start stop [WITHSCORES]  # returns a subset of the sorted set
ZRANK key member                    # determine the index of a member in a sorted set
ZREM key member [member ...]        # remove one or more members from a sorted set
ZREMRANGEBYRANK key start stop      # remove all members in a sorted set within the given indexes
ZREMRANGEBYSCORE key min max        # remove all members in a sorted set, by index, with scores ordered from high to low
ZSCORE key member                   # get the score associated with the given mmeber in a sorted set

ZRANGEBYSCORE key min max [WITHSCORES] [LIMIT offset count]  # return a range of members in a sorted set, by score


# Hashes
# Hashes are maps between string fields and string values, so they are the perfect data type to represent objects.


HGET key field          # get the value of a hash field
HGETALL key             # get all the fields and values in a hash
HSET key field value    # set the string value of a hash field
HSETNX key field value  # set the string value of a hash field, only if the field does not exists

HMSET key field value [field value ...]  # set multiple fields at once

HINCRBY key field increment  # increment value in hash by X
HDEL key field [field ...]   # delete one or more hash fields
HEXISTS key field            # determine if a hash field exists
HKEYS key                    # get all the fields in a hash
HLEN key                     # get all the fields in a hash
HSTRLEN key field            # get the length of the value of a hash field
HVALS key                    # get all the values in a hash


# HyperLogLog
# HyperLogLog uses randomization in order to provide an approximation of the number of unique elements in a set using just a constant, and small, amount of memory


PFADD key element [element ...]  # add the specified elements to the specified HyperLogLog
PFCOUNT key [key ...]            # return the approximated cardinality of the set(s) observed by the HyperLogLog at key's)

PFMERGE destkey sourcekey [sourcekey ...]  # merge N HyperLogLogs into a single one


# Publication & Subscription


PSUBSCRIBE pattern [pattern ...]             # listen for messages published to channels matching the given patterns
PUBSUB subcommand [argument [argument ...]]  # inspect the state of the Pub/Sub subsystem
PUBLISH channel message                      # post a message to a channel
PUNSUBSCRIBE [pattern [pattern ...]]         # stop listening for messages posted to channels matching the given patterns
SUBSCRIBE channel [channel ...]              # listen for messages published to the given channels
UNSUBSCRIBE [channel [channel ...]]          # stop listening for messages posted to the given channels


# Other Commands


KEYS pattern  # find all keys matching the given pattern



"""
#connect to reddis  1.2 Redis Python Client

import redis

r = redis.Redis(host='localhost', port=6379, db=0)
red = redis.StrictRedis('localhost', 6379, charset="utf-8", decode_responses=True)
#set a key

r.set('foo', 'bar')

#get a key

itemausredis = r.get('foo')
itemausredis = itemausredis.decode("utf-8")
itemausredis = itemausredis.split(",")

#delete a key

r.delete('foo')

#set a key with an expiration

r.setex('foo', 30, 'bar')


##################################################################################################################### 2.1 MongoDB Cheat Sheet
"""
# MongoDB Cheat Sheet

## Connect in Docker

docker exec -it mongoContainer mongo

## Show All Databases

```
show dbs
```

## Show Current Database

```
db
```

## Create Or Switch Database

```
use acme
```

## Drop

```
db.dropDatabase()
```

## Create Collection

```
db.createCollection('posts')
```

## Show Collections

```
show collections
```

## Insert Row

```
db.posts.insert({
  title: 'Post One',
  body: 'Body of post one',
  category: 'News',
  tags: ['news', 'events'],
  user: {
    name: 'John Doe',
    status: 'author'
  },
  date: Date()
})
```

## Insert Multiple Rows

```
db.posts.insertMany([
  {
    title: 'Post Two',
    body: 'Body of post two',
    category: 'Technology',
    date: Date()
  },
  {
    title: 'Post Three',
    body: 'Body of post three',
    category: 'News',
    date: Date()
  },
  {
    title: 'Post Four',
    body: 'Body of post three',
    category: 'Entertainment',
    date: Date()
  }
])
```

## Get All Rows

```
db.posts.find()
```

## Get All Rows Formatted

```
db.posts.find().pretty()
```

## Find Rows

```
db.posts.find({ category: 'News' })
```

## Sort Rows

```
# asc
db.posts.find().sort({ title: 1 }).pretty()
# desc
db.posts.find().sort({ title: -1 }).pretty()
```

## Count Rows

```
db.posts.find().count()
db.posts.find({ category: 'news' }).count()
```

## Limit Rows

```
db.posts.find().limit(2).pretty()
```

## Chaining

```
db.posts.find().limit(2).sort({ title: 1 }).pretty()
```

## Foreach

```
db.posts.find().forEach(function(doc) {
  print("Blog Post: " + doc.title)
})
```

## Find One Row

```
db.posts.findOne({ category: 'News' })
```

## Find Specific Fields

```
db.posts.find({ title: 'Post One' }, {
  title: 1,
  author: 1
})
```

## Update Row

```
db.posts.update({ title: 'Post Two' },
{
  title: 'Post Two',
  body: 'New body for post 2',
  date: Date()
},
{
  upsert: true
})
```

## Update Specific Field

```
db.posts.update({ title: 'Post Two' },
{
  $set: {
    body: 'Body for post 2',
    category: 'Technology'
  }
})
```

## Increment Field (\$inc)

```
db.posts.update({ title: 'Post Two' },
{
  $inc: {
    likes: 5
  }
})
```

## Rename Field

```
db.posts.update({ title: 'Post Two' },
{
  $rename: {
    likes: 'views'
  }
})
```

## Delete Row

```
db.posts.remove({ title: 'Post Four' })
```

## Sub-Documents

```
db.posts.update({ title: 'Post One' },
{
  $set: {
    comments: [
      {
        body: 'Comment One',
        user: 'Mary Williams',
        date: Date()
      },
      {
        body: 'Comment Two',
        user: 'Harry White',
        date: Date()
      }
    ]
  }
})
```

## Find By Element in Array (\$elemMatch)

```
db.posts.find({
  comments: {
     $elemMatch: {
       user: 'Mary Williams'
       }
    }
  }
)
```

## Add Index

```
db.posts.createIndex({ title: 'text' })
```

## Text Search

```
db.posts.find({
  $text: {
    $search: "\"Post O\""
    }
})
```

## Greater & Less Than

```
db.posts.find({ views: { $gt: 2 } })
db.posts.find({ views: { $gte: 7 } })
db.posts.find({ views: { $lt: 7 } })
db.posts.find({ views: { $lte: 7 } })
```

"""

#connect to mongodb 2.2 MongoDB Python client

import pymongo

#create a array of data to insert

data = [{'name': 'foo', 'value': 'bar'}, {'name': 'foo2', 'value': 'bar2'}]

#create 100 data entries

for i in range(100):
    data.append({'name': 'foo' + str(i), 'value': 'bar' + str(i)})

#connect to mongodb
client = pymongo.MongoClient('localhost', 27017)

#connect to database
db = client['test-database']

#connect to collection
collection = db['test-collection']

#insert a document

collection.insert_one({'x': 1})

#insert multiple documents

collection.insert_many(data)

#find a document

collection.find_one({'x': 1})

#find multiple documents

collection.find({'x': {'$gt': 1}})

#update a document

collection.update_one({'x': 1}, {'$set': {'x': 2}})

#update multiple documents

collection.update_many({'x': 1}, {'$set': {'x': 2}})

#delete a document

collection.delete_one({'x': 2})

#delete multiple documents

collection.delete_many({'x': 2})

############################################################################################################# 2.3 MongoDB Python pipelining
#Pipelines
import pprint

pipeline=[
    # die match-Klausel ist fuer Aufgabe 1b - nur Sprachkombis, die mit "English" anfangen und die Anzahl der Sprachkombis und diese sortiert nach Anzahl
    {
        '$match': {
            'language': { '$regex': "^English" }
        }
    },
    {
        '$group': {
            '_id': "$language",
            'cnt': { '$sum': 1 },
            # 'cntcnt': { '$count': {}}
        }
    },
        {
        '$sort': { "cnt": -1 }
    }
]

pprint.pprint(list(collection.aggregate(pipeline)))

#das gleiche nur mit einem befehl
pipelineSBC=[
    {
        '$sortByCount': "$language"
    }
]

#max und min pipeline
pipelineMax=[
    {
        '$group': { 
            '_id': 'Maximum',
            'maxYear': { '$max': "$year" },
            'minYear': { '$min': "$year" }
        }
    }
]
pprint.pprint(list(client.mflix.movies_initial.aggregate(pipelineMax)))

#alle einträge von id und year ausgeben. Der rest wird nicht mit ausgegeben.
pipelineFindAll=[
    {
        '$project': { '_id': 1, 'year': 1 }
    }
]
allEntries=list(client.mflix.movies_initial.aggregate(pipelineFindAll))
# printe zum Testen einen Entry aus
print(allEntries[0])

#update alle einträge, die länger als 4 stellig sind und wandle sie in int um.
for e in allEntries:
    if isinstance(e["year"], str):
        updateStringID = { '_id': e["_id"] }
        updateStringDate = { '$set': { 'year': int(e["year"][0:4])}}
        pprint.pprint(f"Update {e['year']} -> {updateStringID}, {updateStringDate}")
        client.mflix.movies_initial.update_one(updateStringID, updateStringDate)

#bearbeitung mit ausgabe in andere collection
zweitausenderShortsPipeline = [
    { 
        '$unwind': '$genre'
    },
    {   
        '$match': { 
            "year": { '$gt': 1999 },
            "genre": "Short"
        }
    },
    {
        '$set': { '_id': '$title' }
    },
    {
        '$project': { 
            # warum brauche ich hier den titel nicht? (A: weil das jetzt die ID ist!)
            'year': 1,
        }
    },
    {
        '$sort': { '_id': 1 }
    },
    {
        '$out': { 'db': 'ShortMovies', 'coll': '2000er' }
    }
]
print(f"Die Anzahl von Filmen ist { len(list(client.mflix.movies_initial.aggregate(zweitausenderShortsPipeline))) }")
##################################################################################################################### 3.1 Spark

"""
Spark Cheat Sheet
"""

spark = SparkSession.builder \
      .master("local[1]") \
      .appName("Datenbanken mit Spark") \
      .getOrCreate()


dataframe = spark.read.option("delimiter", "\t").option("header","true").csv('data.tsv')
dataframe2 = spark.read.option("delimiter", "\t").option("header","true").csv('data_1.tsv')

dataframe.show(10)
dataframe2.show(10)


dataframezusammen= dataframe.join(dataframe2, ["tconst"])
dataframezusammen.show(10)


dataframezusammen.select("tconst","originalTitle","averageRating","numVotes").where(dataframezusammen.averageRating >= 5.0).show(10)


datatopandas = dataframezusammen.toPandas()

datatodict = datatopandas.to_dict("records")

datatopandas.to_json('data.json', orient='records', force_ascii=False, lines=True)

# und wenn wir auf das Schema direkt zugreifen wollen, dann gibt es alternativ die dtypes
print(frank.dtypes)
print(f"Ist das Element == 'string': { frank.dtypes[0][1] == 'string'}") # Das string kann auch durch int, float, etc. ersetzt werden

from pyspark.sql.functions import split
lines = frank.select(split(frank.value, " ").alias("Zeile"))
lines.show(10, truncate=100)

lines = frank.select(split(frank.value, "[^a-zA-Z]").alias("Zeile"))
lines.show(100, truncate=False)

# Spalte selektieren geht auf viele Arten:
lines.select(lines.Zeile).show()
lines.select("Zeile").show()
from pyspark.sql.functions import col
lines.select(col("Zeile")).show()

# Packt die einzelnen Wörter in eine Spalte
from pyspark.sql.functions import explode, col
words = lines.select(explode(col("Zeile")).alias("word"))
words.show(15)

# Alles in Kleinbuchstaben
from pyspark.sql.functions import lower
words_lower = words.select(lower(col("word")).alias("word_lower"))
words_lower.show(truncate = False)

# weg mit den kurzen Zeilen bitte
from pyspark.sql.functions import regexp_extract
# minimum laenge 2 Zeichen ausser dem Wort "a" und "I"
words_clean = words_lower.select(regexp_extract(col("word_lower"), "[a-z]{2,}|a|i", 0).alias("echtesWort"))
words_clean.show(truncate = False)

# oder mein weg ohne a und i drinlassen
from pyspark.sql.functions import length
mind2zeichen = words.where(length(col("lower(Zeilen)"))>=2)
mind2zeichen.show(10,truncate=False)

# weg mit den leeren Zeilen bitte
proper_words = words_clean.filter(col("echtesWort") != "")
proper_words.show()

#soll alles mit any* rauswerfen klappt aber glaub nicht so richtig
proper_words_any = words_clean.filter(col("echtesWort") != "any*")
proper_words_any.show()

#entfernen von "is" oder einem anderen Wort
words_nonull = words_clean.where(col("word") != "is")

#nochmal alle kleinen wörter rauswerfen
# geht auch mit regex
#words_clean = words_lower.select(
#    regexp_extract(col("word_lower"), "[a-z]{3+}", 0).alias("word")
#)

#checken wie viel spalten keine strings enthalten
cnt = 0
for x, y in datenA2.dtypes:
    if y != 'string':
        cnt += 1
print(f'cnt = {cnt}')
#oder kurz
print(len([x for x, y in datenA2.dtypes if y != "string"]))
#kann denk ich auch verwendet werden zum zählen wie viel strings etc es gibt

#Die ganzen spezifizierten wörter entfernen
exclDict = ["is", "not", "if", "the", "for", "of", "no", "at", "and"]
words_no_dict = words_nonull.where(~col("word").isin(exclDict))
words_no_dict.show()
#mein weg
words_isin = mind3zeichen.filter(col("lower(Zeilen)").isin(exclDict)==False)
words_isin.show()

# gruppieren
groups = words_nonull.groupby(col("word"))
print(groups)
wordCounts = groups.count()
wordCounts.printSchema()
wordCounts.show()

#die Anzahl der Worte per Anzahl Buchstaben (also: wie viele Worte mit 1, 2, 3, ... Buchstaben
from pyspark.sql.functions import length
# words_nonull.groupBy(col("word")).count().select("count").alias("len").groupBy(col("len")).count().show()
words_nonull.select(length(col("word")).alias("length")).groupBy("length").count().orderBy(col("length").asc()).show()
#2 alternativen für das oderby
wordCount.orderBy("count", ascending = False).show()
wordCount.orderBy(col("count").desc()).show()

#dataframe in csv auf patte schreiben
words_nonull.coalesce(1).write.csv("frankenCoalesce1.csv")

#cleanup

from pyspark.sql import SparkSession
import pyspark.sql.functions as F


spark = SparkSession.builder.appName(
    "Counting word occurences from a book."
).getOrCreate()

spark.sparkContext.setLogLevel("WARN")

# If you need to read multiple text files, replace `1342-0` by `*`.
results = (
    spark.read.text("frankenstein.txt")
    .select(F.split(F.col("value"), " ").alias("line"))
    .select(F.explode(F.col("line")).alias("word"))
    .select(F.lower(F.col("word")).alias("word"))
    .select(F.regexp_extract(F.col("word"), "[a-z']*", 0).alias("word"))
    .where(F.col("word") != "")
    .groupby(F.col("word"))
    .count()
)

results.orderBy("count", ascending=False).show(10)
results.coalesce(1).write.csv("./results_single_partition.csv")


############################################################################################################ 4.1 Key-Value Stores
"""
1.	Was ist denn nun ein key-value-store genau?
a.	Values werden abgespeichert mit einem einzigartigen Wert, dem Key

2.	Nenne 3 verschiedene Key-Value Datenbanksysteme
a.	Redis, Riak, Amazon DynamoDB

3.	Was ist der Unterschied zu einer Document-Database?
a.	Bei einer Document-Database enthält die Value Dateien, welche mit code gelesen und bearbeitet werden können

4.	Bezüglich des "C" in ACID - was ist der Hauptunterschied zu relationalen Datenbanken?
a.	C = Consitent, eine NoSQL Datenbank muss nicht zu jedem Zeitpunkt consistent sein.
Man kann bei einer einem key-value Datenbank alle daten einfach speichern. Bei einer Relationalen Datenbank kann man immer nur in einer spalte feste Datentype seichern.

5.	welche Normalformen gibt es bei Key-Value-Datenbanken?
a.	Da bei Key-Vale-Datenbanken nur sehr einfache Beziehungen dargestellten werden können ist es ist es schwer von einer Normalform zu sprechen.

6.	Welche Datentypen sind akzeptabel als Key? Was ist der Hauptindex für Key-Value Datenbanken, welchen Datentyp hat er, und wie viele andere Indices kann eine KV-Datenbank haben?
a.	Typ: Binary sequence -> jeder datentyp + empty key
b.	 Balanced tree
c.	Keine weil man über den key zugreifen soll

7.	angenommen wir haben eine Studentendatenbank (Key-Value), wo der Key die Matrikelnummer ist, und der Value die wichtigen Daten wie Name und Lieblingsbier. Mit welcher Suchmöglichkeit kann man alle Studis finden, die gerne Guinness trinken?
a.	Linear-search O(n -> n)

8.	warum bietet sich bei einem Online-Warenkorb (mit großen Umsatzzahlen natürlich, wie z.B. Amazon) eher eine key-Value Datenbank an um den Inhalt des Warenkorbs zu speichern, anstatt einer relationalen Datenbank? "weil es schneller ist" reicht nicht als Antwort. Sei ganz spezifisch!
a.	Eine Key-Value Datenbank kommt mit sehr viel mehr Transaktionen klar als eine rationale Datenbank, alle Warenkörbe eines Onlineshops ändern deren inhalt zu oft, als das eine rationale Datenbank hinterher kommt denn dort werden mindestens 3 tabellen benötigt. Also mindestens 2 joins. Diese sind „teuer“.

9.	Ist Windows Explorer eine key-value-Datenbank?
a.	Der Windows-Explorer würde eher einer Document-Database entsprechen. Ist aber eigentlich ehr ein Browser.

10.	Einer der Artikel behauptet: "key-value stores are not considered suitable for applications requiring frequent updates". Ist das nicht genau das Gegenteil von der Aussage in Aufgabe 8 (Warenkörbe, Session-Daten, usw..). Diskutiere, was hier abgeht/wer Recht hat/was das eigentliche Problem ist!
a.	Eine Key-Value Datenbank kann keine “Updates” an den Daten Vornehmen. Man kann die Daten nur Schreiben, Lesen und Löschen. Will man also ein “Update” vornehmen muss man es Lesen bearbeiten speichern und dann das alte löschen.

11.	Nenne 5 verschiedene Anwendungen wo Key-Value-Datenbanken Vorteile gegenüber Relationalen Datenbanken haben, und beschreibe spezifisch für jeden Fall, was genau der Vorteil ist (und: was potentielle Nachteile sind)
a.	Warenkorb: daten können für die benötigte zeit gespeichert und später einfach gelöscht werden
b.	Session Daten: daten können für die benötigte zeit gespeichert und später einfach gelöscht werden
c.	Caching: Es muss eine stuktur für die daten angegeben werden (-> leichte und schnelle nutzung)
d.	Quick & Dirty Lösungen: Es muss eine stuktur für die daten angegeben werden (-> leichte und schnelle nutzung)
e.	

12.	Be- oder widerlege die folgende Aussage (idealerweise an Hand eines Beispiels) "Dokumentendatenbanken sind das Gleiche wie Kev-Value Datenbanken"
a.	Key-Value Datenbanken können einen beliebigen Value abspeichern, also mit beliebigem Value-Aufbau; Document-Databases sind spezialisiert auf Dokumente und besitzen dadurch mehr Struktur

13.	Erkläre an Hand eines Beispiels was die Auswirkungen sind, wenn man im laufenden Betrieb die Feldstruktur einer KV-Datenbank verändert, und vergleiche es mit dem, was analog bei einer relationalen Datenbank passieren würde
a.	Bei einer KV-Datenbank kann man so gut wie jede Art von Daten gemischt speichern. Bei einer relationalen Datenbank muss der Datentyp spezifiziert werden. Also ist ein einfacher Wechsel nicht möglich.


14.	Mit welchem Kommando wird in Redis eine Datenbank erzeugt (analog zu "CREATE" in SQL)
a.	Es gibt kein create in Redis. Jede Redis Datenbank Instanz ist eine DB. Evl. Kann man mit Hashing mehere “Tabellen” erstellen in dem man immer denselben Hash verwendet. Man kann auch zwischen 16 Datastores wechseln mit : “select *index*”

15.	Wie viele verschiedene Datentypen kann Redis abspeichern?
a.	Strings
b.	Lists
c.	Sets
d.	Hashes
e.	Sorted sets
f.	Streams
g.	Geospatial
h.	HyperLogLog
i.	Bitmaps
j.	Bitfields

16.	Redis ist eine in-________ Datenbank, und daher besonders schnell.
a.	memory

17.	Was für Fragen ergeben sich aus der vorhergehenden Frage?
a.	Ist Redis schneller als eine Datenbank auf Festspeicher? Antwort Denke schon. RAM = Fast
"""
############################################################################################################