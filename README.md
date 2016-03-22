# Anna Karenina

***

Simple [django-based](https://www.djangoproject.com/) app that allows Boolean searching (AND, OR, NOT) through Russian version of ['Anna Karenina'](https://en.wikipedia.org/wiki/Anna_Karenina) by Leo Tolstoy.

Query example:

`word1 AND word2 AND NOT ( word3 OR word4 )`

Precedence levels (high to low): parentheses, NOT, AND, OR. All query tokens must be separated by spaces (however parser allows you to omit them around parens).

Built on top of Django 1.9.4, MySQL 5.7 and Zurb Foundation 6.

### Setup

1. `$ git clone https://github.com/sergeynikiforov/anna-karenina.git`

2. `$ pip install -r requirements.txt` within your virtualenv

3. App assumes you have full unicode support in MySQL; typical settings in `/etc/my.cnf`:

    ```
    [client]
    default-character-set = utf8mb4

    [mysql]
    default-character-set = utf8mb4

    [mysqld]
    transaction-isolation = READ-COMMITTED
    innodb_file_per_table = TRUE
    character-set-client-handshake = FALSE
    character-set-server = utf8mb4
    collation-server = utf8mb4_unicode_ci
    ```

4. Create user and database in MySQL:

    ```
    mysql> CREATE DATABASE anna_db;
    mysql> CREATE USER 'anna_app'@'localhost' IDENTIFIED BY 'qwertY1!';
    mysql> GRANT ALL ON anna_db.* TO 'anna_app'@'localhost';
    ```

5. Get the database from the dump:

    `$ mysql -uanna_app -p anna_db < anna_db.sql`
