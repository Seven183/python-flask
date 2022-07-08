
import flask, json

from connect.mysql.get_Conn import getConn

api = flask.Flask(__name__)


@api.route('/getAlarm', methods=['get'])
def getAlarm():

    alarmCode = flask.request.values.get('alarmCode')
    try:
        conn = getConn()
        cursor = conn.cursor()
        selectAlarm = " select code, '' as alarmRuleList from alarm  where code ='{}' ".format(alarmCode)
        selectAlarmRule = " select month_day , every_day, symbol, rule_value, rule_message from alarm_rule  where alarm_code ='{}' ".format(alarmCode)

        cursor.execute(selectAlarm)
        selectAlarm = cursor.fetchone()

        cursor.execute(selectAlarmRule)
        selectAlarmRule = cursor.fetchall()
        selectAlarm["alarmRuleList"] = selectAlarmRule

        conn.commit()
        cursor.close()
        conn.close()
        ren = {'success': "1", 'code': selectAlarm, 'message': "查询成功", 'data': selectAlarmRule, }
        return json.dumps(ren, ensure_ascii=False)
    except BaseException as e:
        ren = {'error': "0", 'message': e.args}
        return json.dumps(ren, ensure_ascii=False)


if __name__ == '__main__':
    api.run(port=8888, debug=True, host='0.0.0.0')
