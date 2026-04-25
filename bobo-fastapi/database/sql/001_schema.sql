CREATE TABLE admins (
    admin_id    VARCHAR(20) PRIMARY KEY,
    name        VARCHAR(100) NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    status      VARCHAR(20) NOT NULL DEFAULT 'active' CHECK (status IN ('active','inactive')),
    created_at  TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE admin_logs (
    log_id      VARCHAR(20) PRIMARY KEY,
    admin_id    VARCHAR(20) NOT NULL,
    action      VARCHAR(255) NOT NULL,
    created_at  TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_admin_logs_admin FOREIGN KEY (admin_id) REFERENCES admins(admin_id)
);

CREATE TABLE employers (
    em_id               VARCHAR(20) PRIMARY KEY,
    em_username         VARCHAR(100) NOT NULL UNIQUE,
    em_password_hash    VARCHAR(255) NOT NULL,
    em_name             VARCHAR(150) NOT NULL,
    em_phone            VARCHAR(20),
    em_address          TEXT,
    em_bio              TEXT,
    em_profile_image_url VARCHAR(500),
    em_verify_status    VARCHAR(20) NOT NULL DEFAULT 'PENDING' CHECK (em_verify_status IN ('PENDING','VERIFIED','NOT_VERIFIED')),
    em_is_active        BOOLEAN NOT NULL DEFAULT true,
    em_rating_avg       NUMERIC(3,1) DEFAULT 0.0,
    em_created_at       TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    em_updated_at       TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE freelancers (
    fl_id               VARCHAR(20) PRIMARY KEY,
    line_user_id        VARCHAR(100) UNIQUE,
    fl_name             VARCHAR(150) NOT NULL,
    fl_pin_hash         VARCHAR(255) NOT NULL,
    fl_date_of_birth    DATE,
    fl_address          TEXT,
    fl_bio              TEXT,
    fl_profile_image_url VARCHAR(500),
    fl_verify_status    VARCHAR(20) NOT NULL DEFAULT 'PENDING' CHECK (fl_verify_status IN ('PENDING','VERIFIED','NOT_VERIFIED')),
    fl_is_active        BOOLEAN NOT NULL DEFAULT true,
    fl_rating_avg       NUMERIC(3,1) DEFAULT 0.0,
    fl_created_at       TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    fl_updated_at       TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE fl_vehicle (
    fl_vehicle_id           VARCHAR(20) PRIMARY KEY,
    fl_id                   VARCHAR(20) NOT NULL,
    fl_vehicle_type         VARCHAR(20) NOT NULL DEFAULT 'VAN' CHECK (fl_vehicle_type = 'VAN'),
    fl_vehicle_brand        VARCHAR(50) NOT NULL,
    fl_vehicle_model        VARCHAR(50) NOT NULL,
    fl_vehicle_year         SMALLINT NOT NULL,
    fl_vehicle_seat_capa    SMALLINT NOT NULL CHECK (fl_vehicle_seat_capa BETWEEN 9 AND 13),
    fl_vehicle_license_plate VARCHAR(50) NOT NULL,
    CONSTRAINT fk_fl_vehicle_fl FOREIGN KEY (fl_id) REFERENCES freelancers(fl_id)
);

CREATE TABLE fl_vehicle_images (
    fl_vehicle_image_id VARCHAR(20) PRIMARY KEY,
    fl_vehicle_id       VARCHAR(20) NOT NULL,
    fl_vehicle_image_url VARCHAR(500) NOT NULL,
    CONSTRAINT fk_fl_vehicle_images_vehicle FOREIGN KEY (fl_vehicle_id) REFERENCES fl_vehicle(fl_vehicle_id)
);

CREATE TABLE fl_languages (
    fl_language_id  VARCHAR(20) PRIMARY KEY,
    fl_id           VARCHAR(20) NOT NULL,
    fl_language_name VARCHAR(50) NOT NULL,
    CONSTRAINT fk_fl_languages_fl FOREIGN KEY (fl_id) REFERENCES freelancers(fl_id)
);

CREATE TABLE fl_pickup_areas (
    fl_area_id  VARCHAR(20) PRIMARY KEY,
    fl_id       VARCHAR(20) NOT NULL,
    fl_area_name VARCHAR(100) NOT NULL,
    CONSTRAINT fk_fl_pickup_areas_fl FOREIGN KEY (fl_id) REFERENCES freelancers(fl_id)
);

CREATE TABLE fl_availability (
    fl_available_id         VARCHAR(20) PRIMARY KEY,
    fl_id                   VARCHAR(20) NOT NULL,
    fl_available_start_date DATE NOT NULL,
    fl_available_end_date   DATE NOT NULL,
    is_active               BOOLEAN NOT NULL DEFAULT true,
    CONSTRAINT fk_fl_availability_fl FOREIGN KEY (fl_id) REFERENCES freelancers(fl_id)
);

CREATE TABLE fl_documents (
    fl_doc_id       VARCHAR(20) PRIMARY KEY,
    fl_id           VARCHAR(20) NOT NULL,
    fl_vehicle_id   VARCHAR(20),
    fl_doc_type     VARCHAR(50) NOT NULL CHECK (fl_doc_type IN ('ID_CARD','DRIVER_LICENSE','PUBLIC_DRIVER_LICENSE','VEHICLE_REGISTRATION','VEHICLE_INSURANCE')),
    file_url        VARCHAR(500) NOT NULL,
    fl_doc_status   VARCHAR(20) NOT NULL DEFAULT 'PENDING' CHECK (fl_doc_status IN ('PENDING','APPROVED','REJECTED')),
    is_latest       BOOLEAN NOT NULL DEFAULT true,
    fl_uploaded_at  TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    reviewed_by     VARCHAR(20),
    reviewed_at     TIMESTAMP,
    CONSTRAINT fk_fl_documents_fl      FOREIGN KEY (fl_id)         REFERENCES freelancers(fl_id),
    CONSTRAINT fk_fl_documents_vehicle FOREIGN KEY (fl_vehicle_id) REFERENCES fl_vehicle(fl_vehicle_id),
    CONSTRAINT fk_fl_documents_admin   FOREIGN KEY (reviewed_by)   REFERENCES admins(admin_id)
);

CREATE TABLE fl_verification (
    fl_verify_id        VARCHAR(20) PRIMARY KEY,
    fl_id               VARCHAR(20) NOT NULL UNIQUE,
    fl_verify_status    VARCHAR(20) NOT NULL DEFAULT 'PENDING' CHECK (fl_verify_status IN ('PENDING','VERIFIED','NOT_VERIFIED')),
    fl_submitted_at     TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    fl_verified_at      TIMESTAMP,
    reviewed_by         VARCHAR(20),
    CONSTRAINT fk_fl_verification_fl    FOREIGN KEY (fl_id)       REFERENCES freelancers(fl_id),
    CONSTRAINT fk_fl_verification_admin FOREIGN KEY (reviewed_by) REFERENCES admins(admin_id)
);

CREATE TABLE em_documents (
    em_doc_id       VARCHAR(20) PRIMARY KEY,
    em_id           VARCHAR(20) NOT NULL,
    em_doc_type     VARCHAR(50) NOT NULL CHECK (em_doc_type IN ('COMPANY_REGISTRATION','TAX_ID','OTHER')),
    file_url        VARCHAR(500) NOT NULL,
    em_doc_status   VARCHAR(20) NOT NULL DEFAULT 'PENDING' CHECK (em_doc_status IN ('PENDING','APPROVED','REJECTED')),
    is_latest       BOOLEAN NOT NULL DEFAULT true,
    em_uploaded_at  TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    reviewed_by     VARCHAR(20),
    reviewed_at     TIMESTAMP,
    CONSTRAINT fk_em_documents_em    FOREIGN KEY (em_id)       REFERENCES employers(em_id),
    CONSTRAINT fk_em_documents_admin FOREIGN KEY (reviewed_by) REFERENCES admins(admin_id)
);

CREATE TABLE em_verification (
    em_verify_id        VARCHAR(20) PRIMARY KEY,
    em_id               VARCHAR(20) NOT NULL UNIQUE,
    em_verify_status    VARCHAR(20) NOT NULL DEFAULT 'PENDING' CHECK (em_verify_status IN ('PENDING','VERIFIED','NOT_VERIFIED')),
    em_submitted_at     TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    em_verified_at      TIMESTAMP,
    reviewed_by         VARCHAR(20),
    CONSTRAINT fk_em_verification_em    FOREIGN KEY (em_id)       REFERENCES employers(em_id),
    CONSTRAINT fk_em_verification_admin FOREIGN KEY (reviewed_by) REFERENCES admins(admin_id)
);

CREATE TABLE jobs (
    job_id                  VARCHAR(20) PRIMARY KEY,
    em_id                   VARCHAR(20) NOT NULL,
    job_title               VARCHAR(200) NOT NULL,
    job_description         TEXT,
    job_start_date          DATE NOT NULL,
    job_end_date            DATE NOT NULL,
    job_required_vehicle_type VARCHAR(20) NOT NULL DEFAULT 'VAN' CHECK (job_required_vehicle_type = 'VAN'),
    job_required_seat       SMALLINT NOT NULL CHECK (job_required_seat BETWEEN 9 AND 13),
    job_price               NUMERIC(12,2) NOT NULL,
    job_status              VARCHAR(20) NOT NULL DEFAULT 'OPEN' CHECK (job_status IN ('OPEN','MATCHING','SELECTED','IN_PROGRESS','COMPLETED','CANCELLED')),
    selected_fl_id          VARCHAR(20),
    job_created_at          TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    job_updated_at          TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_jobs_em FOREIGN KEY (em_id)           REFERENCES employers(em_id),
    CONSTRAINT fk_jobs_fl FOREIGN KEY (selected_fl_id)  REFERENCES freelancers(fl_id)
);

CREATE TABLE job_required_languages (
    job_req_lg_id   VARCHAR(20) PRIMARY KEY,
    job_id          VARCHAR(20) NOT NULL,
    language_name   VARCHAR(50) NOT NULL,
    CONSTRAINT fk_jrl_job FOREIGN KEY (job_id) REFERENCES jobs(job_id)
);

CREATE TABLE job_pickups (
    job_pickup_id   VARCHAR(20) PRIMARY KEY,
    job_id          VARCHAR(20) NOT NULL,
    pickup_location VARCHAR(100) NOT NULL,
    pickup_time     VARCHAR(20) NOT NULL,
    sequence        SMALLINT NOT NULL,
    CONSTRAINT fk_job_pickups_job FOREIGN KEY (job_id) REFERENCES jobs(job_id)
);

CREATE TABLE job_customers (
    job_customer_id VARCHAR(20) PRIMARY KEY,
    job_id          VARCHAR(20) NOT NULL,
    customer_name   VARCHAR(150) NOT NULL,
    note            TEXT,
    CONSTRAINT fk_job_customers_job FOREIGN KEY (job_id) REFERENCES jobs(job_id)
);

CREATE TABLE job_customer_pickups (
    id              VARCHAR(20) PRIMARY KEY,
    job_customer_id VARCHAR(20) NOT NULL,
    job_pickup_id   VARCHAR(20) NOT NULL,
    CONSTRAINT fk_jcp_customer FOREIGN KEY (job_customer_id) REFERENCES job_customers(job_customer_id),
    CONSTRAINT fk_jcp_pickup   FOREIGN KEY (job_pickup_id)   REFERENCES job_pickups(job_pickup_id)
);

CREATE TABLE job_itineraries (
    job_itinerary_id    VARCHAR(20) PRIMARY KEY,
    job_id              VARCHAR(20) NOT NULL,
    place_name          VARCHAR(200) NOT NULL,
    start_time          VARCHAR(10) NOT NULL,
    end_time            VARCHAR(10) NOT NULL,
    note                TEXT,
    CONSTRAINT fk_job_itineraries_job FOREIGN KEY (job_id) REFERENCES jobs(job_id)
);

CREATE TABLE job_applications (
    job_application_id  VARCHAR(20) PRIMARY KEY,
    job_id              VARCHAR(20) NOT NULL,
    fl_id               VARCHAR(20) NOT NULL,
    application_status  VARCHAR(20) NOT NULL DEFAULT 'APPLIED' CHECK (application_status IN ('APPLIED','ACCEPTED','REJECTED')),
    applied_at          TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    selected_at         TIMESTAMP,
    CONSTRAINT fk_job_applications_job FOREIGN KEY (job_id) REFERENCES jobs(job_id),
    CONSTRAINT fk_job_applications_fl  FOREIGN KEY (fl_id)  REFERENCES freelancers(fl_id)
);

CREATE TABLE job_payments (
    payment_id      VARCHAR(20) PRIMARY KEY,
    job_id          VARCHAR(20) NOT NULL,
    em_id           VARCHAR(20) NOT NULL,
    fl_id           VARCHAR(20) NOT NULL,
    payment_status  VARCHAR(20) NOT NULL DEFAULT 'PENDING' CHECK (payment_status IN ('PENDING','PAID','CONFIRMED','REJECTED')),
    slip_url        VARCHAR(500),
    reject_reason   TEXT,
    paid_at         TIMESTAMP,
    confirmed_at    TIMESTAMP,
    CONSTRAINT fk_job_payments_job FOREIGN KEY (job_id) REFERENCES jobs(job_id),
    CONSTRAINT fk_job_payments_em  FOREIGN KEY (em_id)  REFERENCES employers(em_id),
    CONSTRAINT fk_job_payments_fl  FOREIGN KEY (fl_id)  REFERENCES freelancers(fl_id)
);

CREATE TABLE fl_reviews (
    fl_review_id    VARCHAR(20) PRIMARY KEY,
    job_id          VARCHAR(20) NOT NULL,
    em_id           VARCHAR(20) NOT NULL,
    fl_id           VARCHAR(20) NOT NULL,
    rating          SMALLINT NOT NULL CHECK (rating BETWEEN 1 AND 5),
    comment         TEXT,
    reviewed_at     TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_fl_reviews_job FOREIGN KEY (job_id) REFERENCES jobs(job_id),
    CONSTRAINT fk_fl_reviews_em  FOREIGN KEY (em_id)  REFERENCES employers(em_id),
    CONSTRAINT fk_fl_reviews_fl  FOREIGN KEY (fl_id)  REFERENCES freelancers(fl_id)
);

CREATE TABLE em_reviews (
    em_review_id    VARCHAR(20) PRIMARY KEY,
    job_id          VARCHAR(20) NOT NULL,
    fl_id           VARCHAR(20) NOT NULL,
    em_id           VARCHAR(20) NOT NULL,
    rating          SMALLINT NOT NULL CHECK (rating BETWEEN 1 AND 5),
    comment         TEXT,
    reviewed_at     TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_em_reviews_job FOREIGN KEY (job_id) REFERENCES jobs(job_id),
    CONSTRAINT fk_em_reviews_fl  FOREIGN KEY (fl_id)  REFERENCES freelancers(fl_id),
    CONSTRAINT fk_em_reviews_em  FOREIGN KEY (em_id)  REFERENCES employers(em_id)
);
