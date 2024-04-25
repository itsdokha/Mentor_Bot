import datetime


class DB:
    def __init__(self):
        ...

    @staticmethod
    def get_db():
        with open('db.py') as f:
            return eval(f.read())

    @staticmethod
    def save_db(new_db):
        with open('db.py', 'w') as f:
            f.write(str(new_db))

    def get_user(self, user_id):
        db = self.get_db()
        for user in db['users']:
            if user['id'] == user_id:
                return user

        return None

    def add_user(self, user):
        self.delete_user(user['id'])
        db = self.get_db()
        db['users'].append(user)
        self.save_db(db)

    def delete_user(self, user_id):
        _temp = []
        db = self.get_db()
        for user in db['users']:
            if user['id'] == user_id:
                continue
            _temp.append(user)

        db['users'] = _temp
        self.save_db(db)

    def get_free_mentis(self):
        db = self.get_db()
        free_mentis = []
        _busy_mentis = []
        for mentor_id in db['jobs']:
            _busy_mentis += [db['jobs'][mentor_id]['menti_id']]

        print('_busy_mentis', _busy_mentis)

        for user in db['users']:
            if user['position'] == 'Menti' and user['id'] not in _busy_mentis:
                free_mentis.append(user)

        return free_mentis

    def get_wantings(self):
        db = self.get_db()
        return db['wanting_mentis']

    def add_job(self, mentor_id, menti_id):
        db = self.get_db()
        db['jobs'][mentor_id] = {'menti_id': menti_id, 'jobs': [], 'meetings': [], 'jobs_success': []}
        self.save_db(db)

    def add_wanting(self, mentor_id, menti_id):
        db = self.get_db()
        if db['wanting_mentis'].get(mentor_id):
            db['wanting_mentis'][mentor_id] += [menti_id]
        else:
            db['wanting_mentis'][mentor_id] = [menti_id]

        self.save_db(db)

    def remove_wanting(self, mentor_id, menti_id):
        db = self.get_db()
        db['wanting_mentis'][mentor_id].remove(menti_id)

        self.save_db(db)

    def add_order(self, order_text):
        db = self.get_db()
        db['orders'].append(order_text)

        self.save_db(db)

    def get_orders(self):
        db = self.get_db()
        return db['orders']

    def delete_order(self, order_id):
        db = self.get_db()
        del db['orders'][order_id - 1]

        self.save_db(db)

    def add_review(self, review):
        db = self.get_db()
        db['reviews'].append(review)

        self.save_db(db)

    def get_reviews(self):
        db = self.get_db()
        return db['reviews']

    def get_mentors_menti_id(self, mentor_id):
        db = self.get_db()
        return db['jobs'][mentor_id]['menti_id']

    def get_mentis_mentor_id(self, menti_id):
        db = self.get_db()
        for mentor_id in db['jobs']:
            if db['jobs'][mentor_id]['menti_id'] == menti_id:
                return mentor_id

    def get_users_by_role(self, role):
        db = self.get_db()
        _temp = []
        for user in db['users']:
            if user['position'] == role:
                _temp.append(user)

        return _temp

    def add_task(self, mentor_id, task_text, deadline):
        db = self.get_db()
        db['jobs'][mentor_id]['jobs'].append([task_text, deadline])

        self.save_db(db)

    def delete_task(self, mentor_id, task_id):
        db = self.get_db()
        del db['jobs'][mentor_id]['jobs'][task_id - 1]
        db['jobs'][mentor_id]['jobs_success'].append(True)

        self.save_db(db)

    def add_meeting(self, mentor_id, meeting_text):
        db = self.get_db()
        db['jobs'][mentor_id]['meetings'].append(meeting_text)

        self.save_db(db)

    def add_session(self, session):
        db = self.get_db()
        db['sessions'].append(session)

        self.save_db(db)

    def get_meetings(self, menti_id):
        db = self.get_db()
        for mentor_id in db['jobs']:
            if db['jobs'][mentor_id]['menti_id'] == menti_id:
                return db['jobs'][mentor_id]['meetings'] + db['sessions']

    def get_tasks(self, menti_id):
        db = self.get_db()
        for mentor_id in db['jobs']:
            if db['jobs'][mentor_id]['menti_id'] == menti_id:
                tasks = db['jobs'][mentor_id]['jobs']
                break

        else:
            return

        _temp = []
        for task in tasks:
            if datetime.datetime.now() < task[1]:
                _temp.append(task)

            else:
                db['jobs'][mentor_id]['jobs_success'].append(False)

        db['jobs'][mentor_id]['jobs'] = _temp
        self.save_db(db)

        return _temp

    def get_statics(self):
        db = self.get_db()
        statics = 'Число назначенных встреч:\n'
        for job in db['jobs']:
            statics += f"{self.get_user(job)['fio']} / {self.get_user(db['jobs'][job]['menti_id'])['fio']} = {len(db['jobs'][job]['meetings'])}\n"
        statics += '\nЧисло планируемых задач:\n'
        for job in db['jobs']:
            statics += f"{self.get_user(job)['fio']} / {self.get_user(db['jobs'][job]['menti_id'])['fio']} = {len(db['jobs'][job]['jobs'])}\n"
        statics += '\nПроцент выполненных задач:\n'
        for job in db['jobs']:
            statics += f"{self.get_user(job)['fio']} / {self.get_user(db['jobs'][job]['menti_id'])['fio']} = {db['jobs'][job]['jobs_success'].count(True) / len(db['jobs'][job]['jobs_success']) * 100}%\n"

        return statics
