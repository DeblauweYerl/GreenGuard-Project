-- MySQL dump 10.17  Distrib 10.3.17-MariaDB, for debian-linux-gnueabihf (armv7l)
--
-- Host: localhost    Database: sensorsdb
-- ------------------------------------------------------
-- Server version	10.3.17-MariaDB-0+deb10u1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `tblaction`
--

DROP TABLE IF EXISTS `tblaction`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tblaction` (
  `ActionId` varchar(10) NOT NULL,
  `Description` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`ActionId`),
  UNIQUE KEY `ActionId_UNIQUE` (`ActionId`),
  KEY `Description_idx` (`Description`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tblaction`
--

LOCK TABLES `tblaction` WRITE;
/*!40000 ALTER TABLE `tblaction` DISABLE KEYS */;
INSERT INTO `tblaction` VALUES ('SOLA','Automatic activation solenoid valve'),('SOLM','Manual activation solenoid valve'),('HUM','Read humidity'),('LIGHT','Read light level'),('MOIST','Read soil moisture'),('TEMP','Read temperature');
/*!40000 ALTER TABLE `tblaction` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tbldevice`
--

DROP TABLE IF EXISTS `tbldevice`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tbldevice` (
  `DeviceId` int(11) NOT NULL AUTO_INCREMENT,
  `DeviceName` varchar(60) NOT NULL,
  `Type` varchar(45) DEFAULT NULL,
  `Description` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`DeviceId`),
  UNIQUE KEY `DeviceName_UNIQUE` (`DeviceName`),
  UNIQUE KEY `DeviceId_UNIQUE` (`DeviceId`),
  KEY `Type_DeviceId_idx` (`Type`,`DeviceId`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tbldevice`
--

LOCK TABLES `tbldevice` WRITE;
/*!40000 ALTER TABLE `tbldevice` DISABLE KEYS */;
INSERT INTO `tbldevice` VALUES (1,'LDR','Sensor','Measures the light'),(2,'Soil moisture sensor','Sensor','Measures the moisture in the soil'),(3,'Humidity and temperature sensor','Sensor','Measures the humidity and temperature'),(4,'Solenoid valve','Actuator','Activates water flow');
/*!40000 ALTER TABLE `tbldevice` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tblmeasurement`
--

DROP TABLE IF EXISTS `tblmeasurement`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tblmeasurement` (
  `DateTime` datetime NOT NULL DEFAULT current_timestamp(),
  `ActionId` varchar(10) NOT NULL,
  `DeviceId` int(11) NOT NULL,
  `Status` int(11) DEFAULT NULL,
  `Warning` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`DateTime`,`ActionId`),
  KEY `DeviceMeasurement_idx` (`DeviceId`),
  KEY `ActionMeasurement_idx` (`ActionId`),
  KEY `WarningMeasurement_idx` (`Warning`),
  KEY `DateTime_ActionId_idx` (`DateTime`,`ActionId`),
  KEY `ActionId_Status_DateTime_idx` (`ActionId`,`Status`,`DateTime`),
  KEY `ActionId_DateTime_Status_idx` (`ActionId`,`DateTime`,`Status`),
  KEY `WarningId_DateTime_ActionId_idx` (`Warning`,`DateTime`,`ActionId`),
  CONSTRAINT `ActionMeasurement` FOREIGN KEY (`ActionId`) REFERENCES `tblaction` (`ActionId`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `DeviceMeasurement` FOREIGN KEY (`DeviceId`) REFERENCES `tbldevice` (`DeviceId`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `WarningMeasurement` FOREIGN KEY (`Warning`) REFERENCES `tblwarning` (`Warningid`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tblmeasurement`
--

LOCK TABLES `tblmeasurement` WRITE;
/*!40000 ALTER TABLE `tblmeasurement` DISABLE KEYS */;
/*!40000 ALTER TABLE `tblmeasurement` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tblwarning`
--

DROP TABLE IF EXISTS `tblwarning`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tblwarning` (
  `Warningid` varchar(10) NOT NULL,
  `Message` varchar(33) DEFAULT NULL,
  PRIMARY KEY (`Warningid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tblwarning`
--

LOCK TABLES `tblwarning` WRITE;
/*!40000 ALTER TABLE `tblwarning` DISABLE KEYS */;
INSERT INTO `tblwarning` VALUES ('COLD','Te weinig zon'),('HOT','Te veel zon'),('WATER','Geen water meer');
/*!40000 ALTER TABLE `tblwarning` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-06-14 15:38:17
