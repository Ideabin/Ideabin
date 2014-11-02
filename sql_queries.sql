# SQL Queries (env/bin/alembic upgrade head --sql)

CREATE TABLE alembic_version (
    version_num VARCHAR(32) NOT NULL
);

CREATE TABLE user (
    user_id CHAR(32) NOT NULL,
    username VARCHAR(80),
    email VARCHAR(120),
    first_name VARCHAR(120),
    last_name VARCHAR(120),
    blog_url VARCHAR(120),
    created_on DATETIME,
    last_login_on DATETIME,
    password VARCHAR(180) NOT NULL,
    facebook_url VARCHAR(512) NULL DEFAULT '',
    twitter_url VARCHAR(512) NULL DEFAULT ''
    github_url VARCHAR(512) NULL DEFAULT ''
    role VARCHAR(32) NULL DEFAULT 'Noob',
    PRIMARY KEY (user_id),
    UNIQUE (email),
    UNIQUE (username)
);

CREATE TABLE idea (
    idea_id CHAR(32) NOT NULL,
    user_id CHAR(32) NOT NULL,
    title VARCHAR(500) NOT NULL,
    vote_count INTEGER,
    created_on DATETIME NOT NULL,
    status VARCHAR(20),
    desc_html TEXT NOT NULL,
    desc_md TEXT NOT NULL
    PRIMARY KEY (idea_id),
    FOREIGN KEY(user_id) REFERENCES user (user_id) ON DELETE CASCADE
);

CREATE TABLE tag (
    tag_id CHAR(32) NOT NULL,
    tagname VARCHAR(50) COLLATE utf32_unicode_ci NOT NULL,
    `desc` TEXT,
    created_on DATETIME NOT NULL,
    PRIMARY KEY (tag_id),
    UNIQUE (tagname)
);

CREATE TABLE tagging (
    tag_id CHAR(32) NOT NULL,
    idea_id CHAR(32) NOT NULL,
    PRIMARY KEY (tag_id, idea_id),
    FOREIGN KEY(idea_id) REFERENCES idea (idea_id) ON DELETE CASCADE,
    FOREIGN KEY(tag_id) REFERENCES tag (tag_id) ON DELETE CASCADE
);

CREATE TABLE comment (
    comment_id CHAR(32) NOT NULL,
    user_id CHAR(32) NOT NULL,
    idea_id CHAR(32) NOT NULL,
    desc_md TEXT NOT NULL,
    desc_html TEXT NOT NULL,
    created_on DATETIME NOT NULL,
    PRIMARY KEY (comment_id),
    FOREIGN KEY(idea_id) REFERENCES idea (idea_id) ON DELETE CASCADE,
    FOREIGN KEY(user_id) REFERENCES user (user_id) ON DELETE CASCADE
);

CREATE TABLE vote (
    user_id CHAR(32) NOT NULL,
    idea_id CHAR(32) NOT NULL,
    PRIMARY KEY (user_id, idea_id),
    FOREIGN KEY(idea_id) REFERENCES idea (idea_id) ON DELETE CASCADE,
    FOREIGN KEY(user_id) REFERENCES user (user_id) ON DELETE CASCADE
);




