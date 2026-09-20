-- Tabela para armazenar os dados dos usuários (para o sistema de login e cadastro)
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    is_premium INTEGER DEFAULT 0 -- 0 = não premium, 1 = premium
);


-- Tabela para armazenar os materiais de construção
CREATE TABLE materials (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    image_url TEXT,
    caption TEXT,
    description TEXT
);

-- Tabela para armazenar as vantagens (pros) de cada material
CREATE TABLE pros (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    material_id INTEGER,
    pro_text TEXT NOT NULL,
    FOREIGN KEY (material_id) REFERENCES materials (id)
);

-- Tabela para armazenar as desvantagens (cons) de cada material
CREATE TABLE cons (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    material_id INTEGER,
    con_text TEXT NOT NULL,
    FOREIGN KEY (material_id) REFERENCES materials (id)
);

-- Tabela para armazenar as marcas e fornecedores associados a cada material
CREATE TABLE brands (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    material_id INTEGER,
    position INTEGER NOT NULL,
    name TEXT NOT NULL,
    rating REAL,
    price_observation TEXT,
    FOREIGN KEY (material_id) REFERENCES materials (id)
);

-- Inserindo os dados dos materiais da sua página 'index.html'
INSERT INTO materials (id, name, image_url, caption, description) VALUES
(1, 'Blocos de Construção', 'ZCZ3PTc0MA.jpg', 'Bloco de construção utilizado em alvenaria.', 'Elementos modulares essenciais para construção de paredes e muros em alvenaria.'),
(2, 'Lajes Pré-moldadas', 'laje.jpeg', 'Laje treliçada com EPS sendo montada.', 'Estruturas planas, geralmente de concreto com enchimento cerâmico ou EPS, utilizadas para criar pisos e tetos.'),
(3, 'Pilares de Concreto', 'akM5VFN4NHM.jpg', 'Pilares de concreto armado com esperas para vigas.', 'Elementos estruturais verticais que recebem as cargas das vigas e lajes, transferindo-as para as fundações.'),
(4, 'Vigas de Concreto', 'viga.jpg', 'Estrutura pré-moldada de concreto com vigas e pilares.', 'Elementos estruturais horizontais ou inclinados que suportam lajes e paredes, transferindo as cargas para os pilares.');

-- Vantagens e Desvantagens
INSERT INTO pros (material_id, pro_text) VALUES
(1, 'Instalação rápida'), (1, 'Isolamento térmico e acústico'), (1, 'Variedade de tamanhos e formatos'),
(2, 'Montagem rápida e eficiente'), (2, 'Redução de custos com mão de obra e material'), (2, 'Bom isolamento termoacústico (especialmente com EPS)'),
(3, 'Alta resistência à compressão'), (3, 'Durabilidade e longa vida útil'), (3, 'Versatilidade em formas e tamanhos'),
(4, 'Suporte para grandes vãos'), (4, 'Integração com lajes e pilares'), (4, 'Resistência a esforços de flexão');

INSERT INTO cons (material_id, con_text) VALUES
(1, 'Requer mão de obra qualificada'), (1, 'Necessita de revestimento'), (1, 'Fragilidade antes da aplicação'),
(2, 'Requer planejamento preciso e escoramento adequado'), (2, 'Limitações em grandes vãos (dependendo do tipo)'), (2, 'Necessidade de capeamento de concreto'),
(3, 'Peso próprio elevado'), (3, 'Requer fôrmas e escoramento durante a execução'), (3, 'Tempo de cura do concreto'),
(4, 'Complexidade na armação (se moldada in loco)'), (4, 'Necessidade de fôrmas e escoramento (in loco)'), (4, 'Interferência em layouts (vigas aparentes)');

-- Marcas e Fornecedores
INSERT INTO brands (material_id, position, name, rating, price_observation) VALUES
(1, 1, 'Votoran', 9.5, 'R$ 2,50/un'), (1, 2, 'Tegra', 9.3, 'R$ 2,70/un'), (1, 3, 'Blocos Rápidos', 6.2, 'R$ 1,80/un'),
(2, 1, 'LajesProtend', 9.6, 'R$ 80,00'), (2, 2, 'Precon', 9.2, 'R$ 85,00'), (2, 3, 'TecLaje', 8.9, 'R$ 75,00'),
(3, 1, 'Engemix (Concreto)', 9.4, 'Preço varia com projeto'), (3, 2, 'Gerdau (Aço)', 9.7, 'Preço varia com projeto'), (3, 3, 'Concreviga (Soluções)', 9.0, 'Preço varia com projeto'),
(4, 1, 'Holcim (Concreto)', 9.3, 'Preço varia com projeto'), (4, 2, 'ArcelorMittal (Aço)', 9.5, 'Preço varia com projeto'), (4, 3, 'Viga Forte (Pré-moldados)', 8.8, 'Preço varia com projeto');
