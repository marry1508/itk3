drop database scootech;
create database scootech;
use scootech;

create table escooter (
	scooter_ID			integer auto_increment not null,
    standort			varchar(50),
    mietpreis			decimal(10,2),
    primary key (scooter_ID)
);

create table kunde (
	kunden_ID			integer auto_increment not null,
    vorname				varchar(50),
    nachname			varchar(50),
    passwort            varchar(50),
    primary key (kunden_ID)
);

create table mietvorgang (
	mietvorgang_ID		integer auto_increment not null,
    scooter_ID			integer not null,
    kunden_ID			integer not null,
    startzeit			datetime,
    endzeit				datetime,
    preis				decimal(10,2),
    abgeschlossen		boolean,
    primary key (mietvorgang_ID),
    foreign key (scooter_ID) references escooter (scooter_ID),
    foreign key (kunden_ID) references kunde (kunden_ID)
);
    