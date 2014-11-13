CREATE TABLE `idea` (
    `idea_id` CHAR(32) NOT NULL,
    `user_id` CHAR(32) NOT NULL,
    `title` VARCHAR(500) NOT NULL,
    `created_on` DATETIME NOT NULL,
    `status` VARCHAR(20) NULL DEFAULT NULL,
    `desc_html` TEXT NOT NULL,
    `desc_md` TEXT NOT NULL,
    PRIMARY KEY (`idea_id`),
    FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`) ON DELETE CASCADE
)

CREATE TABLE `user` (
    `user_id` CHAR(32) NOT NULL,
    `username` VARCHAR(80) NULL DEFAULT NULL,
    `email` VARCHAR(120) NULL DEFAULT NULL,
    `first_name` VARCHAR(120) NULL DEFAULT NULL,
    `last_name` VARCHAR(120) NULL DEFAULT NULL,
    `blog_url` VARCHAR(120) NULL DEFAULT NULL,
    `created_on` DATETIME NULL DEFAULT NULL,
    `last_login_on` DATETIME NULL DEFAULT NULL,
    `password` VARCHAR(180) NOT NULL,
    `facebook_url` VARCHAR(512) NULL DEFAULT '',
    `github_url` VARCHAR(512) NULL DEFAULT '',
    `twitter_url` VARCHAR(512) NULL DEFAULT '',
    `role` VARCHAR(32) NULL DEFAULT 'Noob',
    PRIMARY KEY (`user_id`),
)

CREATE TABLE `tag` (
    `tag_id` CHAR(32) NOT NULL,
    `tagname` VARCHAR(50) NOT NULL,
    `desc` TEXT NULL,
    `created_on` DATETIME NOT NULL,
    PRIMARY KEY (`tag_id`),
)

CREATE TABLE `comment` (
    `comment_id` CHAR(32) NOT NULL,
    `user_id` CHAR(32) NOT NULL,
    `idea_id` CHAR(32) NOT NULL,
    `desc_md` TEXT NOT NULL,
    `desc_html` TEXT NOT NULL,
    `created_on` DATETIME NOT NULL,
    PRIMARY KEY (`comment_id`),
    FOREIGN KEY (`idea_id`) REFERENCES `idea` (`idea_id`) ON DELETE CASCADE,
    FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`) ON DELETE CASCADE
)

CREATE TABLE `tagging` (
    `tag_id` CHAR(32) NOT NULL,
    `idea_id` CHAR(32) NOT NULL,
    PRIMARY KEY (`tag_id`, `idea_id`),
    FOREIGN KEY (`idea_id`) REFERENCES `idea` (`idea_id`) ON DELETE CASCADE,
    FOREIGN KEY (`tag_id`) REFERENCES `tag` (`tag_id`) ON DELETE CASCADE
)

CREATE TABLE `vote` (
    `user_id` CHAR(32) NOT NULL,
    `idea_id` CHAR(32) NOT NULL,
    PRIMARY KEY (`user_id`, `idea_id`),
    FOREIGN KEY (`idea_id`) REFERENCES `idea` (`idea_id`) ON DELETE CASCADE,
    FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`) ON DELETE CASCADE
)

CREATE TABLE `notif_comment_by_user` (
    `notif_id` CHAR(32) NOT NULL,
    `user_by` CHAR(32) NOT NULL,
    `user_to` CHAR(32) NOT NULL,
    `idea_id` CHAR(32) NOT NULL,
    `comment_id` CHAR(32) NOT NULL,
    `read` TINYINT(1) NOT NULL DEFAULT '0',
    `created_on` DATETIME NOT NULL,
    PRIMARY KEY (`notif_id`),
    FOREIGN KEY (`comment_id`) REFERENCES `comment` (`comment_id`) ON DELETE CASCADE,
    FOREIGN KEY (`idea_id`) REFERENCES `idea` (`idea_id`) ON DELETE CASCADE,
    FOREIGN KEY (`user_by`) REFERENCES `user` (`user_id`) ON DELETE CASCADE,
    FOREIGN KEY (`user_to`) REFERENCES `user` (`user_id`) ON DELETE CASCADE
)

CREATE TABLE `notif_comment_on_idea` (
    `notif_id` CHAR(32) NOT NULL,
    `user_by` CHAR(32) NOT NULL,
    `user_to` CHAR(32) NOT NULL,
    `idea_id` CHAR(32) NOT NULL,
    `comment_id` CHAR(32) NOT NULL,
    `read` TINYINT(1) NOT NULL DEFAULT '0',
    `created_on` DATETIME NOT NULL,
    PRIMARY KEY (`notif_id`),
    FOREIGN KEY (`comment_id`) REFERENCES `comment` (`comment_id`) ON DELETE CASCADE,
    FOREIGN KEY (`idea_id`) REFERENCES `idea` (`idea_id`) ON DELETE CASCADE,
    FOREIGN KEY (`user_by`) REFERENCES `user` (`user_id`) ON DELETE CASCADE,
    FOREIGN KEY (`user_to`) REFERENCES `user` (`user_id`) ON DELETE CASCADE
)

CREATE TABLE `notif_idea_by_user` (
    `notif_id` CHAR(32) NOT NULL,
    `user_by` CHAR(32) NOT NULL,
    `user_to` CHAR(32) NOT NULL,
    `idea_id` CHAR(32) NOT NULL,
    `read` TINYINT(1) NOT NULL DEFAULT '0',
    `created_on` DATETIME NOT NULL,
    PRIMARY KEY (`notif_id`),
    FOREIGN KEY (`idea_id`) REFERENCES `idea` (`idea_id`) ON DELETE CASCADE,
    FOREIGN KEY (`user_by`) REFERENCES `user` (`user_id`) ON DELETE CASCADE,
    FOREIGN KEY (`user_to`) REFERENCES `user` (`user_id`) ON DELETE CASCADE
)

CREATE TABLE `notif_idea_update` (
    `notif_id` CHAR(32) NOT NULL,
    `user_by` CHAR(32) NOT NULL,
    `user_to` CHAR(32) NOT NULL,
    `idea_id` CHAR(32) NOT NULL,
    `read` TINYINT(1) NOT NULL DEFAULT '0',
    `created_on` DATETIME NOT NULL,
    PRIMARY KEY (`notif_id`),
    FOREIGN KEY (`idea_id`) REFERENCES `idea` (`idea_id`) ON DELETE CASCADE,
    FOREIGN KEY (`user_by`) REFERENCES `user` (`user_id`) ON DELETE CASCADE,
    FOREIGN KEY (`user_to`) REFERENCES `user` (`user_id`) ON DELETE CASCADE
)

CREATE TABLE `tag_sub` (
    `sub_by` CHAR(32) NOT NULL,
    `sub_to` CHAR(32) NOT NULL,
    PRIMARY KEY (`sub_by`, `sub_to`),
    FOREIGN KEY (`sub_by`) REFERENCES `user` (`user_id`) ON DELETE CASCADE,
    FOREIGN KEY (`sub_to`) REFERENCES `tag` (`tag_id`) ON DELETE CASCADE
)


CREATE TABLE `user_sub` (
    `sub_by` CHAR(32) NOT NULL,
    `sub_to` CHAR(32) NOT NULL,
    PRIMARY KEY (`sub_by`, `sub_to`),
    FOREIGN KEY (`sub_by`) REFERENCES `user` (`user_id`) ON DELETE CASCADE,
    FOREIGN KEY (`sub_to`) REFERENCES `user` (`user_id`) ON DELETE CASCADE
)

CREATE TABLE `idea_sub` (
    `sub_by` CHAR(32) NOT NULL,
    `sub_to` CHAR(32) NOT NULL,
    PRIMARY KEY (`sub_by`, `sub_to`),
    FOREIGN KEY (`sub_by`) REFERENCES `user` (`user_id`) ON DELETE CASCADE,
    FOREIGN KEY (`sub_to`) REFERENCES `idea` (`idea_id`) ON DELETE CASCADE
)

