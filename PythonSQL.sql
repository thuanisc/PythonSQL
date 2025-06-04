CREATE DATABASE PythonSQL;

USE PythonSQL;

SHOW TABLES;

DESCRIBE usuarios;

SELECT * FROM usuarios;

SELECT u.nome, l.titulo, e.data_emprestimo
FROM usuarios u
JOIN emprestimos e ON u.id = e.usuario_id
JOIN livros l ON l.id = e.livro_id;
