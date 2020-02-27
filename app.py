#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from flask import Flask ,redirect ,url_for,request,render_template
import random
import os, sys
import hashlib,base64
import requests
import glob
import config
import codecs, markdown
from wtforms import TextAreaField
from flask import make_response,escape,session,flash
app=Flask(__name__)
flag = True
app.secret_key ="config.config['secret_key']"
@app.route('/index.html')
def Get_Index():    
    if request.method == 'GET':                      
        some_page_name=glob.glob('%sflask/static/post/some_page*.html'%(config.config['path']))
        number=len(some_page_name)
        dic = dict.fromkeys(range(number), number)
        return render_template('index.html',dic=dic,number=number)
@app.route('/',methods=['GET'])            #@app.route('/index.html/<id>')  尝试把主页做成轮循模式
def Into_Index():
    if request.method == 'GET':
        some_page_name=glob.glob('%sflask/static/post/some_page*.html'%(config.config['path']))
        number=len(some_page_name)
        dic = dict.fromkeys(range(number), number)
        return render_template('index.html',dic=dic,number=number)
@app.route('/page/<id>',methods=['GET'])
def Get_Page(id):
    if request.method == 'GET':
        template="post/page%s.html"%(id)
        return render_template(template)
@app.route('/archives/<id>',methods=['GET'])
def Get_Archives_Page(id):
    if request.method == 'GET':
        template="archives/page_%s.html"%(id)
        return render_template(template)

@app.route('/about.html')
def Get_About():
    return render_template('about.html')

@app.route('/cates.html')
def Get_Cates():
    return render_template('cates.html')

@app.route('/search.html')
def Get_Search():
    jso=requests.get('http://api.tianapi.com/txapi/weibohot/index?key=53d0bbc6bd5023cac74d6dac4a9704f1').json()
    return render_template('search.html',jso = jso)

@app.route('/archives.html')
def Get_Archives():
    if request.method == 'GET':
        some_page_name=glob.glob('%sflask/static/archives/page*.html'%(config.config['path']))
        number=len(some_page_name)
        dic = dict.fromkeys(range(number), number)
        return render_template('archives.html',dic=dic,number=number)


def number_char_md5(string): #用MD5进行了加密
	##random_number=random.randint(1000000000,99999999999)
	md5=hashlib.md5(str(string).encode())
	random_number_md5=md5.hexdigest()
	return random_number_md5



@app.route('/write_up/?<session_name>/<session_passwd>')
def write_up(session_name,session_passwd):
    if session_name == session['username'] and session_passwd == session['userpasswd']:
        some_page_name=glob.glob('%sflask/static/post/some_page*.html'%(config.config['path']))
        some_page_number=len(some_page_name)
        page_name=glob.glob('%sflask/templates/post/page*.html'%(config.config['path']))
        page_number=len(page_name)
        archives_page_name=glob.glob('%sflask/static/archives/page_*.html'%(config.config['path']))
        archives_page_number=len(archives_page_name)
        return render_template('write_up.html',archives_page_number=archives_page_number,page_number=page_number,some_page_number=some_page_number)
    else :
        return redirect(url_for('Get_Index'))
@app.route('/get_body_page',methods=['GET'])
def get_body_page():
    if request.method == 'GET':
        filename = request.args.get('file_name')        
        name = request.args.get('user_name')
        time = request.args.get('time')
        md_name = request.args.get('md_name')
        page_href = request.args.get('page_url')
        title = request.args.get('file_title')
        some_body = request.args.get('file_body')
        result={'filename':filename,'name':name,'time':time,'page_href':page_href,'title':title,'some_body':some_body,'md_name':md_name}
        file_url='%sflask/templates/post/'%(config.config['path'])
        write_md(filename,file_url,result,md_name)
        return redirect(url_for('Get_Index'))



@app.route('/get_index_page',methods=['GET'])
def get_index_page():
    if request.method == 'GET':
        filename = request.args.get('file_name')        
        name = request.args.get('user_name')
        time = request.args.get('time')
        page_href = request.args.get('page_url')
        title = request.args.get('file_title')
        some_body = request.args.get('file_body')
        result={'filename':filename,'name':name,'time':time,'page_href':page_href,'title':title,'some_body':some_body}
        file_url='%sflask/static/post/'
        html=render_template('some_page_templates.html',result = result)
        write_html(filename,file_url,html)
        return render_template('some_page_templates.html',result = result)


@app.route('/get_archives_page',methods=['GET'])
def get_archives_page():
    if request.method == 'GET':
        filename = request.args.get('file_name')        
        name = request.args.get('user_name')
        time = request.args.get('time')
        year_time = request.args.get('year_time')
        title = request.args.get('file_title')
        page_href = request.args.get('page_url')
        some_body = request.args.get('file_body')
        result={'filename':filename,'time':time,'title':title,'some_body':some_body,'year_time':year_time,'page_href':page_href}
        file_url='%sflask/static/archives/'%(config.config['path'])
        page_url='%sflask/templates/archives/'%(config.config['path'])
        html=render_template('archives_page.html',result = result)
        write_archives_html(filename,page_url,html)
        write_html(filename,file_url,html)
        return render_template('archives_page.html',result = result)


@app.route('/rm_some_body_page',methods=['GET'])
def rm_some_body_page():
    path='%sflask/static/post/'%(config.config['path'])
    file_path=request.args.get('rm_file_name')
    file_path=path+file_path
    rm_file(file_path)
    return redirect(url_for('Get_Index'))

@app.route('/rm_body_page',methods=['GET'])
def rm_body_page():
    path='%sflask/templates/post/'
    file_path=request.args.get('rm_file_name')
    file_path=path+file_path
    rm_file(file_path)
    return redirect(url_for('Get_Index'))


@app.route('/rm_archives_page',methods=['GET'])
def rm_archives_page():
    file_path='%sflask/static/archives/'%(config.config['path'])+request.args.get('rm_file_name')
    rm_file(file_path)
    return redirect(url_for('Get_Index'))

def rm_file(file_path):
    os.remove(file_path)
    return True

@app.route('/login')  #登录口 用户输入name 并设置session
def login():
    return render_template('login.html')

@app.route('/logout')     #登出 删除session
def logout():
    session.pop('username',None)
    return redirect(url_for('Admin'))
@app.route('/check_login',methods=['POST'])
def check_login():
    name=request.form['username']
    passwd=request.form['userpasswd']
    if name==config.config['name'] and passwd == config.config['passwd']:#检测账号密码
            session['username']=number_char_md5(name)
            session['userpasswd']=number_char_md5(passwd)
            session_name=session['username']
            session_passwd=session['userpasswd']
            return redirect(url_for('write_up',session_name=session_name,session_passwd=session_passwd))
             
    else:
        return redirect(url_for('Get_Index'))

def write_html(filename,file_url,html):
    file_name=file_url+filename
    f=open(file_name,'a+')
    f.write(html)
    f.close()

def write_archives_html(filename,page_url,html):
    file_name=page_url+filename
    f=open(file_name,'a+')
    f.write(html)
    f.close()

def write_md(filename,file_url,result,md_name):
    md_name=file_url+md_name
    filename=file_url+filename
    md_check=glob.glob(md_name)
    print(md_check)
    if md_check == True:
        input_file = codecs.open(md_name, mode="r", encoding="utf-8")
        text = input_file.read()
        html = markdown.markdown(text)
        output_file = codecs.open(filename, mode="w", encoding="utf-8")
        output_file.write(html)
        return True
    else:
        f=open(md_name,'a+')
        f.write(result['title']+result['some_body']+result['time'])
        f.close()
        input_file = codecs.open(md_name, mode="r", encoding="utf-8")
        text = input_file.read()
        html = markdown.markdown(text)
        output_file = codecs.open(filename, mode="w", encoding="utf-8")
        output_file.write(html)
        return True

if __name__ == '__main__':
	app.run(host = config.config['host'] , port = config.config['port'] ,debug = config.config['debug'])
    
