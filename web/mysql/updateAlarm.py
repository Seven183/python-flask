import uuid
import flask, json

from connect.mysql.get_Conn import getConn

api = flask.Flask(__name__)


@api.route('/updateAlarm', methods=['post'])
def update():
    alarmCode = flask.request.json.get('alarmCode')
    alarmEmail = flask.request.json.get('alarmEmail')

    try:
        conn = getConn()
        cursor = conn.cursor()
        updateAlarm = " update alarm set " \
                      "`alarm_email`='%s' " \
                      "where `code` = '%s' " % (alarmEmail, alarmCode)
        updateAlarmRule = " update alarm_rule set " \
                          " `rule_message`='{}'" \
                          " where `alarm_code` = '{}'".format("alarmEmail2", alarmCode)

        cursor.execute(updateAlarm)
        execute = cursor.execute(updateAlarmRule)

        conn.commit()
        cursor.close()
        conn.close()
        ren = {'success': "1", 'code': 1, 'message': "更新成功", 'data': execute, }
        return json.dumps(ren, ensure_ascii=False)
    except BaseException as e:
        ren = {'error': "0", 'message': e.args}
        return json.dumps(ren, ensure_ascii=False)


if __name__ == '__main__':
    api.run(port=8888, debug=True, host='0.0.0.0')
