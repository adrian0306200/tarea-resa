CREATE DATABASE bike_registry;
USE bike_registry;

CREATE TABLE bicycles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    brand VARCHAR(50) NOT NULL,
    model VARCHAR(50) NOT NULL,
    year INT NOT NULL
);
