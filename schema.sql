drop table if exists urls;
create table urls (
  id integer primary key autoincrement,
  long text not null,
  short text
);
