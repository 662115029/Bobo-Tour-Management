-- ======================
-- ADMINS
-- ======================
CREATE TABLE admins (
    admin_id VARCHAR(36) PRIMARY KEY,
    name VARCHAR(100),
    password_hash VARCHAR(255),
    status VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ======================
-- EMPLOYERS
-- ======================
CREATE TABLE employers (
    em_id VARCHAR(36) PRIMARY KEY,
    em_username VARCHAR(100) UNIQUE,
    em_password_hash VARCHAR(255),

    em_name VARCHAR(250),
    em_phone VARCHAR(20),
    em_address TEXT,
    em_bio VARCHAR(250),

    em_profile_image_url TEXT,

    em_verify_status ENUM('NOT_VERIFIED','PENDING','VERIFIED') DEFAULT 'NOT_VERIFIED',
    em_is_active BOOLEAN DEFAULT TRUE,

    em_rating_avg DECIMAL(2,1) DEFAULT 0.0,

    em_created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    em_updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- ======================
-- FREELANCERS
-- ======================
CREATE TABLE freelancers (
    fl_id VARCHAR(36) PRIMARY KEY,
    line_user_id VARCHAR(100) UNIQUE,

    fl_name VARCHAR(100),
    fl_pin_hash VARCHAR(255),

    fl_date_of_birth DATE,
    fl_address TEXT,
    fl_bio VARCHAR(250),

    fl_profile_image_url TEXT,

    fl_verify_status ENUM('NOT_VERIFIED','PENDING','VERIFIED') DEFAULT 'NOT_VERIFIED',
    fl_is_active BOOLEAN DEFAULT TRUE,

    fl_rating_avg DECIMAL(2,1) DEFAULT 0.0,

    fl_created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fl_updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);