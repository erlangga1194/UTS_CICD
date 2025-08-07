from flask import Flask, render_template
import pymysql
import boto3
import os

# 👇 Sesuaikan lokasi template dan static
app = Flask(
    __name__,
    template_folder='frontend/templates',
    static_folder='frontend/static'
)

# Backend config
import backend.config as cfg

# RDS connection
conn = pymysql.connect(
    host=cfg.RDS_HOST,
    user=cfg.DB_USER,
    password=cfg.DB_PASS,
    db=cfg.DB_NAME
)
cur = conn.cursor()

# S3 config
s3 = boto3.client('s3')
bucket = cfg.S3_BUCKET

@app.route('/')
def index():
    cur.execute("SELECT name, price FROM products")
    products = cur.fetchall()

    images = s3.list_objects_v2(Bucket=bucket).get('Contents', [])
    image_urls = [f"https://{bucket}.s3.amazonaws.com/{img['Key']}" for img in images]

    return render_template('index.html', products=products, images=image_urls)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
