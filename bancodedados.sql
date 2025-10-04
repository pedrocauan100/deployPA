CREATE DATABASE IF NOT EXISTS deployPA;
USE deployPA;


CREATE TABLE IF NOT EXISTS usuarios (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nome VARCHAR(100),
    email VARCHAR(200) UNIQUE NOT NULL,
    senha VARCHAR(300) NOT NULL,
    tipo VARCHAR(50) NOT NULL
);


INSERT INTO usuarios (nome, email, senha, tipo) VALUES 
('Maria', 'maria@email.com', '123', 'cliente'),
('João', 'joao@email.com', '123', 'cliente'),
('Pedro', 'pedro@email.com', '123', 'admin'),
('Carlo', 'carlo@email.com', '123', 'admin');


CREATE TABLE IF NOT EXISTS produtos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    preco DECIMAL(10, 2) NOT NULL,
    descricao TEXT,
    imagem VARCHAR(255),
    tipo ENUM('eletronico', 'livro', 'esporte', 'acessorio') NOT NULL,
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


INSERT INTO produtos (nome, preco, descricao, imagem, tipo) VALUES
('Smartphone XYZ', 899.99, 'Smartphone com câmera de alta resolução e bateria de longa duração', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSNFsq9qmG36Ek55tCywElinlpzKrlpIjnZnw&s', 'eletronico'),
('Bola de Futebol', 79.90, 'Bola oficial para partidas profissionais', 'https://a-static.mlcdn.com.br/1500x1500/bola-futebol-campo-oficial-penalty-profissional-s11-r2-xxiii/acribludecor/a6a800f0c97a11eda0924201ac185033/67570c2005fe7ea24e76fbae774b827f.jpeg', 'esporte'),
('Relógio Inteligente', 299.99, 'Monitor seus exercícios e notificações do smartphone', 'https://a-static.mlcdn.com.br/800x560/relogio-inteligente-smartwatch-masculino-t200-ultra-9-original-compativel-c-samsung-xiaomi-hapes/hapes/smart-ultra9-p-501/808f1efb909a2cb93ab9441225af4ae4.jpeg', 'acessorio');
