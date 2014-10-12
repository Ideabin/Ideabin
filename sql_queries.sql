# SQL Queries (env/bin/alembic upgrade head --sql)

CREATE TABLE user (
    user_id CHAR(32) NOT NULL,
    username VARCHAR(80),
    password VARCHAR(180) NOT NULL
    email VARCHAR(120),
    first_name VARCHAR(120),
    last_name VARCHAR(120),
    blog_url VARCHAR(120),
    profile_fb VARCHAR(120),
    profile_twitter VARCHAR(120),
    created_on DATETIME,
    last_login_on DATETIME,
    PRIMARY KEY (user_id),
    UNIQUE (email),
    UNIQUE (username),
);

CREATE TABLE idea (
    idea_id CHAR(32) NOT NULL,
    user_id CHAR(32) NOT NULL,
    title VARCHAR(500) NOT NULL,
    `desc` TEXT NOT NULL,
    status VARCHAR(20),
    story TEXT NULL,
    vote_count INTEGER,
    created_on DATETIME NOT NULL,
    PRIMARY KEY (idea_id),
    FOREIGN KEY(user_id) REFERENCES user (user_id) ON DELETE CASCADE
);


CREATE TABLE tag (
    tag_id CHAR(32) NOT NULL,
    idea_id CHAR(32) NOT NULL,
    tagname VARCHAR(500) NOT NULL,
    created_on DATETIME NOT NULL,
    PRIMARY KEY (tag_id),
    FOREIGN KEY(idea_id) REFERENCES idea (idea_id) ON DELETE CASCADE
);

CREATE TABLE alembic_version (
    version_num VARCHAR(32) NOT NULL
);

