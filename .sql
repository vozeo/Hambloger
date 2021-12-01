--20211119

CREATE TABLE users (
    userid      INTEGER PRIMARY KEY     NOT NULL,
    nickname    TEXT                    NOT NULL,
    passwd      TEXT                    NOT NULL
);

CREATE TABLE works (
    workid      INTEGER PRIMARY KEY     AUTOINCREMENT,
    workname    TEXT                    DEFAULT "No Name",
    authorid    INTEGER                 NOT NULL,
    rank        INTEGER                 DEFAULT 0,
    ext         TEXT                    
);

CREATE INDEX userid_index ON users (userid);
CREATE INDEX workid_index ON works (workid);

INSERT INTO users (userid, nickname, passwd) VALUES (0, "hehepig", "hehe");


--20211201

CREATE TABLE follows (
    whofollow   INTEGER                 NOT NULL,
    followwho   INTEGER                 NOT NULL
);