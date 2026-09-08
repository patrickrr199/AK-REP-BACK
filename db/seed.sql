-- seed.sql — datos de prueba, todos ficticios (alice@example.com, "Test Product N", etc.)

INSERT INTO users (id, email, password, role) VALUES
(1, 'admin@example.com', 'admin123', 'admin'),
(2, 'root@example.com', 'toor', 'admin'),
(3, 'alice@example.com', 'alice123', 'customer'),
(4, 'bob@example.com', 'bobpass1', 'customer'),
(5, 'carol@example.com', 'carol123', 'customer'),
(6, 'dave@example.com', 'davepass1', 'customer'),
(7, 'erin@example.com', 'erin123', 'customer'),
(8, 'frank@example.com', 'frankpass1', 'customer'),
(9, 'grace@example.com', 'grace123', 'customer'),
(10, 'heidi@example.com', 'heidipass1', 'customer');
SELECT setval('users_id_seq', 10);

INSERT INTO products (id, seller_id, title, description, price, stock) VALUES
(1, 3, 'Test Product 1', 'Auriculares inalámbricos de prueba', 29.99, 50),
(2, 3, 'Test Product 2', 'Teclado mecánico de prueba', 59.99, 20),
(3, 4, 'Test Product 3', 'Mouse ergonómico de prueba', 19.99, 35),
(4, 4, 'Test Product 4', 'Monitor 24" de prueba', 149.99, 10),
(5, 5, 'Test Product 5', 'Webcam HD de prueba', 39.99, 25),
(6, 5, 'Test Product 6', 'Silla de oficina de prueba', 199.99, 8),
(7, 6, 'Test Product 7', 'Lámpara LED de escritorio', 24.99, 40),
(8, 6, 'Test Product 8', 'Mochila para laptop', 44.99, 30),
(9, 7, 'Test Product 9', 'Cargador USB-C 65W', 22.99, 60),
(10, 7, 'Test Product 10', 'Disco SSD 1TB', 89.99, 15),
(11, 8, 'Test Product 11', 'Router WiFi 6', 79.99, 12),
(12, 8, 'Test Product 12', 'Altavoz Bluetooth', 34.99, 45),
(13, 9, 'Test Product 13', 'Funda para tablet', 14.99, 55),
(14, 9, 'Test Product 14', 'Hub USB 7 puertos', 27.99, 33),
(15, 10, 'Test Product 15', 'Micrófono USB', 49.99, 18),
(16, 10, 'Test Product 16', 'Soporte para monitor', 32.99, 22),
(17, 3, 'Test Product 17', 'Batería externa 20000mAh', 36.99, 28),
(18, 4, 'Test Product 18', 'Cable HDMI 2m', 9.99, 100);
SELECT setval('products_id_seq', 18);

INSERT INTO orders (id, buyer_id, product_id, quantity, status) VALUES
(1, 3, 1, 1, 'paid'),
(2, 4, 2, 2, 'pending'),
(3, 5, 3, 1, 'shipped'),
(4, 6, 4, 1, 'paid'),
(5, 7, 5, 3, 'pending'),
(6, 8, 6, 1, 'shipped'),
(7, 9, 7, 2, 'paid'),
(8, 10, 8, 1, 'pending'),
(9, 3, 9, 1, 'shipped'),
(10, 4, 10, 1, 'paid'),
(11, 5, 11, 2, 'pending'),
(12, 6, 12, 1, 'shipped'),
(13, 7, 13, 3, 'paid'),
(14, 8, 14, 1, 'pending'),
(15, 9, 15, 1, 'shipped'),
(16, 10, 16, 2, 'paid'),
(17, 3, 17, 1, 'pending'),
(18, 4, 18, 4, 'shipped'),
(19, 5, 1, 1, 'paid'),
(20, 6, 2, 1, 'pending'),
(21, 7, 3, 2, 'shipped'),
(22, 8, 4, 1, 'paid'),
(23, 9, 5, 1, 'pending'),
(24, 10, 6, 1, 'shipped');
SELECT setval('orders_id_seq', 24);

-- VULN: xss-stored — comment #2 carries a stored XSS payload on purpose so the
-- product detail page (which renders comment bodies with v-html) fires it.
INSERT INTO comments (id, product_id, author_id, body) VALUES
(1, 1, 3, 'Excelente producto, muy recomendado.'),
(2, 1, 4, '<img src=x onerror="alert(''xss'')">'),
(3, 1, 5, 'Llegó rápido y en buen estado.'),
(4, 2, 6, 'La calidad es buena para el precio.'),
(5, 2, 7, 'No es tan silencioso como esperaba.'),
(6, 3, 8, 'Perfecto para uso diario de oficina.'),
(7, 3, 9, 'El envío tardó más de lo esperado.'),
(8, 4, 10, 'Excelente resolución de pantalla.'),
(9, 4, 3, 'Un poco caro pero vale la pena.'),
(10, 5, 4, 'La imagen se ve muy nítida.'),
(11, 5, 5, 'Fácil de configurar.'),
(12, 6, 6, 'Muy cómoda para largas jornadas.'),
(13, 6, 7, 'El ensamblaje fue sencillo.'),
(14, 7, 8, 'Buena luz para leer de noche.'),
(15, 7, 9, 'El brazo articulado es útil.'),
(16, 8, 10, 'Resistente y con buen espacio.'),
(17, 8, 3, 'Las correas podrían ser más acolchadas.'),
(18, 9, 4, 'Carga rápido mi teléfono.'),
(19, 9, 5, 'Cable incluido de buena calidad.'),
(20, 10, 6, 'Velocidad de lectura excelente.'),
(21, 10, 7, 'Instalación sencilla en mi laptop.'),
(22, 11, 8, 'Buena cobertura en toda la casa.'),
(23, 11, 9, 'La configuración inicial fue algo confusa.'),
(24, 12, 10, 'Sonido claro y buen volumen.'),
(25, 12, 3, 'La batería dura bastante.'),
(26, 13, 4, 'Se ajusta bien a mi tablet.'),
(27, 13, 5, 'Material resistente a rayones.'),
(28, 14, 6, 'Todos los puertos funcionan bien.'),
(29, 14, 7, 'Compacto y fácil de transportar.'),
(30, 15, 8, 'Buena calidad de audio para streaming.'),
(31, 15, 9, 'Se conecta rápido por USB.'),
(32, 16, 10, 'Estable y ajustable en altura.');
SELECT setval('comments_id_seq', 32);
