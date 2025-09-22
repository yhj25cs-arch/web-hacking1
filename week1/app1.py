from flask import Flask, request, render_template #플라스크 모듈의 여러 기능 불러오기
import sqlite3

app = Flask(__name__) #Flask 객체 생성

def init_db(): #DB 생성 함수
    conn = sqlite3.connect('guestbook.db') #데이터 베이스와 연결
    c = conn.cursor() #명령 준비
    c.execute('''CREATE TABLE IF NOT EXISTS guestbook
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, message TEXT)''') #명령 실행
    conn.commit() #변경 사항 저장
    conn.close() #연결 종료

@app.route('/') #URL 경로 연결
def home(): #홈페이지 함수
    conn = sqlite3.connect('guestbook.db')
    c = conn.cursor()
    entries = c.execute("SELECT name, message FROM guestbook").fetchall() #데이터베이스에서 데이터 모두 가져오기
    conn.close()
    return render_template('guestbook.html') #HTML 파일 렌더링

@app.route('/write' , methods=['POST']) #write 경로일 때 POST 방식으로 데이터 받기
def write(): #데이터 쓰기 함수
    name = request.form.get('name') #폼에서 데이터 가져오기
    message = request.form.get('message')
    
    conn = sqlite3.connect('guestbook.db')
    c = conn.cursor()
    c.execute("INSERT INTO guestbook (name, message) VALUES (?, ?)", (name, message)) #데이터베이스에 데이터 삽입
    entries = c.execute("SELECT name, message FROM guestbook").fetchall() #데이터베이스에 있는 데이터 리스트 형태로 모두 가져오기
    conn.commit()
    conn.close()

    return render_template('guestbook.html', entries=entries) #HTML 파일 렌더링, entries 변수 전달

@app.route('/search') #search 경로일 때 함수 실행
def search(): #검색 함수
    query = request.args.get('query', '') #쿼리 파라미터에서 검색어 가져오기, 기본값은 빈 문자열

    conn = sqlite3.connect('guestbook.db')
    c = conn.cursor()
    c.execute("SELECT name, message FROM guestbook WHERE message LIKE ?", ('%' + query + '%',))
    results = c.fetchall()
    conn.close()

    return render_template('guestbook.html', query=query, results=results)

if __name__ == '__main__': #직접 실행할 때만 실행(없으면 다른 파일에서 import할 때 실행됨)
    init_db() #DB 생성 함수 호출

    app.run(debug=True) #Flask 앱 실행, 디버그 모드 활성화