-- Tabla tbl_configuration
CREATE TABLE tbl_configuration (
    key VARCHAR(64) PRIMARY KEY,
    content NVARCHAR(MAX) NOT NULL CHECK (ISJSON(content) = 1),
    created_at DATETIMEOFFSET DEFAULT SYSDATETIMEOFFSET(),
    updated_at DATETIMEOFFSET DEFAULT SYSDATETIMEOFFSET()
);

-- Tabla tbl_category
CREATE TABLE tbl_category (
    id BIGINT PRIMARY KEY IDENTITY(1000,1),
    name TEXT NOT NULL,
    created_at DATETIMEOFFSET DEFAULT SYSDATETIMEOFFSET(),
    updated_at DATETIMEOFFSET DEFAULT SYSDATETIMEOFFSET()
);

-- Tabla tbl_team_member
CREATE TABLE tbl_team_member (
    id BIGINT IDENTITY(1000,1) PRIMARY KEY,
    name VARCHAR(60) NOT NULL,  -- Limite de 60 caracteres
    photo_url VARCHAR(2048),    -- Limite de 2048 caracteres para la URL
    description VARCHAR(500),   -- Limite de 500 caracteres
    role VARCHAR(100),          -- Limite de 100 caracteres para el rol
    created_at DATETIMEOFFSET DEFAULT SYSDATETIMEOFFSET(),
    updated_at DATETIMEOFFSET DEFAULT SYSDATETIMEOFFSET()
);

-- Tabla tbl_social_platform
CREATE TABLE tbl_social_platform (
    id BIGINT IDENTITY(1000,1) PRIMARY KEY,
    name VARCHAR(60) NOT NULL UNIQUE,  -- Limite de 60 caracteres
    icon_url VARCHAR(1024), -- Limite de 1024 caracteres
    created_at DATETIMEOFFSET DEFAULT SYSDATETIMEOFFSET(),
    updated_at DATETIMEOFFSET DEFAULT SYSDATETIMEOFFSET()
);

-- Tabla tbl_social_media
CREATE TABLE tbl_social_media (
    id BIGINT IDENTITY(1000,1) PRIMARY KEY,
    team_member_id BIGINT FOREIGN KEY REFERENCES tbl_team_member(id) ON DELETE CASCADE,
    url VARCHAR(2048) NOT NULL,  -- Limite de 512 caracteres para la URL
    platform_id BIGINT FOREIGN KEY REFERENCES tbl_social_platform(id) ON DELETE CASCADE,
    updated_at DATETIMEOFFSET DEFAULT SYSDATETIMEOFFSET(),
    created_at DATETIMEOFFSET DEFAULT SYSDATETIMEOFFSET()
);

-- Tabla tbl_contact_us
CREATE TABLE tbl_contact_us (
    id BIGINT IDENTITY(1000,1) PRIMARY KEY,
    created_at DATETIMEOFFSET DEFAULT SYSDATETIMEOFFSET(),
    name VARCHAR(64) NOT NULL,  
    status VARCHAR(64) NOT NULL,  
    email VARCHAR(255) NOT NULL, -- Limite de 255 caracteres
    message VARCHAR(1000) NOT NULL, -- Limite de 1000 caracteres
    updated_at DATETIMEOFFSET DEFAULT SYSDATETIMEOFFSET()
);

-- Tabla tbl_history_status
CREATE TABLE tbl_history_status (
    id BIGINT IDENTITY(1000,1) PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE,  -- Limite de 255 caracteres para el nombre y único
    created_at DATETIMEOFFSET DEFAULT SYSDATETIMEOFFSET(),
    updated_at DATETIMEOFFSET DEFAULT SYSDATETIMEOFFSET()
);

-- Tabla tbl_profile
CREATE TABLE tbl_profile (
    id BIGINT IDENTITY(1000,1) PRIMARY KEY,
    first_name VARCHAR(60) NOT NULL,  -- Limite de 60 caracteres
    last_name VARCHAR(60) NOT NULL,   -- Limite de 60 caracteres
    email VARCHAR(255) NOT NULL UNIQUE, -- Limite de 255 caracteres
    password_hash VARCHAR(255) NOT NULL, -- Limite de 255 caracteres
    salt VARCHAR(255) NOT NULL,         -- Limite de 255 caracteres
    created_at DATETIMEOFFSET DEFAULT SYSDATETIMEOFFSET(), -- Fecha de creación con zona horaria
    updated_at DATETIMEOFFSET DEFAULT SYSDATETIMEOFFSET(), -- Fecha de actualización con zona horaria
    is_active BIT DEFAULT 1             -- Valor por defecto 1 (activo)
);

-- Tabla tbl_timeline_year
CREATE TABLE tbl_timeline_year (
    year INT PRIMARY KEY,
    title TEXT NOT NULL, 
    description TEXT,
    image_url TEXT,
    created_at DATETIMEOFFSET DEFAULT SYSDATETIMEOFFSET(),
    updated_at DATETIMEOFFSET DEFAULT SYSDATETIMEOFFSET(),
    is_active BIT DEFAULT 1
);

-- Tabla tbl_timeline_year_category
CREATE TABLE tbl_timeline_year_category (
    id BIGINT IDENTITY(1000,1) PRIMARY KEY,
    timeline_year INT FOREIGN KEY REFERENCES tbl_timeline_year(year) ON DELETE CASCADE,
    category_id BIGINT FOREIGN KEY REFERENCES tbl_category(id) ON DELETE CASCADE
);

-- Tabla tbl_timeline_history
CREATE TABLE tbl_timeline_history (
    id BIGINT IDENTITY(1000,1) PRIMARY KEY,
    main_image_url VARCHAR(2048),
    title VARCHAR(255) NOT NULL,
    created_at DATETIMEOFFSET DEFAULT SYSDATETIMEOFFSET(),
    status_id BIGINT FOREIGN KEY REFERENCES tbl_history_status(id),
    timeline_id INT FOREIGN KEY REFERENCES tbl_timeline_year(year) ON DELETE CASCADE,
    category_id BIGINT FOREIGN KEY REFERENCES tbl_category(id) ON DELETE CASCADE,
    event_date DATE,
    updated_at DATETIMEOFFSET DEFAULT SYSDATETIMEOFFSET()
);

-- Tabla tbl_timeline_history_category
CREATE TABLE tbl_timeline_history_category (
  id BIGINT IDENTITY(1000,1) PRIMARY KEY, -- Campo id con auto incremento
  timeline_history_id BIGINT FOREIGN KEY REFERENCES tbl_timeline_history(id) ON DELETE NO ACTION, -- Relación con timeline_history
  category_id BIGINT FOREIGN KEY REFERENCES tbl_category(id) ON DELETE NO ACTION -- Relación con category
);

-- Tabla tbl_timeline_section
CREATE TABLE tbl_timeline_section (
  id BIGINT IDENTITY(1000,1) PRIMARY KEY,
  history_id BIGINT FOREIGN KEY REFERENCES tbl_timeline_history(id) ON DELETE NO ACTION, -- Relación con timeline_history
  title VARCHAR(255) NOT NULL,
  description VARCHAR(1000),
  multimedia_url VARCHAR(2048),
  created_at DATETIMEOFFSET DEFAULT SYSDATETIMEOFFSET(),
  template VARCHAR(255),
  updated_at DATETIMEOFFSET DEFAULT SYSDATETIMEOFFSET()
);

-- Tabla tbl_timeline_history_observations
CREATE TABLE tbl_timeline_history_observations (
    id BIGINT IDENTITY(1000,1) PRIMARY KEY,
    history_id BIGINT FOREIGN KEY REFERENCES tbl_timeline_history(id) ON DELETE CASCADE,
    message VARCHAR(1000) NOT NULL,
    email VARCHAR(255),
    created_at DATETIMEOFFSET DEFAULT SYSDATETIMEOFFSET(),
    updated_at DATETIMEOFFSET DEFAULT SYSDATETIMEOFFSET()
);

-- Triggers para actualizar updated_at
CREATE TRIGGER trg_tbl_configuration_update
ON tbl_configuration
AFTER UPDATE
AS
BEGIN
    SET NOCOUNT ON;
    UPDATE tbl_configuration
    SET updated_at = SYSDATETIMEOFFSET()
    FROM inserted i
    WHERE tbl_configuration.id = i.id;
END;

CREATE TRIGGER trg_tbl_category_update
ON tbl_category
AFTER UPDATE
AS
BEGIN
    SET NOCOUNT ON;
    UPDATE tbl_category
    SET updated_at = SYSDATETIMEOFFSET()
    FROM inserted i
    WHERE tbl_category.id = i.id;
END;

CREATE TRIGGER trg_tbl_team_member_update
ON tbl_team_member
AFTER UPDATE
AS
BEGIN
    SET NOCOUNT ON;
    UPDATE tbl_team_member
    SET updated_at = SYSDATETIMEOFFSET()
    FROM inserted i
    WHERE tbl_team_member.id = i.id;
END;

CREATE TRIGGER trg_tbl_social_platform_update
ON tbl_social_platform
AFTER UPDATE
AS
BEGIN
    SET NOCOUNT ON;
    UPDATE tbl_social_platform
    SET updated_at = SYSDATETIMEOFFSET()
    FROM inserted i
    WHERE tbl_social_platform.id = i.id;
END;

CREATE TRIGGER trg_tbl_social_media_update
ON tbl_social_media
AFTER UPDATE
AS
BEGIN
    SET NOCOUNT ON;
    UPDATE tbl_social_media
    SET updated_at = SYSDATETIMEOFFSET()
    FROM inserted i
    WHERE tbl_social_media.id = i.id;
END;

CREATE TRIGGER trg_tbl_contact_us_update
ON tbl_contact_us
AFTER UPDATE
AS
BEGIN
    SET NOCOUNT ON;
    UPDATE tbl_contact_us
    SET updated_at = SYSDATETIMEOFFSET()
    FROM inserted i
    WHERE tbl_contact_us.id = i.id;
END;

CREATE TRIGGER trg_tbl_history_status_update
ON tbl_history_status
AFTER UPDATE
AS
BEGIN
    SET NOCOUNT ON;
    UPDATE tbl_history_status
    SET updated_at = SYSDATETIMEOFFSET()
    FROM inserted i
    WHERE tbl_history_status.id = i.id;
END;

CREATE TRIGGER trg_tbl_profile_update
ON tbl_profile
AFTER UPDATE
AS
BEGIN
    SET NOCOUNT ON;
    UPDATE tbl_profile
    SET updated_at = SYSDATETIMEOFFSET()
    FROM inserted i
    WHERE tbl_profile.id = i.id;
END;

CREATE TRIGGER trg_timeline_year_update
ON tbl_timeline_year
AFTER UPDATE
AS
BEGIN
    SET NOCOUNT ON;
    UPDATE tbl_timeline_year
    SET updated_at = SYSDATETIMEOFFSET()
    FROM inserted i
    WHERE tbl_timeline_year.year = i.year;
END;

CREATE TRIGGER trg_timeline_history_update
ON tbl_timeline_history
AFTER UPDATE
AS
BEGIN
    SET NOCOUNT ON;
    UPDATE tbl_timeline_history
    SET updated_at = SYSDATETIMEOFFSET()
    FROM inserted i
    WHERE tbl_timeline_history.id = i.id;
END;

CREATE TRIGGER trg_timeline_section_update
ON tbl_timeline_section
AFTER UPDATE
AS
BEGIN
    SET NOCOUNT ON;
    UPDATE tbl_timeline_section
    SET updated_at = SYSDATETIMEOFFSET()
    FROM inserted i
    WHERE tbl_timeline_section.id = i.id;
END;

CREATE TRIGGER trg_timeline_history_observations_update
ON tbl_timeline_history_observations
AFTER UPDATE
AS
BEGIN
    SET NOCOUNT ON;
    UPDATE tbl_timeline_history_observations
    SET updated_at = SYSDATETIMEOFFSET()
    FROM inserted i
    WHERE tbl_timeline_history_observations.id = i.id;
END;
