import uuid
import flask, json

from connect.mysql.get_Conn import getConn

api = flask.Flask(__name__)


@api.route('/addAlarm', methods=['post'])
def login():
    alarmCode = uuid.uuid1()
    alarmEmail = flask.request.json.get('alarmEmail')
    alarmUser = flask.request.json.get('alarmUser')
    userEmail = flask.request.json.get('userEmail')
    alarmType = flask.request.json.get('alarmType')
    tireType = flask.request.json.get('tireType')
    name = flask.request.json.get('name')
    operator = flask.request.json.get('operator')
    alarmRuleParams = flask.request.json.get('alarmRuleParams')
    monthDay = alarmRuleParams[0]["monthDay"]
    everyDay = alarmRuleParams[0]["everyDay"]
    if alarmRuleParams[0]["moreOrLess"] == 'Less Than':
        moreOrLess = 1
    else:
        moreOrLess = 2
    value = alarmRuleParams[0]["value"]

    try:
        conn = getConn()
        cursor = conn.cursor()
        insertAlarm = " insert into alarm (`code`, `name`, `alarm_type`, `tire_type`, `alarm_user`, `alarm_email`, `user_email`, `create_user`, `update_user`) " \
                      "VALUES('%s','%s','%s','%s','%s','%s','%s','%s','%s') " % (alarmCode, name, alarmType, tireType, alarmUser, alarmEmail, userEmail, operator, operator)
        insertAlarmRule = " insert into alarm_rule (`alarm_code`, `month_day`, `every_day`, `symbol`, `rule_value`, `rule_message`, `create_user`, `update_user`) " \
                          "VALUES('{}','{}','{}','{}','{}','{}','{}','{}') ".format(alarmCode, monthDay, everyDay, moreOrLess, value, "alarmEmail", operator, operator)

        cursor.execute(insertAlarm)
        execute = cursor.execute(insertAlarmRule)
        conn.commit()
        cursor.close()
        conn.close()
        ren = {'success': "1", 'code': execute, 'message': "插入成功", 'data': cursor.lastrowid, }
        return json.dumps(ren, ensure_ascii=False)
    except BaseException as e:
        ren = {'error': "0", 'message': e.args}
        return json.dumps(ren, ensure_ascii=False)


if __name__ == '__main__':
    api.run(port=8888, debug=True, host='0.0.0.0')
