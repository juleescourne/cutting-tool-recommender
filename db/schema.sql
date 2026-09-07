-- phpMyAdmin SQL Dump
-- version 5.0.2
-- https://www.phpmyadmin.net/
--
-- Hôte : 127.0.0.1:3306
-- Généré le : jeu. 01 avr. 2021 à 18:36
-- Version du serveur :  5.7.31
-- Version de PHP : 7.3.21

CREATE DATABASE IF NOT EXISTS cutting CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE cutting;

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de données : `cutting`
--



CREATE TABLE procede(
   `id_procede` int(11) NOT NULL AUTO_INCREMENT,
   `type_procede` VARCHAR(15) DEFAULT NULL,
   `type_operation` VARCHAR(15) DEFAULT NULL,
   `assistance` VARCHAR(15) DEFAULT NULL,
   `debit_mql` float DEFAULT NULL,
   `debit_cryo` float DEFAULT NULL,
   `emulsion` float DEFAULT NULL,
   `vitesse_coupe` float DEFAULT NULL,
   `vitesse_avance_dent` float DEFAULT NULL,
   `vitesse_avance_min` float DEFAULT NULL,
   `profondeur_passe` float DEFAULT NULL,
   `engagement` float DEFAULT NULL,
   `frequence_rotation` float DEFAULT NULL,
   `id_experience` int(11) DEFAULT NULL,
   PRIMARY KEY(`id_procede`),
   KEY `id_experience` (`id_experience`)
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE copeaux(
   `id_copeaux` int(11) NOT NULL AUTO_INCREMENT,
   `epaisseur` float DEFAULT NULL,
   `id_experience` int(11) DEFAULT NULL,
   PRIMARY KEY(`id_copeaux`),
   KEY `id_experience` (`id_experience`)
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE entree_piece(
   `id_entree_piece` int(11) NOT NULL AUTO_INCREMENT,
   `type_matiere` VARCHAR(15) DEFAULT NULL,
   `materiaux` VARCHAR(15) DEFAULT NULL,
   `procede_elaboration` VARCHAR(15) DEFAULT NULL,
   `impression_3d` VARCHAR(15) DEFAULT NULL,
   `longueur_usinee` float DEFAULT NULL,
   `num_passe` int(3) DEFAULT NULL,
   `id_experience` int(11) DEFAULT NULL,
   PRIMARY KEY(`id_entree_piece`),
   KEY `id_experience` (`id_experience`)
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE entree_outil(
   `id_entree_outil` int(11) NOT NULL AUTO_INCREMENT,
   `type_outil` VARCHAR(15) DEFAULT NULL,
   `matiere` VARCHAR(15) DEFAULT NULL,
   `diametre` float DEFAULT NULL,
   `nb_dents_util` int(2) DEFAULT NULL,
   `revetement` VARCHAR(15) DEFAULT NULL,
   `rayon_arrete` float DEFAULT NULL,
   `angle_depouille` float DEFAULT NULL,
   `angle_axial` float DEFAULT NULL,
   `angle_radial` float DEFAULT NULL,
   `angle_attaque` float DEFAULT NULL,
   `angle_listel1` float DEFAULT NULL,
   `angle_listel2` float DEFAULT NULL,
   `id_experience` int(11) DEFAULT NULL,
   PRIMARY KEY(`id_entree_outil`),
   KEY `id_experience` (`id_experience`)
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE sortie_piece(
   `id_sortie_piece` int(11) NOT NULL AUTO_INCREMENT,
   `rugosite` float DEFAULT NULL,
   `durete` float DEFAULT NULL,
   `limite_endurance` float DEFAULT NULL,
   `contrainte_residuelle` float DEFAULT NULL,
   `id_entree_piece` int(11) DEFAULT NULL,
   PRIMARY KEY(`id_sortie_piece`),
   KEY `id_entree_piece` (`id_entree_piece`)
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE temperature_piece(
   `id_temperature_piece` int(11) NOT NULL AUTO_INCREMENT,
   `temps_temperature_piece` float DEFAULT NULL,
   `temperature_piece` float DEFAULT NULL,
   `id_entree_piece` int(11) DEFAULT NULL,
   PRIMARY KEY(`id_temperature_piece`),
   KEY `id_entree_piece` (`id_entree_piece`)
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE effort_piece(
   `id_effort_piece` int(11) NOT NULL AUTO_INCREMENT,
   `temps_effort_piece` float(10) DEFAULT NULL,
   `fx` float DEFAULT NULL,
   `fy` float DEFAULT NULL,
   `fz` float DEFAULT NULL,
   `id_entree_piece` int(11) DEFAULT NULL,
   PRIMARY KEY(`id_effort_piece`),
   KEY `id_entree_piece` (`id_entree_piece`)
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE effort_outil(
   `id_effort_outil` int(11) NOT NULL AUTO_INCREMENT,
   `temps_effort_outil` float DEFAULT NULL,
   `fx` float DEFAULT NULL,
   `fy` float DEFAULT NULL,
   `fz` float DEFAULT NULL,
   `id_entree_outil` int(11) DEFAULT NULL,
   PRIMARY KEY(`id_effort_outil`),
   KEY `id_entree_outil` (`id_entree_outil`)
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE temperature_outil(
   `id_temperature_outil` int(11) NOT NULL AUTO_INCREMENT,
   `temps_temperature_outil` float DEFAULT NULL,
   `temperature_outil` float DEFAULT NULL,
   `id_entree_outil` int(11) DEFAULT NULL,
   PRIMARY KEY(`id_temperature_outil`),
   KEY `id_entree_outil` (`id_entree_outil`)
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE usure_outil(
   `id_usure_outil` int(11) NOT NULL AUTO_INCREMENT,
   `temps_usinage` float DEFAULT NULL,
   `vb` float DEFAULT NULL,
   `Er` float DEFAULT NULL,
   `Kt` float DEFAULT NULL,
   `id_entree_outil` int(11) DEFAULT NULL,
   PRIMARY KEY(`id_usure_outil`),
   KEY `id_entree_outil` (`id_entree_outil`)
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE experience(
   `id_experience` int(11) NOT NULL AUTO_INCREMENT,
   `nom`  varchar(100) DEFAULT NULL,
   PRIMARY KEY(`id_experience`)
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE vibration(
   `temps_vibration` float DEFAULT NULL,
   `frequence` float DEFAULT NULL,
   `amplitude` float DEFAULT NULL,
   `id_entree_piece` int(11) NOT NULL,
   `id_entree_outil` int(11) NOT NULL,
   PRIMARY KEY(`id_entree_piece`, `id_entree_outil`, `temps_vibration`),
   KEY `id_entree_piece` (`id_entree_piece`),
   KEY `id_entree_outil` (`id_entree_outil`)
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

