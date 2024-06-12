import boto3
import pymysql
from botocore.exceptions import NoCredentialsError

def read_from_s3(bucket, key):
    s3 = boto3.client('s3')
    try:
        response = s3.get_object(Bucket=bucket, Key=key)
        data = response['Body'].read().decode('utf-8')
        return data
    except NoCredentialsError:
        print('Credentials not available')
        return None

def push_to_rds(data, host, user, password, db):
    try:
        connection = pymysql.connect(host=host, user=user, password=password, database=db)
        cursor = connection.cursor()
        cursor.execute("INSERT INTO your_table (data_column) VALUES (%s)", (data,))
        connection.commit()
        connection.close()
    except pymysql.MySQLError as e:
        print(f"Error: {e}")
        return False
    return True

def push_to_glue(data, database, table):
    glue = boto3.client('glue')
    response = glue.put_record(DatabaseName=database, TableName=table, Record=data)
    return response

def main():
    bucket = 'your-bucket-name'
    key = 'your-object-key'
    data = read_from_s3(bucket, key)
    if data:
        rds_success = push_to_rds(data, 'rds-host', 'rds-user', 'rds-password', 'rds-db')
        if not rds_success:
            push_to_glue(data, 'glue-database', 'glue-table')

if __name__ == "__main__":
    main()
