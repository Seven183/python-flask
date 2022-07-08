
import flask, json, os
from gevent import pywsgi

api = flask.Flask(__name__)

@api.route('/clickhouseExport', methods=['post'])
def getAlarm():

    sql = flask.request.json.get('sql')

    try:
        os.popen('clickhouse-client --password 123456 --query "{} FORMAT CSVWithNames" > 3.csv'.format(sql))
        ren = {'message': "导出成功"}
        return json.dumps(ren, ensure_ascii=False)
    except BaseException as e:
        ren = {'message': e.args}
        return json.dumps(ren, ensure_ascii=False)

if __name__ == '__main__':
    server = pywsgi.WSGIServer(('0.0.0.0', 8888), api)
    server.serve_forever()
    # api.run(port=8888, debug=True, host='0.0.0.0')

