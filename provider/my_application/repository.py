
# Copyright 2020 Nedeljko Radulovic, Dihia Boulegane, Albert Bifet
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import sys
from pymongo import MongoClient
from datetime import datetime, timedelta
import logging
logging.basicConfig(level='DEBUG')


class MongoRepository:
    client = None

    def __init__(self, mongo_host):
        try:
            self.client = MongoClient(mongo_host, 27017)
        except Exception as e:
            sys.stderr.write(str(e))

    def create_database(self, db_name):
        """
        Create a database in MongoDB
        :param db_name: Name of the database
        :return:
        """
        db = self.client[db_name]
        return db

    def create_collection(self, db_name, collection_name):
        """
        Create collection inside database db_name.
        :param db_name: Name of the database
        :param collection_name: name of the collection
        :return:
        """
        db = self.client[db_name]
        collection = db[collection_name]
        return collection

    def insert_document(self, db_name, collection_name, document):
        """
        Insert a document in collection (collection_name) in database (db_name).

        :param db_name: Database name
        :param collection_name: Collection name
        :param document: json document
        :return:
        """
        db = self.client[db_name]
        collection = db[collection_name]
        collection.insert_one(document)

    def get_competition_data_records(self, competition_id):
        """
        Fetch the datastream.

        :param competition_id: Competition ID
        :return: Datastream where each record(row) is a dictionary
        """
        db = self.client['data']
        collection = db['data']
        results = collection.find_one({"competition_id": competition_id})
        return results

    def get_competition_evaluation_measures(self, competition_id):
        """
        Fetch the evaluation metrics for a given competition.
        :param competition_id: Competition ID
        :return: List of metrics
        """
        db = self.client['evaluation_measures']
        collection = db['evaluation_measures']

        results = collection.find_one({"competition_id": int(competition_id)})
        data = []

        record = {}
        record['competition_id'] = results['competition_id']
        record['measures'] = results['measures']

        return record

    def get_standard_evaluation_measures(self):
        """
        Retrieve the standard set of evaluation metrics offered on the platform.
        :return: List of measures (by name: MSE, MAPE, ACC...)
        """
        db = self.client['evaluation_measures']
        collection = db['standard_measures']

        measures = collection.find({})
        data = []

        # print(measures)
        for m in measures:
            # print(m)
            data.append(m['name'])

        return data

    def get_results_by_user(self, competition_id, field, measure, user_id):
        """
        Fetch evaluation metric values for a given user and competition.
        :param competition_id: Competition ID
        :param field: Label column name
        :param measure: Evaluation metric
        :param user_id: User ID
        :return: Dictionary with the computed evaluation metric for a given user
        """

        db = self.client['evaluation_measures']
        collection = db['measures']
        """
        res = collection.find()
        for r in res : 
            print('INIT',r)"""

        results = collection.aggregate([
            {"$match": {"$and":
                [
                    {"competition_id": int(competition_id)},
                    {'user_id': {"$in": [0, int(user_id)]}}

                ]}
            },

            {
                "$group":
                    {
                        "_id": "$user_id",
                        "measures": {"$push": "$$ROOT"}
                    }
            },
            {
                "$project": {
                    "measures.competition_id": 0,
                    "measures._id": 0
                }
            },
            {"$sort": {"_id": 1}}

        ])

        final_stats = []
        for r in results:
            stats = {'user_id': r['_id'], 'results': []}
            measures = r['measures']
            for m in measures:
                start_date = m['start_date']
                end_date = m['end_date']
                center_date = start_date + (end_date - start_date) / 2

                year = str(center_date.year)
                month = str(center_date.month)
                day = str(center_date.day)
                hour = str(center_date.hour)
                minute = str(center_date.minute)
                second = str(center_date.second)

                row = {"label": {"Year": year, "Month": month, "Day": day, "Hour": hour, "Minute": minute,
                                 "Second": second},
                       "data": m['measures'][str(field)][str(measure)]}

                stats['results'].append(row)
            stats['results'] = sorted(stats['results'],
                                      key=lambda i: datetime(**{k.lower(): int(v) for k, v in i['label'].items()}))
            final_stats.append(stats)

        if len(final_stats) > 1:
            # get baseline results (x-axis)
            base_line_results = [r for r in final_stats if r['user_id'] == 0][0]
            user_results = [r for r in final_stats if r['user_id'] != 0][0]

            base_line_dates = [r['label'] for r in base_line_results['results']]
            user_line_dates = [r['label'] for r in user_results['results']]
            # Filling missing dates with zeros
            for i in range(len(base_line_dates)):
                if base_line_dates[i] not in user_line_dates:
                    # add this missing date at this index
                    user_results['results'].insert(i, {'label': base_line_dates[i], 'data': str(0)})
            final_stats = [base_line_results, user_results]

        for r in final_stats:
            r['user_id'] = 'Baseline' if r['user_id'] == 0 else 'You'

        return final_stats

    def get_last_predictions_by_user(self, competition_id, now, field, measure, user_id, evaluation_time_interval):
        """
        NOT USED!

        Retrieve the latest predictions sent by user.
        :param competition_id:
        :param now:
        :param field:
        :param measure:
        :param user_id:
        :param evaluation_time_interval:
        :return: Dictionary with the computed evaluation metric for a given user
        """
        db = self.client['evaluation_measures']
        collection = db['measures']

        date = now - timedelta(seconds=35)
        results = collection.aggregate([
            {"$match": {"$and":
                [
                    {"competition_id": int(competition_id)},
                    {"start_date": {"$gte": date, "$lt": now}},
                    {'user_id': {"$in": [0, int(user_id)]}}

                ]}
            },

            {
                "$group":
                    {
                        "_id": "$user_id",
                        "measures": {"$push": "$$ROOT"}
                    }
            },
            {
                "$project": {
                    "measures.competition_id": 0,
                    "measures._id": 0
                }
            },
            {"$sort": {"_id": 1}}

        ])

        final_stats = []
        for r in results:
            stats = {'user_id': r['_id'], 'results': []}
            measures = r['measures']
            for m in measures:
                start_date = m['start_date']
                end_date = m['end_date']
                center_date = start_date + (end_date - start_date) / 2

                year = str(center_date.year)
                month = str(center_date.month)
                day = str(center_date.day)
                hour = str(center_date.hour)
                minute = str(center_date.minute)
                second = str(center_date.minute)

                # TODO : Determine which field, which value
                row = {"label": {"Year": year, "Month": month, "Day": day, "Hour": hour, "Minute": minute,
                                 "Second": second},
                       "data": m['measures'][str(field)][str(measure)]}

                stats['results'].append(row)
            # stats['results'] = sorted(stats['results'], key=lambda i: str(i['label']))
            stats['results'] = sorted(stats['results'],
                                      key=lambda i: datetime(**{k.lower(): int(v) for k, v in i['label'].items()}))
            final_stats.append(stats)

        if len(final_stats) > 1:
            # get baseline results (x-axis)
            base_line_results = [r for r in final_stats if r['user_id'] == 0][0]
            user_results = [r for r in final_stats if r['user_id'] != 0][0]

            base_line_dates = [r['label'] for r in base_line_results['results']]
            user_line_dates = [r['label'] for r in user_results['results']]
            # Filling missing dates with zeros
            for i in range(len(base_line_dates)):
                if base_line_dates[i] not in user_line_dates:
                    # add this missing date at this index
                    user_results['results'].insert(i, {'label': base_line_dates[i], 'data': str(0)})
            final_stats = [base_line_results, user_results]

        for r in final_stats:
            r['user_id'] = 'Baseline' if r['user_id'] == 0 else 'You'
        return final_stats

    def get_users_ranking_by_field_by_measure(self, competition_id, field, measure):
        """
        Retrieve rankings of users for a specific label column and evaluation metric.
        :param competition_id: Competition ID
        :param field: Label column name
        :param measure: Evaluation metric
        :return: List of dictionary with the computed evaluation metric for all users
        """

        db = self.client['evaluation_measures']
        collection = db['measures']

        results = collection.aggregate([
            {"$match": {"$and":
                [
                    {"competition_id": int(competition_id)}

                ]}
            },

            {"$sort": {"user_id": 1, "end_date": -1}},
            {
                "$group":
                    {
                        "_id": "$user_id",
                        "end_date": {"$first": "$end_date"},
                        "measures": {"$first": "$measures"}
                    }
            },
            {
                "$project": {
                    "measures.competition_id": 0,
                    "measures._id": 0
                }
            }

        ])

        data = []
        for r in results:
            # print (r)
            item = {}
            item['id'] = r['_id']
            item['measures'] = r['measures'][field][measure]
            data.append(item)

        return data

    def insert_standard_measures(self, standard_measures):
        """
        Store standard set of evaluation metrics.
        :param standard_measures: list of metrics
        :return:
        """
        db = self.client['evaluation_measures']
        collection = db['standard_measures']
        measures = collection.find({})
        existing_measures = []
        for m in measures:
            existing_measures.append(m)

        for measure in standard_measures:
            insert = True
            for m in existing_measures:
                if m['name'] == measure['name']:
                    insert = False
            if insert:
                collection.insert_one(measure)