-- MySQL dump 10.13  Distrib 5.6.19, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: ideabin
-- ------------------------------------------------------
-- Server version	5.6.19-0ubuntu0.14.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `alembic_version`
--

DROP TABLE IF EXISTS `alembic_version`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `alembic_version` (
  `version_num` varchar(32) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `alembic_version`
--

LOCK TABLES `alembic_version` WRITE;
/*!40000 ALTER TABLE `alembic_version` DISABLE KEYS */;
INSERT INTO `alembic_version` VALUES ('16088d721b4');
/*!40000 ALTER TABLE `alembic_version` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `comment`
--

DROP TABLE IF EXISTS `comment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `comment` (
  `comment_id` char(32) NOT NULL,
  `user_id` char(32) NOT NULL,
  `idea_id` char(32) NOT NULL,
  `desc_md` text NOT NULL,
  `desc_html` text NOT NULL,
  `created_on` datetime NOT NULL,
  PRIMARY KEY (`comment_id`),
  KEY `idea_id` (`idea_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `comment_ibfk_1` FOREIGN KEY (`idea_id`) REFERENCES `idea` (`idea_id`) ON DELETE CASCADE,
  CONSTRAINT `comment_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `comment`
--

LOCK TABLES `comment` WRITE;
/*!40000 ALTER TABLE `comment` DISABLE KEYS */;
/*!40000 ALTER TABLE `comment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `idea`
--

DROP TABLE IF EXISTS `idea`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `idea` (
  `idea_id` char(32) NOT NULL,
  `user_id` char(32) NOT NULL,
  `title` varchar(500) NOT NULL,
  `created_on` datetime NOT NULL,
  `status` varchar(20) DEFAULT NULL,
  `desc_html` text NOT NULL,
  `desc_md` text NOT NULL,
  PRIMARY KEY (`idea_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `idea_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `idea`
--

LOCK TABLES `idea` WRITE;
/*!40000 ALTER TABLE `idea` DISABLE KEYS */;
/*!40000 ALTER TABLE `idea` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `idea_sub`
--

DROP TABLE IF EXISTS `idea_sub`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `idea_sub` (
  `sub_by` char(32) NOT NULL,
  `sub_to` char(32) NOT NULL,
  PRIMARY KEY (`sub_by`,`sub_to`),
  KEY `sub_to` (`sub_to`),
  CONSTRAINT `idea_sub_ibfk_1` FOREIGN KEY (`sub_by`) REFERENCES `user` (`user_id`) ON DELETE CASCADE,
  CONSTRAINT `idea_sub_ibfk_2` FOREIGN KEY (`sub_to`) REFERENCES `idea` (`idea_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `idea_sub`
--

LOCK TABLES `idea_sub` WRITE;
/*!40000 ALTER TABLE `idea_sub` DISABLE KEYS */;
/*!40000 ALTER TABLE `idea_sub` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `notif_comment_by_user`
--

DROP TABLE IF EXISTS `notif_comment_by_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `notif_comment_by_user` (
  `notif_id` char(32) NOT NULL,
  `user_by` char(32) NOT NULL,
  `user_to` char(32) NOT NULL,
  `idea_id` char(32) NOT NULL,
  `comment_id` char(32) NOT NULL,
  `read` tinyint(1) NOT NULL DEFAULT '0',
  `created_on` datetime NOT NULL,
  PRIMARY KEY (`notif_id`),
  KEY `comment_id` (`comment_id`),
  KEY `idea_id` (`idea_id`),
  KEY `user_by` (`user_by`),
  KEY `user_to` (`user_to`),
  CONSTRAINT `notif_comment_by_user_ibfk_1` FOREIGN KEY (`comment_id`) REFERENCES `comment` (`comment_id`) ON DELETE CASCADE,
  CONSTRAINT `notif_comment_by_user_ibfk_2` FOREIGN KEY (`idea_id`) REFERENCES `idea` (`idea_id`) ON DELETE CASCADE,
  CONSTRAINT `notif_comment_by_user_ibfk_3` FOREIGN KEY (`user_by`) REFERENCES `user` (`user_id`) ON DELETE CASCADE,
  CONSTRAINT `notif_comment_by_user_ibfk_4` FOREIGN KEY (`user_to`) REFERENCES `user` (`user_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `notif_comment_by_user`
--

LOCK TABLES `notif_comment_by_user` WRITE;
/*!40000 ALTER TABLE `notif_comment_by_user` DISABLE KEYS */;
/*!40000 ALTER TABLE `notif_comment_by_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `notif_comment_on_idea`
--

DROP TABLE IF EXISTS `notif_comment_on_idea`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `notif_comment_on_idea` (
  `notif_id` char(32) NOT NULL,
  `user_by` char(32) NOT NULL,
  `user_to` char(32) NOT NULL,
  `idea_id` char(32) NOT NULL,
  `comment_id` char(32) NOT NULL,
  `read` tinyint(1) NOT NULL DEFAULT '0',
  `created_on` datetime NOT NULL,
  PRIMARY KEY (`notif_id`),
  KEY `comment_id` (`comment_id`),
  KEY `idea_id` (`idea_id`),
  KEY `user_by` (`user_by`),
  KEY `user_to` (`user_to`),
  CONSTRAINT `notif_comment_on_idea_ibfk_1` FOREIGN KEY (`comment_id`) REFERENCES `comment` (`comment_id`) ON DELETE CASCADE,
  CONSTRAINT `notif_comment_on_idea_ibfk_2` FOREIGN KEY (`idea_id`) REFERENCES `idea` (`idea_id`) ON DELETE CASCADE,
  CONSTRAINT `notif_comment_on_idea_ibfk_3` FOREIGN KEY (`user_by`) REFERENCES `user` (`user_id`) ON DELETE CASCADE,
  CONSTRAINT `notif_comment_on_idea_ibfk_4` FOREIGN KEY (`user_to`) REFERENCES `user` (`user_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `notif_comment_on_idea`
--

LOCK TABLES `notif_comment_on_idea` WRITE;
/*!40000 ALTER TABLE `notif_comment_on_idea` DISABLE KEYS */;
/*!40000 ALTER TABLE `notif_comment_on_idea` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `notif_idea_by_user`
--

DROP TABLE IF EXISTS `notif_idea_by_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `notif_idea_by_user` (
  `notif_id` char(32) NOT NULL,
  `user_by` char(32) NOT NULL,
  `user_to` char(32) NOT NULL,
  `idea_id` char(32) NOT NULL,
  `read` tinyint(1) NOT NULL DEFAULT '0',
  `created_on` datetime NOT NULL,
  PRIMARY KEY (`notif_id`),
  KEY `idea_id` (`idea_id`),
  KEY `user_by` (`user_by`),
  KEY `user_to` (`user_to`),
  CONSTRAINT `notif_idea_by_user_ibfk_1` FOREIGN KEY (`idea_id`) REFERENCES `idea` (`idea_id`) ON DELETE CASCADE,
  CONSTRAINT `notif_idea_by_user_ibfk_2` FOREIGN KEY (`user_by`) REFERENCES `user` (`user_id`) ON DELETE CASCADE,
  CONSTRAINT `notif_idea_by_user_ibfk_3` FOREIGN KEY (`user_to`) REFERENCES `user` (`user_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `notif_idea_by_user`
--

LOCK TABLES `notif_idea_by_user` WRITE;
/*!40000 ALTER TABLE `notif_idea_by_user` DISABLE KEYS */;
/*!40000 ALTER TABLE `notif_idea_by_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `notif_idea_update`
--

DROP TABLE IF EXISTS `notif_idea_update`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `notif_idea_update` (
  `notif_id` char(32) NOT NULL,
  `user_by` char(32) NOT NULL,
  `user_to` char(32) NOT NULL,
  `idea_id` char(32) NOT NULL,
  `read` tinyint(1) NOT NULL DEFAULT '0',
  `created_on` datetime NOT NULL,
  PRIMARY KEY (`notif_id`),
  KEY `idea_id` (`idea_id`),
  KEY `user_by` (`user_by`),
  KEY `user_to` (`user_to`),
  CONSTRAINT `notif_idea_update_ibfk_1` FOREIGN KEY (`idea_id`) REFERENCES `idea` (`idea_id`) ON DELETE CASCADE,
  CONSTRAINT `notif_idea_update_ibfk_2` FOREIGN KEY (`user_by`) REFERENCES `user` (`user_id`) ON DELETE CASCADE,
  CONSTRAINT `notif_idea_update_ibfk_3` FOREIGN KEY (`user_to`) REFERENCES `user` (`user_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `notif_idea_update`
--

LOCK TABLES `notif_idea_update` WRITE;
/*!40000 ALTER TABLE `notif_idea_update` DISABLE KEYS */;
/*!40000 ALTER TABLE `notif_idea_update` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tag`
--

DROP TABLE IF EXISTS `tag`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tag` (
  `tag_id` char(32) NOT NULL,
  `tagname` varchar(50) NOT NULL,
  `desc` text,
  `created_on` datetime NOT NULL,
  PRIMARY KEY (`tag_id`),
  UNIQUE KEY `tagname` (`tagname`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tag`
--

LOCK TABLES `tag` WRITE;
/*!40000 ALTER TABLE `tag` DISABLE KEYS */;
/*!40000 ALTER TABLE `tag` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tag_sub`
--

DROP TABLE IF EXISTS `tag_sub`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tag_sub` (
  `sub_by` char(32) NOT NULL,
  `sub_to` char(32) NOT NULL,
  PRIMARY KEY (`sub_by`,`sub_to`),
  KEY `sub_to` (`sub_to`),
  CONSTRAINT `tag_sub_ibfk_1` FOREIGN KEY (`sub_by`) REFERENCES `user` (`user_id`) ON DELETE CASCADE,
  CONSTRAINT `tag_sub_ibfk_2` FOREIGN KEY (`sub_to`) REFERENCES `tag` (`tag_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tag_sub`
--

LOCK TABLES `tag_sub` WRITE;
/*!40000 ALTER TABLE `tag_sub` DISABLE KEYS */;
/*!40000 ALTER TABLE `tag_sub` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tagging`
--

DROP TABLE IF EXISTS `tagging`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tagging` (
  `tag_id` char(32) NOT NULL,
  `idea_id` char(32) NOT NULL,
  PRIMARY KEY (`tag_id`,`idea_id`),
  KEY `idea_id` (`idea_id`),
  CONSTRAINT `tagging_ibfk_1` FOREIGN KEY (`idea_id`) REFERENCES `idea` (`idea_id`) ON DELETE CASCADE,
  CONSTRAINT `tagging_ibfk_2` FOREIGN KEY (`tag_id`) REFERENCES `tag` (`tag_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tagging`
--

LOCK TABLES `tagging` WRITE;
/*!40000 ALTER TABLE `tagging` DISABLE KEYS */;
/*!40000 ALTER TABLE `tagging` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user` (
  `user_id` char(32) NOT NULL,
  `username` varchar(80) DEFAULT NULL,
  `email` varchar(120) DEFAULT NULL,
  `first_name` varchar(120) DEFAULT NULL,
  `last_name` varchar(120) DEFAULT NULL,
  `blog_url` varchar(120) DEFAULT NULL,
  `created_on` datetime DEFAULT NULL,
  `last_login_on` datetime DEFAULT NULL,
  `password` varchar(180) NOT NULL,
  `facebook_url` varchar(512) DEFAULT '',
  `github_url` varchar(512) DEFAULT '',
  `twitter_url` varchar(512) DEFAULT '',
  `role` varchar(32) DEFAULT 'Noob',
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `email` (`email`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_sub`
--

DROP TABLE IF EXISTS `user_sub`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user_sub` (
  `sub_by` char(32) NOT NULL,
  `sub_to` char(32) NOT NULL,
  PRIMARY KEY (`sub_by`,`sub_to`),
  KEY `sub_to` (`sub_to`),
  CONSTRAINT `user_sub_ibfk_1` FOREIGN KEY (`sub_by`) REFERENCES `user` (`user_id`) ON DELETE CASCADE,
  CONSTRAINT `user_sub_ibfk_2` FOREIGN KEY (`sub_to`) REFERENCES `user` (`user_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_sub`
--

LOCK TABLES `user_sub` WRITE;
/*!40000 ALTER TABLE `user_sub` DISABLE KEYS */;
/*!40000 ALTER TABLE `user_sub` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `vote`
--

DROP TABLE IF EXISTS `vote`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `vote` (
  `user_id` char(32) NOT NULL,
  `idea_id` char(32) NOT NULL,
  PRIMARY KEY (`user_id`,`idea_id`),
  KEY `idea_id` (`idea_id`),
  CONSTRAINT `vote_ibfk_1` FOREIGN KEY (`idea_id`) REFERENCES `idea` (`idea_id`) ON DELETE CASCADE,
  CONSTRAINT `vote_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `vote`
--

LOCK TABLES `vote` WRITE;
/*!40000 ALTER TABLE `vote` DISABLE KEYS */;
/*!40000 ALTER TABLE `vote` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2015-03-15 12:44:55
