import random

#Added AnonymousUser
from django.contrib.auth.models import User, AnonymousUser

#Added RequestFactory to handle the request.user.is_staff check in the views
from django.test import RequestFactory
#Added these Middleware to simulate the messages, since RequestFactory doesn't do it
from django.contrib.messages.middleware import MessageMiddleware
from django.contrib.sessions.middleware import SessionMiddleware

from rest_framework.test import APIClient

from .models import Census
#Added the necessary models
from voting.models import Voting, Question, QuestionOption
from base import mods
from base.tests import BaseTestCase
import os

from .views import exporting_census, importing_census, add_to_census, remove_from_census
import csv



class CensusTestCase(BaseTestCase):

    def setUp(self):
        super().setUp()
        self.census = Census(voting_id=1, voter_id=1)
        self.census.save()

    def tearDown(self):
        super().tearDown()
        self.census = None

    def test_check_vote_permissions(self):
        response = self.client.get('/census/{}/?voter_id={}'.format(1, 2), format='json')
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), 'Invalid voter')

        response = self.client.get('/census/{}/?voter_id={}'.format(1, 1), format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), 'Valid voter')

    def test_list_voting(self):
        response = self.client.get('/census/?voting_id={}'.format(1), format='json')
        self.assertEqual(response.status_code, 401)

        self.login(user='noadmin')
        response = self.client.get('/census/?voting_id={}'.format(1), format='json')
        self.assertEqual(response.status_code, 403)

        self.login()
        response = self.client.get('/census/?voting_id={}'.format(1), format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'voters': [1]})

    def test_add_new_voters_conflict(self):
        data = {'voting_id': 1, 'voters': [1]}
        response = self.client.post('/census/', data, format='json')
        self.assertEqual(response.status_code, 401)

        self.login(user='noadmin')
        response = self.client.post('/census/', data, format='json')
        self.assertEqual(response.status_code, 403)

        self.login()
        response = self.client.post('/census/', data, format='json')
        self.assertEqual(response.status_code, 409)

    def test_add_new_voters(self):
        data = {'voting_id': 2, 'voters': [1,2,3,4]}
        response = self.client.post('/census/', data, format='json')
        self.assertEqual(response.status_code, 401)

        self.login(user='noadmin')
        response = self.client.post('/census/', data, format='json')
        self.assertEqual(response.status_code, 403)

        self.login()
        response = self.client.post('/census/', data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(len(data.get('voters')), Census.objects.count() - 1)

    def test_destroy_voter(self):
        data = {'voters': [1]}
        response = self.client.delete('/census/{}/'.format(1), data, format='json')
        self.assertEqual(response.status_code, 204)
        self.assertEqual(0, Census.objects.count())


class CensusAddRemove(BaseTestCase):
    def setUp(self):
        super().setUp()

        self.q = Question(desc='test question')
        self.q.save()
        for i in range(5):
            self.opt = QuestionOption(question=self.q, option='option {}'.format(i+1))
            self.opt.save()
        self.v = Voting(name='test voting', question=self.q)
        self.v.save()

        self.voter = User(username='test_user')
        self.voter.save()

        user_admin = User.objects.get(username="admin")
        self.census = Census(voting_id=self.v.id, voter_id=user_admin.id)
        self.census.save()

        self.factory = RequestFactory()
        self.sm = SessionMiddleware()
        self.mm = MessageMiddleware()

    def tearDown(self):
        super().tearDown()
        self.census = None

        self.q = None
        self.opt = None
        self.v = None
        self.voter = None

        self.factory = None
        self.sm = None
        self.mm = None

    def test_create_census_from_gui(self):
        self.user = AnonymousUser()
        data = {'voting-select': self.v.id, 'user-select': self.voter.id}
        request = self.factory.post('/census/add/add_to_census/', data, format='json')
        self.sm.process_request(request)
        self.mm.process_request(request)
        request.user = self.user
        response = add_to_census(request)
        self.assertEqual(response.status_code, 401)

        user_admin = User.objects.get(username="admin")
        self.user = user_admin
        existing_censuss = Census.objects.count()
        data = {'voting-select': self.v.id, 'user-select': self.voter.id}
        request = self.factory.post('/census/add/add_to_census/', data, format='json')
        self.sm.process_request(request)
        self.mm.process_request(request)
        request.user = self.user
        response = add_to_census(request)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(existing_censuss+1, Census.objects.count())
        self.assertTrue(Census.objects.all().filter(voting_id=self.v.id, voter_id=self.voter.id).exists())

        user_admin = User.objects.get(username="admin")
        self.user = user_admin
        existing_censuss = Census.objects.count()
        data = {'voting-select': self.v.id, 'user-select': self.voter.id}
        request = self.factory.post('/census/add/add_to_census/', data, format='json')
        self.sm.process_request(request)
        self.mm.process_request(request)
        request.user = self.user
        response = add_to_census(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(existing_censuss, Census.objects.count())


    def test_delete_census_from_gui(self):
        user_admin = User.objects.get(username="admin")

        self.user = AnonymousUser()
        data = {'voting-select': self.v.id, 'user-select': user_admin.id}
        request = self.factory.post('/census/remove/remove_from_census/', data, format='json')
        self.sm.process_request(request)
        self.mm.process_request(request)
        request.user = self.user
        response = remove_from_census(request)
        self.assertEqual(response.status_code, 401)


        self.user = user_admin
        existing_censuss = Census.objects.count()
        data = {'voting-select': self.v.id, 'user-select': user_admin.id}
        request = self.factory.post('/census/remove/remove_from_census/', data, format='json')
        self.sm.process_request(request)
        self.mm.process_request(request)
        request.user = self.user
        response = remove_from_census(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(existing_censuss-1, Census.objects.count())
        self.assertFalse(Census.objects.all().filter(voting_id=self.v.id, voter_id=user_admin.id).exists())

        user_admin = User.objects.get(username="admin")
        self.user = user_admin
        existing_censuss = Census.objects.count()
        data = {'voting-select': self.v.id, 'user-select': user_admin.id}
        request = self.factory.post('/census/add/add_to_census/', data, format='json')
        self.sm.process_request(request)
        self.mm.process_request(request)
        request.user = self.user
        response = remove_from_census(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(existing_censuss, Census.objects.count())

class CensusExportImport(BaseTestCase):
    def setUp(self):
        super().setUp()

        self.q = Question(desc='test question')
        self.q.save()
        for i in range(5):
            self.opt = QuestionOption(question=self.q, option='option {}'.format(i+1))
            self.opt.save()
        self.v = Voting(name='test voting', question=self.q)
        self.v.save()

        self.voter = User(username='test_user')
        self.voter.save()

        self.census = Census(voting_id=self.v.id, voter_id=self.voter.id)
        self.census.save()

        self.factory = RequestFactory()
        self.sm = SessionMiddleware()
        self.mm = MessageMiddleware()

    def tearDown(self):
        super().tearDown()
        self.census = None

        self.q = None
        self.opt = None

        if os.path.exists('./census/export/export_' + self.v.name + '.csv'):
            os.remove('./census/export/export_' + self.v.name + '.csv')

        if os.path.exists('./census/export/import_test.csv'):
            os.remove('./census/export/import_test.csv')

        self.v = None
        self.voter = None
        self.factory = None
        self.sm = None
        self.mm = None

        self.file = None

    def test_export_census(self):
        self.user = AnonymousUser()
        data = {'voting-select': self.v.id}
        request = self.factory.post('/census/export/exporting_census/', data, format='json')
        self.sm.process_request(request)
        self.mm.process_request(request)
        request.user = self.user
        response = exporting_census(request)
        self.assertEqual(response.status_code, 401)
        self.assertFalse(os.path.exists('./census/export/export_' + self.v.name + '.csv'))

        user_admin = User.objects.get(username="admin")
        self.user = user_admin
        data = {'voting-select': self.v.id}
        request = self.factory.post('/census/export/exporting_census/', data, format='json')
        self.sm.process_request(request)
        self.mm.process_request(request)
        request.user = self.user
        response = exporting_census(request)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(os.path.exists('./census/export/export_' + self.v.name + '.csv'))
        with open('./census/export/export_' + self.v.name + '.csv', 'r') as csvfile:
            self.assertEqual(2, len(csvfile.readlines()))

             
    def generate_import_csv(self):
        #Creates a csv file with a row containing the user admin
        try:
            user_admin = User.objects.get(username="admin")
            self.file = open('./census/export/import_test.csv', 'w', encoding='UTF8')
            wr = csv.writer(self.file)
            header = ['username', 'first_name', 'last_name', 'email']
            wr.writerow(header)
            row = [user_admin.username,'','','']
            wr.writerow(row)
        finally:
            self.file.close()

        return self.file
        
    def test_import_census(self):
        #Gets the csv file with the user admin to import it into the census created in the set up method
        import_csv = self.generate_import_csv()
        file_path = import_csv.name

        f = open(file_path, "r")

        self.user = AnonymousUser()
        data = {'voting-select': self.v.id, 'csv-file': f}
        request = self.factory.post('/census/import/importing_census/', data, format='json')
        self.sm.process_request(request)
        self.mm.process_request(request)
        request.user = self.user
        response = importing_census(request)
        self.assertEqual(response.status_code, 401)

        f.close()
        f = open(file_path, "r")

        user_admin = User.objects.get(username="admin")
        self.user = user_admin
        data = {'voting-select': self.v.id, 'csv-file': f}
        request = self.factory.post('/census/import/importing_census/', data, format='json')
        self.sm.process_request(request)
        self.mm.process_request(request)
        request.user = self.user
        response = importing_census(request)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Census.objects.all().filter(voting_id=self.v.id,voter_id=user_admin.id).exists())
            
        f.close()
