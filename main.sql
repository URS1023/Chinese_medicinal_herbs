/*
 Navicat Premium Data Transfer

 Source Server         : 3
 Source Server Type    : SQLite
 Source Server Version : 3035005
 Source Schema         : main

 Target Server Type    : SQLite
 Target Server Version : 3035005
 File Encoding         : 65001

 Date: 07/06/2025 19:18:12
*/

PRAGMA foreign_keys = false;

-- ----------------------------
-- Table structure for alembic_version
-- ----------------------------
DROP TABLE IF EXISTS "alembic_version";
CREATE TABLE "alembic_version" (
  "version_num" VARCHAR(32) NOT NULL,
  CONSTRAINT "alembic_version_pkc" PRIMARY KEY ("version_num")
);

-- ----------------------------
-- Table structure for detection_history
-- ----------------------------
DROP TABLE IF EXISTS "detection_history";
CREATE TABLE "detection_history" (
  "id" INTEGER NOT NULL,
  "user_id" INTEGER NOT NULL,
  "herb_id" INTEGER NOT NULL,
  "image_path" VARCHAR(200),
  "detection_time" DATETIME,
  "confidence" FLOAT,
  "is_correct" BOOLEAN,
  PRIMARY KEY ("id"),
  FOREIGN KEY ("user_id") REFERENCES "user" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION,
  FOREIGN KEY ("herb_id") REFERENCES "herb" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION
);

-- ----------------------------
-- Table structure for herb
-- ----------------------------
DROP TABLE IF EXISTS "herb";
CREATE TABLE "herb" (
  "id" INTEGER NOT NULL,
  "name" VARCHAR(100) NOT NULL,
  "image_path" VARCHAR(200),
  "description" TEXT,
  "similar_herbs" TEXT,
  "effects" TEXT,
  "properties" TEXT,
  "created_at" DATETIME,
  "english_name" VARCHAR(100),
  "photo_number" INTEGER,
  "page_number" VARCHAR(50),
  "usage_parts" TEXT,
  "season" VARCHAR(20),
  PRIMARY KEY ("id"),
  UNIQUE ("name" ASC)
);

-- ----------------------------
-- Table structure for sensor
-- ----------------------------
DROP TABLE IF EXISTS "sensor";
CREATE TABLE "sensor" (
  "temp" TEXT(255),
  "humi" TEXT(255),
  "sound" TEXT(255),
  "tilt" TEXT(255),
  "vibrate" TEXT(255),
  "fire" TEXT(255),
  "smoke" TEXT(255),
  "light_sense" TEXT(255),
  "event_time" TEXT(255)
);

-- ----------------------------
-- Table structure for user
-- ----------------------------
DROP TABLE IF EXISTS "user";
CREATE TABLE "user" (
  "id" INTEGER NOT NULL,
  "username" VARCHAR(80) NOT NULL,
  "password_hash" VARCHAR(128),
  "is_admin" BOOLEAN,
  "created_at" DATETIME,
  PRIMARY KEY ("id"),
  UNIQUE ("username" ASC)
);

PRAGMA foreign_keys = true;
