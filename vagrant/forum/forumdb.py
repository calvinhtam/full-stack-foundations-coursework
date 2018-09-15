# "Database code" for the DB Forum.

import psycopg2


def get_posts():
  """Return all posts from the 'database', most recent first."""
  db = psycopg2.connect('dbname=forum')
  c = db.cursor()
  c.execute("select content, time from posts order by time desc;")
  c.execute("update posts set content where content like '%spam%';")
  c.execute("delete from posts where content = 'cheese'")
  db.close()
  return c.fetchall()

def add_post(content):
  """Add a post to the 'database' with the current timestamp."""
  db = psycopg2.connect('dbname=forum')
  c = db.cursor()
  c.execute("insert into post values (%s);", (bleach.clean(content),))
  db.commit()
  db.close()
