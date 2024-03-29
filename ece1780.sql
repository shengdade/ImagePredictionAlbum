-- MySQL Script generated by MySQL Workbench
-- Sat Feb 18 17:57:59 2017
-- Model: New Model    Version: 1.0
-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS = @@UNIQUE_CHECKS, UNIQUE_CHECKS = 0;
SET @OLD_FOREIGN_KEY_CHECKS = @@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS = 0;
SET @OLD_SQL_MODE = @@SQL_MODE, SQL_MODE = 'TRADITIONAL,ALLOW_INVALID_DATES';

-- -----------------------------------------------------
-- Schema ece1780
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema ece1780
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `ece1780`
  DEFAULT CHARACTER SET utf8;
USE `ece1780`;

-- -----------------------------------------------------
-- Table `ece1780`.`users`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `ece1780`.`users`;

CREATE TABLE IF NOT EXISTS `ece1780`.`users` (
  `id`       INT         NOT NULL AUTO_INCREMENT,
  `login`    VARCHAR(16) NOT NULL,
  `password` VARCHAR(16) NOT NULL,
  PRIMARY KEY (`id`)
)
  ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table `ece1780`.`images`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `ece1780`.`images`;

CREATE TABLE IF NOT EXISTS `ece1780`.`images` (
  `id`       INT          NOT NULL AUTO_INCREMENT,
  `userId`   INT          NOT NULL,
  `imageKey` VARCHAR(255) NOT NULL,
  `predict`  VARCHAR(512) NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_images_users_idx` (`userId` ASC),
  CONSTRAINT `fk_images_users`
  FOREIGN KEY (`userId`)
  REFERENCES `ece1780`.`users` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE
)
  ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table `ece1780`.`setting`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `ece1780`.`setting`;

CREATE TABLE IF NOT EXISTS `ece1780`.`setting` (
  `autoScaling` INT NOT NULL,
  `cpuGrow`     INT NOT NULL,
  `cpuShrink`   INT NOT NULL,
  `ratioExpand` INT NOT NULL,
  `ratioShrink` INT NOT NULL
)
  ENGINE = InnoDB;

INSERT INTO setting (autoScaling, cpuGrow, cpuShrink, ratioExpand, ratioShrink) VALUES (0, 90, 10, 2, 2);


SET SQL_MODE = @OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS = @OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS = @OLD_UNIQUE_CHECKS;
