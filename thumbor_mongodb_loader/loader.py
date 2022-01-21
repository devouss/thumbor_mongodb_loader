#!/usr/bin/python
# -*- coding: utf-8 -*-
# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
from tornado import gen
from pymongo import MongoClient
from bson.objectid import ObjectId
import gridfs
import urllib
import logging
from thumbor.loaders import LoaderResult

def __conn__(self):
    logging.warning('1')
    the_database = self.config.MONGO_ORIGIN_SERVER_DB
    if urllib.parse.quote_plus(self.config.MONGO_ORIGIN_SERVER_USER):
        password = urllib.parse.quote_plus(self.config.MONGO_ORIGIN_SERVER_PASSWORD)
        user = urllib.parse.quote_plus(self.config.MONGO_ORIGIN_SERVER_USER)
        uri = 'mongodb://'+ user +':' + password + '@' + self.config.MONGO_ORIGIN_SERVER_HOST + '/?authSource=' + self.config.MONGO_ORIGIN_SERVER_DB
    else:
        uri = 'mongodb://'+ self.config.MONGO_ORIGIN_SERVER_HOST
    client = MongoClient(uri)
    #database
    db = client[self.config.MONGO_ORIGIN_SERVER_DB]
    logging.warning(db)
    return db

@gen.coroutine
def load(self, path):
    logging.warning('2')
    db = __conn__(self)
    words2 = path.split("/")
    storage = self.config.MONGO_ORIGIN_SERVER_COLLECTION
    images = gridfs.GridFS(db, collection=storage)
    result = LoaderResult()
    logging.warning(words2)
    if ObjectId.is_valid(words2[0]):
        if images.exists(ObjectId(words2[0])):
            logging.warning('ObjectId(words2[0])========>  ', ObjectId(words2[0]))
            contents = images.get(ObjectId(words2[0])).read()
            logging.warning('contents heeeererre ')
            result.successful = True
            result.buffer = contents
            logging.warning('contents  ', contents)
        else:
            result.error = LoaderResult.ERROR_NOT_FOUND
            result.successful = False
    else:
        result.error = LoaderResult.ERROR_NOT_FOUND
        result.successful = False
    logging.warning('result.successful =++++++=> ', result.successful)
    raise gen.Return(result)
