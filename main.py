import base64
import html
import json
import os
import subprocess
import sys
import re
import time
import traceback
from concurrent.futures import ThreadPoolExecutor
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import click
import yaml
import pickle
import smtplib
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import staleness_of
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from pypdf import PdfWriter
from compress import __compress



requests.adapters.DEFAULT_RETRIES = 5
reqsession = requests.session()
requests.packages.urllib3.disable_warnings()
reqsession.keep_alive = False
reqsession.verify = False

retry_strategy = Retry(
    total=3,
    status_forcelist=[500, 502, 503, 504, 404],
    allowed_methods=["HEAD", "GET", "OPTIONS", "POST"],
    backoff_factor=0.5,
)

http_adapter = HTTPAdapter(
    max_retries=retry_strategy,
    pool_connections=200,
    pool_maxsize=200,
)
reqsession.mount("http://", http_adapter)
reqsession.mount("https://", http_adapter)

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,"
    "image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
}

def __send_devtools(driver, cmd, params={}):
    resource = "/session/%s/chromium/send_command_and_get_result" % driver.session_id
    url = f"{driver.command_executor._client_config.remote_server_addr}{resource}"
    body = json.dumps({"cmd": cmd, "params": params})
    response = driver.command_executor._request("POST", url, body)

    if not response:
        raise Exception(response.get("value"))

    return response.get("value")

def worker(driver, uri, timeout):
    driver.get(uri)
    print(f'Working on {uri}')
    temp_height = 0
    while True:
        driver.execute_script("window.scrollBy(0,100)")
        driver.implicitly_wait(0.2)
        check_height = driver.execute_script(
            "return document.documentElement.scrollTop || window.pageYOffset || document.body.scrollTop;",
        )
        if check_height == temp_height:
            break
        temp_height = check_height

    try:
        WebDriverWait(driver, timeout).until(
            staleness_of(driver.find_element(by=By.TAG_NAME, value="html")),
        )
    except TimeoutException:
        calculated_print_options = {
            "landscape": False,
            "displayHeaderFooter": False,
            "printBackground": True,
            "preferCSSPageSize": True,
        }
        result = __send_devtools(
            driver,
            "Page.printToPDF",
            calculated_print_options,
        )
        return base64.b64decode(result["data"])

def head(uri):
    try:
        resp = requests.head(uri, timeout=3, headers={'User-Agent': 'Mozilla/5.0'})
        print(f'head status_code: {resp.status_code}, {uri}')
    except Exception as e:
        print(f'head error: {e}, {uri}')



@click.command("all_pdf")
@click.option(
    "-i",
    "--source",
    required=True,
    help="source is path",
)
@click.option(
    "-o",
    "--output",
    default="logs",
    help="output is dir",
)
@click.option(
    "-t",
    "--timeout",
    type=int,
    default=3,
    help="get url with browser timeout",
)
@click.option(
    "-c",
    "--compress",
    type=bool,
    default=False,
    help="PDF is compressed or not. Default value is False",
)
@click.option(
    "-p",
    "--power",
    type=int,
    default=0,
    help="power of the compression. Default value is 0. This can be 0: default, 1: prepress, 2: printer, 3: ebook, 4: screen",
)
@click.option(
    "-a",
    "--port",
    type=int,
    default=8000,
    help="mkdocs port. Default value is 8000",
)
def make_all_pdf(source, output, timeout, compress, power, port):
    webdriver_options = Options()
    webdriver_prefs = {}
    webdriver_prefs["profile.default_content_settings"] = {"images": 2}
    webdriver_options.add_argument("--headless")
    webdriver_options.add_argument("--disable-gpu")
    webdriver_options.add_argument("--no-sandbox")
    webdriver_options.add_argument("--disable-dev-shm-usage")
    webdriver_options.experimental_options["prefs"] = webdriver_prefs

    service = Service(ChromeDriverManager().install())
    host = f"http://127.0.0.1:{port}/"
    for dirname, _, file_lst in os.walk(source):
        for fname in file_lst:
            if not fname in ["mkdocs.yml"]:
                continue

            for i in range(9):
                os.popen("lsof -i:"+str(port)+" | grep -v 'PID' | awk '{print $2}' |  xargs kill -9")
                driver = webdriver.Chrome(service=service, options=webdriver_options)
                try:
                    parts_dir = os.path.join(dirname, "parts")
                    pattern = r'https?://[^\s]+'
                    fpath = os.path.join(dirname, "mkdocs.yml")
                    data = yaml.safe_load(open(fpath))
                    print(f'dirname: {dirname}')
                    navs = data.get('nav')
                    proc = subprocess.Popen(
                        ["mkdocs", "serve", "--no-livereload", "-a", f"127.0.0.1:{port}"],
                             cwd=dirname,  stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

                    part_dir = os.path.join(parts_dir, dirname)
                    if not os.path.exists(part_dir):
                        os.makedirs(part_dir, exist_ok=True)

                    pdfs = []
                    for nav in ["index.md"] + navs:
                        base_name = os.path.splitext(nav)[0]
                        target = os.path.join(part_dir, base_name.replace('%', "")  + ".pdf")
                        uri = host if base_name == "index" else host + html.escape(base_name)
                        mk_path = os.path.join(dirname, "docs", base_name+'.md')
                        mk_data = open(mk_path).read()
                        matches = re.findall(pattern, mk_data)
                        images = []
                        for match in matches:
                            if 'static001.geekbang.org' not in match:
                                continue
                            match = match if match.count(')') <= 0 else match[:match.index(')')]
                            images.append(match)

                        if os.path.exists(target):
                            pdfs.append((target, base_name, mk_data, images))
                            continue
                        with ThreadPoolExecutor(max_workers=3) as executor:
                            for img_url in images:
                                executor.submit(head, img_url)

                        result = worker(driver, uri, timeout)
                        if compress:
                            __compress(result, target, power)
                            print(f"__compress {target}")
                        else:
                            with open(target, "wb") as file:
                                file.write(result)
                                print(f"writing {target}")
                        pdfs.append((target, base_name, mk_data, images))


                    proc.kill()
                    os.popen("lsof -i:" + str(port) + " | grep -v 'PID' | awk '{print $2}' |  xargs kill -9")
                    merger = PdfWriter()
                    for (pdf, name, text, images) in pdfs:
                        merger.append(pdf)
                    pdf_base_name = os.path.basename(dirname).replace('%', "")
                    pdf_name = f"{pdf_base_name}.pdf"
                    pdf_path = os.path.join(dirname, pdf_name)
                    merger.write(pdf_path)
                    print(f"writing pdf {pdf_path}")
                    merger.close()
                    output_path = f'{output}/{os.path.basename(os.path.dirname(dirname))}/{pdf_name}'
                    if not os.path.exists(os.path.dirname(output_path)):
                        os.makedirs(os.path.dirname(output_path), exist_ok=True)
                    print(output_path)
                    os.rename(pdf_path, output_path)
                    break
                except Exception as e:
                    print(f"exception: {e}, traceback: {traceback.format_exc()}")
                    if 'No such file or directory' in str(e):
                        driver.quit()
                        os.popen("lsof -i:" + str(port) + " | grep -v 'PID' | awk '{print $2}' |  xargs kill -9")
                        break
                finally:
                    driver.quit()


@click.command("pdf")
@click.option(
    "-i",
    "--source",
    required=True,
    help="source is path",
)
@click.option(
    "-t",
    "--timeout",
    type=int,
    default=3,
    help="get url with browser timeout",
)
@click.option(
    "-c",
    "--compress",
    type=bool,
    default=False,
    help="PDF is compressed or not. Default value is False",
)
@click.option(
    "-p",
    "--power",
    type=int,
    default=0,
    help="power of the compression. Default value is 0. This can be 0: default, 1: prepress, 2: printer, 3: ebook, 4: screen",
)
@click.option(
    "-a",
    "--port",
    type=int,
    default=8000,
    help="mkdocs port. Default value is 8000",
)
def make_pdf(source, timeout, compress, power, port):
    webdriver_options = Options()
    webdriver_prefs = {}
    webdriver_prefs["profile.default_content_settings"] = {"images": 2}
    webdriver_options.add_argument("--headless")
    webdriver_options.add_argument("--disable-gpu")
    webdriver_options.add_argument("--no-sandbox")
    webdriver_options.add_argument("--disable-dev-shm-usage")
    webdriver_options.experimental_options["prefs"] = webdriver_prefs

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=webdriver_options)

    host = f"http://127.0.0.1:{port}/"
    parts_dir = os.path.join(source, "parts")
    pattern = r'https?://[^\s]+'
    fpath = os.path.join(source, "mkdocs.yml")
    data = yaml.safe_load(open(fpath))

    proc = subprocess.Popen(["mkdocs", "serve", "--no-livereload"],
                            cwd=source,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT,
                            )

    part_dir = os.path.join(parts_dir, source)
    if not os.path.exists(part_dir):
        os.makedirs(part_dir, exist_ok=True)

    pdfs = []
    navs = ["index.md"] + data.get('nav')
    for nav in navs:
        base_name = os.path.splitext(nav)[0]
        target = os.path.join(part_dir, base_name.replace('%', "") + ".pdf")
        uri = host if base_name == "index" else host + html.escape(base_name)
        mk_path = os.path.join(source, "docs", nav)
        mk_data = open(mk_path).read()
        matches = re.findall(pattern, mk_data)
        images = []
        for match in matches:
            if 'static001.geekbang.org' not in match:
                continue
            match = match if match.count(')') <= 0 else match[:match.index(')')]
            if os.path.exists(target):
                images.append(match)
            else:
                try:
                    resp = requests.head(match, timeout=3, headers={'User-Agent': 'Mozilla/5.0'})
                    print(f'head status_code: {resp.status_code}, {match}')
                    images.append(match)
                except Exception as e:
                    print(f'head error: {e}, {match}')

        if os.path.exists(target):
            pdfs.append((target, base_name, mk_data, images))
            continue

        result = worker(driver, uri, timeout)
        if compress:
            __compress(result, target, power)
            print(f"__compress {target}")
        else:
            with open(target, "wb") as file:
                file.write(result)
                print(f"writing {target}")
        pdfs.append((target, base_name, mk_data, images))


    proc.kill()

    merger = PdfWriter()
    for (pdf, name, text, images) in pdfs:
        merger.append(pdf)

    pdf_base_name = os.path.basename(source).replace('%','')
    pdf_path = os.path.join(source, pdf_base_name + ".pdf")
    merger.write(pdf_path)
    print(f"writing pdf {pdf_path}")
    merger.close()


@click.command("sayhi_email")
@click.option(
    "-i",
    "--repo",
    required=True,
    default="https://github.com/it-ebooks-0/geektime-books/stargazers",
    help="repo is github repositories",
)
@click.option(
    "-c",
    "--github_cookie",
    required=True,
    default=os.getenv("GITHUB_COOKIE"),
    help="repo is github repositories",
)
@click.option(
    "-o",
    "--pkl",
    required=True,
    default='email.pkl',
    help="email file",
)
def sayhi_email(repo, github_cookie, pkl):
    print(f"hello {repo}, github_cookie: {github_cookie}, pkl: {pkl}")
    page = 0
    timeout = 10
    headers = {
        'User-Agent': 'Mozilla/5.0',
        "Cookie": github_cookie,
    }
    proxies = {
        'http': 'socks5://127.0.0.1:1080',
        'https': 'socks5://127.0.0.1:1080',
    }
    data = {}
    while True:
        try:
            page += 1
            resp = requests.get(f'{repo}?page={page}', timeout=timeout, headers=headers, proxies=proxies)
            if resp.status_code != 200:
                print(f'say_hi status_code: {resp.status_code}, {repo}')
                break
            soup = BeautifulSoup(resp.text, 'html.parser')
            links = soup.find_all('a', class_='d-inline-block', attrs={'data-hovercard-type': 'user'})
            if not links:
                break
            for link in links:
                user_name = link['href'].split('/')[-1]
                user_url = 'https://github.com/'+user_name
                ret = requests.get(user_url, timeout=timeout, headers=headers, proxies=proxies)
                if ret.status_code != 200:
                    print(f'say_hi status_code: {ret.status_code}, {user_url}')
                    continue
                soup = BeautifulSoup(ret.text, 'html.parser')
                link = soup.find('li', attrs={'itemprop': 'email'})
                if link:
                    email = link.find('a', class_='Link--primary').text
                    if user_name not in data:
                        data[user_name] = email
                        print(user_name, email)
                else:
                   print(f'say_hi no email: {user_url}, page: {page}')
                time.sleep(0.2)
        except Exception as e:
            print(f'say_hi error: {e}, {repo}')

    with open(pkl, 'wb') as f:
        pickle.dump(data, f)

@click.command("sayhi")
@click.option(
    "-i",
    "--pkl",
    required=True,
    default='email.pkl',
    help="email file",
)
@click.option(
    "-n",
    "--project",
    required=True,
    default=os.getenv("PROJECT"),
    help="project",
)
@click.option(
    "-f",
    "--email_from",
    required=True,
    default=os.getenv("EMAIL_FROM"),
    help="email from",
)
@click.option(
    "-h",
    "--email_host",
    required=True,
    default=os.getenv("EMAIL_HOST"),
    help="email FROM",
)
@click.option(
    "-p",
    "--email_port",
    required=True,
    type=int,
    default=os.getenv("EMAIL_PORT"),
    help="email port",
)
@click.option(
    "-u",
    "--email_user",
    required=True,
    default=os.getenv("EMAIL_USER"),
    help="email user",
)
@click.option(
    "-d",
    "--email_password",
    required=True,
    default=os.getenv("EMAIL_PASSWORD"),
    help="email password",
)
@click.option(
    "-a",
    "--attch_path",
    required=True,
    help="email attch path",
)
def sayhi(
        pkl,
        project,
        email_from,
        email_host,
        email_port,
        email_user,
        email_password,
        attch_path,
):
    print(f"hello {pkl}")
    with open(pkl, 'rb') as f:
        data = pickle.load(f)
        for k, v in data.items():
            try:
                text = f'''
                         <html>
                             <body>

                             <h2> {project} </h2>

                             <p>你好！👋： <b>{k}</b></p>

                             <p>由于近期 geektime-books 项目许多用户反馈图片和电子书链接失效，影响阅读体验</p>

                             <p> 在此推荐极客时间markdown & pdf 文档的项目给你，欢迎关注，🌟star，请及时保存 </p>

                             <p> <a href='https://github.com/uaxe/geektime-docs'>geektime-docs</a>：支持markdown阅读方式</p>

                             <p> <a href='https://github.com/uaxe/geektime-pdfs'>geektime-pdfs</a>：支持pdf阅读方式</p>

                             <p> <a href='https://github.com/zkep/mygeektime'>mygeektime</a>：支持音视频下载在线播放</p>

                             <p>多种方式满足你的日常学习需求</p>

                             <p>同时欢迎在使用过程中，积极提交issue, 以便让项目更好的完善</p>
                             </body>
                         </html>
                         '''
                msg = MIMEMultipart()
                msg.attach(MIMEText(text, 'html', 'utf-8'))
                msg["From"] = email_from
                msg["To"] = v
                msg["Subject"] = f"{project}"

                if os.path.exists(attch_path):
                    base_name = os.path.basename(attch_path)
                    with open(attch_path, 'rb') as f:
                        mimebase = MIMEBase(os.path.splitext(base_name)[0], 'jpg')
                        mimebase.add_header('Content-Disposition', 'attachment', filename=base_name)
                        mimebase.set_payload(f.read())
                        encoders.encode_base64(mimebase)
                        msg.attach(mimebase)
                with smtplib.SMTP_SSL(email_host, email_port, timeout=3) as smtp:
                    smtp.login(email_user, email_password)
                    smtp.send_message(msg)
                time.sleep(5)
            except Exception as e:
                print(f'say_hi error: {e}, {traceback.format_exc()}')
        print(f'total: {len(data.items())}')

@click.group(invoke_without_command=True)
@click.pass_context
def heya(ctx):
    if ctx.invoked_subcommand is None:
        click.echo(ctx.get_help())

heya.add_command(make_pdf)
heya.add_command(make_all_pdf)
# heya.add_command(sayhi)
# heya.add_command(sayhi_email)

def main() -> int:
    return heya(auto_envvar_prefix="HEYA")

if __name__ == '__main__':
    sys.exit(main())