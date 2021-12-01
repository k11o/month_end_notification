import calendar
import datetime
import json
import os
import urllib.request


class DateTypeManager():
    # ただの日
    NORMAL_DAY = 1
    # 最終日の前の日
    DAY_BEFORE_LAST_DAY = 2
    # 最終日
    LAST_DAY = 3

    def get_text(self):
        # 通知メッセージにするテキストを生成する
        if self.get_day_type() == self.LAST_DAY:
            return os.environ.get('LAST_DAY_TEXT', "今日は月末です")
        elif self.get_day_type() == self.DAY_BEFORE_LAST_DAY:
            return os.environ.get('DAY_BEFORE_LAST_DAY_TEXT', "そろそろ月末です")
        else:
            return ""

    def get_day_type(self):
        today = datetime.date.today()
        firstdate, lastdate = calendar.monthrange(today.year, today.month)
        if (today.weekday() == 4 and today.day >= lastdate - 2) or today.day == lastdate:
            # 金は土日が月末じゃないかどうかを判定する必要がある。
            # 上記 true の場合は月末
            return self.LAST_DAY
        elif (today.weekday() == 3 and today.day >= lastdate - 3) or today.day == lastdate - 1:
            # 木曜も土日が月末じゃないかどうかを判定する この場合は月末
            # 月末前の木曜もTRUE。また、月末二日前もTRUE
            return self.DAY_BEFORE_LAST_DAY


def lambda_handler(event, context):
    headers = {
        'Content-Type': 'application/json',
    }
    Manager = DateTypeManager()
    text = Manager.get_text()
    if text:
        data = json.dumps(
            {"message": text}).encode('utf-8')

        request = urllib.request.Request(os.environ['SLACK_WEBHOOK_URL'],
                                         data=data,
                                         method="POST",
                                         headers=headers)

        with urllib.request.urlopen(request) as response:
            response_body = response.read().decode("utf-8")

        return {
            'statusCode': 200,
            'body': response_body
        }
    else:
        return {
            'statusCode': 200,
            'body': "no applicant"
        }
