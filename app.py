from flask import Flask, render_template, redirect, url_for, request, make_response # flash 제거

app = Flask(__name__)
app.secret_key = 'Ch41Ns_G0t_TH3_k3Y_c4rd'

# 루트 경로: 쿠키 확인 및 설정
@app.route('/')
def index_redirect():
    response = make_response(redirect(url_for('index')))
    user_role = request.cookies.get('user_role')

    # user_role 쿠키가 'admin'이 아니면 'guest'로 설정
    if user_role != 'admin':
        response.set_cookie('user_role', 'guest', max_age=3600*24*7) # 1주일

    return response

# index.html 페이지 제공
@app.route('/index.html')
def index():
    return render_template('index.html')

# admin.html 페이지 제공 및 접근 제어
@app.route('/admin')
def admin():
    user_role = request.cookies.get('user_role')

    if user_role == 'admin':
        return render_template('admin.html')
    else:
        # admin이 아니면 'guest'로 강제 설정 (혹시 모를 상황 대비)
        # 이전에 설정된 쿠키가 'guest'가 아니라면 'guest'로 설정
        if user_role != 'guest':
            response = make_response(redirect(url_for('index'))) # index로 리다이렉트
            response.set_cookie('user_role', 'guest', max_age=3600*24*7) # 1주일
        else: # 이미 guest인 경우 (쿠키 재설정 불필요)
            response = make_response(redirect(url_for('index'))) # index로 리다이렉트
        return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=2001)