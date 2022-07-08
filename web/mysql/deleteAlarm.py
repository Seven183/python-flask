import uuid
import flask, json

from connect.mysql.get_Conn import getConn

api = flask.Flask(__name__)


@api.route('/deleteAlarm', methods=['get'])
def delete():
    alarmCode = flask.request.values.get('alarmCode')

    try:
        conn = getConn()
        cursor = conn.cursor()
        selectAlarm = " delete from alarm  where code ='{}' ".format(alarmCode)
        selectAlarmRule = " delete from alarm_rule  where alarm_code = '{}' ".format(alarmCode)

        cursor.execute(selectAlarmRule)
        execute = cursor.execute(selectAlarm)

        conn.commit()
        cursor.close()
        conn.close()
        ren = {'success': "1", 'code': 1, 'message': "删除成功", 'data': execute, }
        return json.dumps(ren, ensure_ascii=False)
    except BaseException as e:
        ren = {'error': "0", 'message': e.args}
        return json.dumps(ren, ensure_ascii=False)


if __name__ == '__main__':
    api.run(port=8888, debug=True, host='0.0.0.0')
