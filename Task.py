import re
import hashlib
import datetime
import dateparser
import humanize


class Task:
    def __init__(self):
        self.text = None
        self.meta = {
            'id': '',
            'created': datetime.datetime.now(),
            'updated': datetime.datetime.now()
        }

    def fillFromStoredLine(self, line):
        if '|' not in line:
            self.text = line.strip()
            self.meta['id'] = self._createId(self.text)
            return

        text, _, meta = line.rpartition('|')
        self.text = text.strip()

        for piece in meta.strip().split(','):
            label, data = piece.split(':', 1)
            data = data.strip()
            label = label.strip()
            if label == 'created' or label == 'updated' or label == 'dueDate':
                data = datetime.datetime.strptime(data, '%Y-%m-%d %H:%M:%S')
            self.meta[label] = data

    def _createId(self, text):
        return hashlib.sha1(text.encode('utf-8')).hexdigest()

    def fillFromHumanLine(self, line):
        dueDate, line = self._parseHumanDueDate(line)
        timer, line = self._parseHumanNotificationTimer(line)
        dueDate = datetime.datetime.now() if not dueDate and timer else dueDate

        self.text = re.sub(r"\s+", " ", line)
        self.meta['id'] = self._createId(self.text)
        self.meta['updated'] = datetime.datetime.now()

        if dueDate:
            hour = int(timer[0]) if timer else 0
            minute = int(timer[1]) if timer else 0
            self.meta['dueDate'] = dueDate.replace(hour=hour, minute=minute, second=0)

    def _parseHumanDueDate(self, text):
        dueDatePattern = r"=[\w-]+"
        matches = re.findall(dueDatePattern, text)
        if not matches:
            return [None, text]

        dueDate = dateparser.parse(matches[-1][1:], settings={'PREFER_DATES_FROM': 'future'})

        return [dueDate, text.replace(matches[-1], '').strip()]

    def _parseHumanNotificationTimer(self, text):
        timerPattern = r"\@[\d:]+"
        matches = re.findall(timerPattern, text)
        if not matches:
            return [None, text]

        timer = matches[-1][1:]
        if ':' not in timer:
            dueTime = datetime.datetime.now() + datetime.timedelta(minutes=int(timer))
            timer = f"{dueTime.hour}:{dueTime.minute}"

        return [timer.split(':'), text.replace(matches[-1], '').strip()]

    def prettyPrint(self):
        text = self.text
        if 'dueDate' not in self.meta:
            return text

        text += f" ={humanize.naturalday(self.meta['dueDate']).replace(' ', '-')}"

        if self.meta['dueDate'].hour != 0 or self.meta['dueDate'].minute != 0:
            text += f" @{0 if self.meta['dueDate'].hour < 10 else ''}{self.meta['dueDate'].hour}:{0 if self.meta['dueDate'].minute < 10 else ''}{self.meta['dueDate'].minute}"

        return text

    def __str__(self):
        meta = []
        for index, data in self.meta.items():
            if index == 'created' or index == 'updated' or index == 'dueDate':
                data = data.strftime('%Y-%m-%d %H:%M:%S')
            meta.append((index, data))
        meta_str = ', '.join('%s:%s' % m for m in meta)
        return '%s | %s\n' % (self.text, meta_str)

    def __getattr__(self, attr):
        if attr in self.meta:
            return self.meta[attr]
        elif attr == 'priority':
            match = re.search(r"\bAA+", self.text)
            return 0 if not match else len(match.group())
        elif attr not in ('id', 'dueDate', 'created', 'updated'):
            raise AttributeError('Unknow attribute: ' + attr)
        else:
            return ''

    def finish(self):
        self.meta['updated'] = datetime.datetime.now()

    def isOverdue(self):
        if 'dueDate' not in self.meta:
            return False

        return datetime.datetime.now() > self.meta['dueDate']
