-- =============================================================================
-- 001_schema_v3.sql
-- Changes from v2:
--   1. Added lookup tables: languages, areas
--   2. fl_languages → junction table (fl_id + language_id)
--   3. fl_pickup_areas → junction table (fl_id + area_id)
--   4. job_required_languages → uses language_id instead of language_name
--   5. fl_documents.file_url + em_documents.file_url → nullable
--      (5 slots created on registration, upload later)
-- =============================================================================

-- -----------------------------------------------------------------------------
-- admins
-- -----------------------------------------------------------------------------
CREATE TABLE admins (
    admin_id      INT UNSIGNED  NOT NULL AUTO_INCREMENT PRIMARY KEY,
    username      VARCHAR(100)  NOT NULL UNIQUE,
    email         VARCHAR(255)  NOT NULL UNIQUE,
    name          VARCHAR(100)  NOT NULL,
    password_hash VARCHAR(255)  NOT NULL,
    status        VARCHAR(20)   NOT NULL DEFAULT 'active'
                      CHECK (status IN ('active','inactive')),
    created_at    TIMESTAMP     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at    TIMESTAMP     NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- -----------------------------------------------------------------------------
-- admin_logs
-- -----------------------------------------------------------------------------
CREATE TABLE admin_logs (
    log_id      INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    admin_id    INT UNSIGNED NOT NULL,
    action_type VARCHAR(50)  NOT NULL
                    CHECK (action_type IN (
                        'APPROVE_DOCUMENT',
                        'REJECT_DOCUMENT',
                        'VERIFY_FREELANCER',
                        'VERIFY_EMPLOYER',
                        'BAN_USER',
                        'UNBAN_USER',
                        'DELETE_JOB'
                    )),
    target_type VARCHAR(20)  NOT NULL
                    CHECK (target_type IN ('FREELANCER','EMPLOYER','DOCUMENT','JOB')),
    target_id   INT UNSIGNED NOT NULL,
    target_name VARCHAR(200),
    note        TEXT,
    created_at  TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (admin_id) REFERENCES admins(admin_id),
    INDEX idx_admin_logs_admin_id   (admin_id),
    INDEX idx_admin_logs_target     (target_type, target_id),
    INDEX idx_admin_logs_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- -----------------------------------------------------------------------------
-- employers
-- -----------------------------------------------------------------------------
CREATE TABLE employers (
    em_id                INT UNSIGNED  NOT NULL AUTO_INCREMENT PRIMARY KEY,
    em_username          VARCHAR(100)  NOT NULL UNIQUE,
    em_email             VARCHAR(255)  NOT NULL UNIQUE,
    em_password_hash     VARCHAR(255)  NOT NULL,
    em_name              VARCHAR(150)  NOT NULL,
    em_phone             VARCHAR(20),
    em_address           TEXT,
    em_bio               TEXT,
    em_profile_image_url VARCHAR(500),
    em_verify_status     VARCHAR(20)   NOT NULL DEFAULT 'PENDING'
                             CHECK (em_verify_status IN ('PENDING','VERIFIED','NOT_VERIFIED')),
    em_is_active         BOOLEAN       NOT NULL DEFAULT TRUE,
    em_rating_avg        DECIMAL(3,1)  DEFAULT 0.0,
    em_created_at        TIMESTAMP     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    em_updated_at        TIMESTAMP     NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_employers_verify_status (em_verify_status),
    INDEX idx_employers_is_active     (em_is_active)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- -----------------------------------------------------------------------------
-- freelancers
-- -----------------------------------------------------------------------------
CREATE TABLE freelancers (
    fl_id                INT UNSIGNED  NOT NULL AUTO_INCREMENT PRIMARY KEY,
    line_user_id         VARCHAR(100)  UNIQUE,
    fl_username          VARCHAR(100)  NOT NULL UNIQUE,
    fl_email             VARCHAR(255)  NOT NULL UNIQUE,
    fl_name              VARCHAR(150)  NOT NULL,
    fl_pin_hash          VARCHAR(255)  NOT NULL,
    fl_date_of_birth     DATE,
    fl_phone             VARCHAR(20),
    fl_address           TEXT,
    fl_bio               TEXT,
    fl_profile_image_url VARCHAR(500),
    fl_verify_status     VARCHAR(20)   NOT NULL DEFAULT 'PENDING'
                             CHECK (fl_verify_status IN ('PENDING','VERIFIED','NOT_VERIFIED')),
    fl_is_active         BOOLEAN       NOT NULL DEFAULT TRUE,
    fl_rating_avg        DECIMAL(3,1)  DEFAULT 0.0,
    fl_created_at        TIMESTAMP     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    fl_updated_at        TIMESTAMP     NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_freelancers_verify_status (fl_verify_status),
    INDEX idx_freelancers_is_active     (fl_is_active),
    INDEX idx_freelancers_line_user_id  (line_user_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- -----------------------------------------------------------------------------
-- fl_bank_accounts
-- -----------------------------------------------------------------------------
CREATE TABLE fl_bank_accounts (
    fl_bank_account_id INT UNSIGNED  NOT NULL AUTO_INCREMENT PRIMARY KEY,
    fl_id              INT UNSIGNED  NOT NULL,
    account_name       VARCHAR(150)  NOT NULL,
    account_number     VARCHAR(20)   NOT NULL,
    bank_name          VARCHAR(100)  NOT NULL,
    is_primary         BOOLEAN       NOT NULL DEFAULT TRUE,
    created_at         TIMESTAMP     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at         TIMESTAMP     NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (fl_id) REFERENCES freelancers(fl_id),
    INDEX idx_fl_bank_fl_id      (fl_id),
    INDEX idx_fl_bank_is_primary (fl_id, is_primary)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- -----------------------------------------------------------------------------
-- em_bank_accounts
-- -----------------------------------------------------------------------------
CREATE TABLE em_bank_accounts (
    em_bank_account_id INT UNSIGNED  NOT NULL AUTO_INCREMENT PRIMARY KEY,
    em_id              INT UNSIGNED  NOT NULL,
    account_name       VARCHAR(150)  NOT NULL,
    account_number     VARCHAR(20)   NOT NULL,
    bank_name          VARCHAR(100)  NOT NULL,
    is_primary         BOOLEAN       NOT NULL DEFAULT TRUE,
    created_at         TIMESTAMP     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at         TIMESTAMP     NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (em_id) REFERENCES employers(em_id),
    INDEX idx_em_bank_em_id      (em_id),
    INDEX idx_em_bank_is_primary (em_id, is_primary)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- -----------------------------------------------------------------------------
-- fl_vehicle
-- -----------------------------------------------------------------------------
CREATE TABLE fl_vehicle (
    fl_vehicle_id            INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    fl_id                    INT UNSIGNED NOT NULL,
    fl_vehicle_type          VARCHAR(20)  NOT NULL DEFAULT 'VAN'
                                 CHECK (fl_vehicle_type = 'VAN'),
    fl_vehicle_brand         VARCHAR(50)  NOT NULL,
    fl_vehicle_model         VARCHAR(50)  NOT NULL,
    fl_vehicle_year          SMALLINT     NOT NULL,
    fl_vehicle_seat_capa     SMALLINT     NOT NULL
                                 CHECK (fl_vehicle_seat_capa BETWEEN 9 AND 13),
    fl_vehicle_license_plate VARCHAR(50)  NOT NULL,
    fl_vehicle_created_at    TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    fl_vehicle_updated_at    TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (fl_id) REFERENCES freelancers(fl_id),
    INDEX idx_fl_vehicle_fl_id (fl_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- -----------------------------------------------------------------------------
-- fl_vehicle_images
-- -----------------------------------------------------------------------------
CREATE TABLE fl_vehicle_images (
    fl_vehicle_image_id  INT UNSIGNED  NOT NULL AUTO_INCREMENT PRIMARY KEY,
    fl_vehicle_id        INT UNSIGNED  NOT NULL,
    fl_vehicle_image_url VARCHAR(500)  NOT NULL,
    uploaded_at          TIMESTAMP     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (fl_vehicle_id) REFERENCES fl_vehicle(fl_vehicle_id),
    INDEX idx_fl_vehicle_images_vehicle_id (fl_vehicle_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- -----------------------------------------------------------------------------
-- languages  ← new lookup table
-- stores unique language names
-- if user types a new language name → insert new record
-- if name already exists → reuse existing id
-- -----------------------------------------------------------------------------
CREATE TABLE languages (
    language_id   INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    language_name VARCHAR(50)  NOT NULL UNIQUE,
    INDEX idx_languages_name (language_name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- -----------------------------------------------------------------------------
-- fl_languages  ← junction table (links freelancer to language)
-- 1 freelancer can have multiple languages
-- 1 language can be used by many freelancers
-- -----------------------------------------------------------------------------
CREATE TABLE fl_languages (
    fl_id       INT UNSIGNED NOT NULL,
    language_id INT UNSIGNED NOT NULL,
    PRIMARY KEY (fl_id, language_id),
    FOREIGN KEY (fl_id)       REFERENCES freelancers(fl_id),
    FOREIGN KEY (language_id) REFERENCES languages(language_id),
    INDEX idx_fl_languages_language_id (language_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- -----------------------------------------------------------------------------
-- areas  ← new lookup table
-- stores unique area names
-- if user types a new area name → insert new record
-- if name already exists → reuse existing id
-- typos or different spacing → new record (by design)
-- -----------------------------------------------------------------------------
CREATE TABLE areas (
    area_id   INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    area_name VARCHAR(100) NOT NULL UNIQUE,
    INDEX idx_areas_name (area_name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- -----------------------------------------------------------------------------
-- fl_pickup_areas  ← junction table (links freelancer to area)
-- 1 freelancer can have multiple areas
-- 1 area can have many freelancers
-- -----------------------------------------------------------------------------
CREATE TABLE fl_pickup_areas (
    fl_id   INT UNSIGNED NOT NULL,
    area_id INT UNSIGNED NOT NULL,
    PRIMARY KEY (fl_id, area_id),
    FOREIGN KEY (fl_id)   REFERENCES freelancers(fl_id),
    FOREIGN KEY (area_id) REFERENCES areas(area_id),
    INDEX idx_fl_pickup_areas_area_id (area_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- -----------------------------------------------------------------------------
-- fl_availability
-- -----------------------------------------------------------------------------
CREATE TABLE fl_availability (
    fl_available_id         INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    fl_id                   INT UNSIGNED NOT NULL UNIQUE,
    fl_available_start_date DATE         NOT NULL,
    fl_available_end_date   DATE         NOT NULL,
    is_active               BOOLEAN      NOT NULL DEFAULT TRUE,
    created_at              TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at              TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT chk_availability_max_30_days
        CHECK (DATEDIFF(fl_available_end_date, fl_available_start_date) <= 30),
    CONSTRAINT chk_availability_end_after_start
        CHECK (fl_available_end_date >= fl_available_start_date),
    FOREIGN KEY (fl_id) REFERENCES freelancers(fl_id),
    INDEX idx_fl_availability_fl_id (fl_id),
    INDEX idx_fl_availability_dates (is_active, fl_available_start_date, fl_available_end_date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- -----------------------------------------------------------------------------
-- fl_documents
-- Important notes:
--   - Every freelancer gets 5 records on registration (created by backend)
--   - file_url = NULL means not yet uploaded
--   - file_url has value means uploaded, pending admin review
--   - UPDATE overwrites the same slot when resubmitting (no history in this table)
--   - All action history (approve/reject) stored in admin_logs instead
--   - fl_doc_status = APPROVED for all 5 docs → user can be verified
-- -----------------------------------------------------------------------------
CREATE TABLE fl_documents (
    fl_doc_id      INT UNSIGNED  NOT NULL AUTO_INCREMENT PRIMARY KEY,
    fl_id          INT UNSIGNED  NOT NULL,
    fl_vehicle_id  INT UNSIGNED  NULL DEFAULT NULL,
    fl_doc_type    VARCHAR(50)   NOT NULL
                       CHECK (fl_doc_type IN (
                           'PERSONAL_ID',
                           'DRIVER_LICENSE',
                           'PUBLIC_DRIVER_LICENSE',
                           'VEHICLE_REGISTRATION',
                           'VEHICLE_INSPECTION'
                       )),
    file_url       VARCHAR(500)  NULL DEFAULT NULL,
    fl_doc_status  VARCHAR(20)   NOT NULL DEFAULT 'PENDING'
                       CHECK (fl_doc_status IN ('PENDING','APPROVED','REJECTED')),
    reject_reason  TEXT          NULL DEFAULT NULL,
    fl_uploaded_at TIMESTAMP     NULL DEFAULT NULL,
    reviewed_by    INT UNSIGNED  NULL DEFAULT NULL,
    reviewed_at    TIMESTAMP     NULL DEFAULT NULL,
    UNIQUE KEY uq_fl_doc (fl_id, fl_doc_type),
    FOREIGN KEY (fl_id)         REFERENCES freelancers(fl_id),
    FOREIGN KEY (fl_vehicle_id) REFERENCES fl_vehicle(fl_vehicle_id),
    FOREIGN KEY (reviewed_by)   REFERENCES admins(admin_id),
    INDEX idx_fl_documents_fl_id      (fl_id),
    INDEX idx_fl_documents_status     (fl_doc_status),
    INDEX idx_fl_documents_vehicle_id (fl_vehicle_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- -----------------------------------------------------------------------------
-- fl_verification
-- -----------------------------------------------------------------------------
CREATE TABLE fl_verification (
    fl_verify_id     INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    fl_id            INT UNSIGNED NOT NULL,
    fl_verify_status VARCHAR(20)  NOT NULL DEFAULT 'PENDING'
                         CHECK (fl_verify_status IN ('PENDING','VERIFIED','NOT_VERIFIED')),
    is_latest        BOOLEAN      NOT NULL DEFAULT TRUE,
    fl_submitted_at  TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    fl_verified_at   TIMESTAMP    NULL DEFAULT NULL,
    reviewed_by      INT UNSIGNED,
    FOREIGN KEY (fl_id)       REFERENCES freelancers(fl_id),
    FOREIGN KEY (reviewed_by) REFERENCES admins(admin_id),
    INDEX idx_fl_verification_fl_id  (fl_id),
    INDEX idx_fl_verification_status (fl_verify_status),
    INDEX idx_fl_verification_latest (fl_id, is_latest)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- -----------------------------------------------------------------------------
-- em_documents
-- Important notes:
--   - Every employer gets 5 records on registration (created by backend)
--   - file_url = NULL means not yet uploaded
--   - UPDATE overwrites the same slot when resubmitting (no history in this table)
--   - All action history (approve/reject) stored in admin_logs instead
--   - em_doc_status = APPROVED for all 5 docs → user can be verified
-- -----------------------------------------------------------------------------
CREATE TABLE em_documents (
    em_doc_id      INT UNSIGNED  NOT NULL AUTO_INCREMENT PRIMARY KEY,
    em_id          INT UNSIGNED  NOT NULL,
    em_doc_type    VARCHAR(50)   NOT NULL
                       CHECK (em_doc_type IN (
                           'COMPANY_REGISTRATION',
                           'BUSINESS_LICENSE',
                           'TOURISM_LICENSE',
                           'TAX_ID_DOCUMENT',
                           'AUTHORIZED_PERSON_ID'
                       )),
    file_url       VARCHAR(500)  NULL DEFAULT NULL,
    em_doc_status  VARCHAR(20)   NOT NULL DEFAULT 'PENDING'
                       CHECK (em_doc_status IN ('PENDING','APPROVED','REJECTED')),
    reject_reason  TEXT          NULL DEFAULT NULL,
    em_uploaded_at TIMESTAMP     NULL DEFAULT NULL,
    reviewed_by    INT UNSIGNED  NULL DEFAULT NULL,
    reviewed_at    TIMESTAMP     NULL DEFAULT NULL,
    UNIQUE KEY uq_em_doc (em_id, em_doc_type),
    FOREIGN KEY (em_id)       REFERENCES employers(em_id),
    FOREIGN KEY (reviewed_by) REFERENCES admins(admin_id),
    INDEX idx_em_documents_em_id  (em_id),
    INDEX idx_em_documents_status (em_doc_status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- -----------------------------------------------------------------------------
-- em_verification
-- -----------------------------------------------------------------------------
CREATE TABLE em_verification (
    em_verify_id     INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    em_id            INT UNSIGNED NOT NULL,
    em_verify_status VARCHAR(20)  NOT NULL DEFAULT 'PENDING'
                         CHECK (em_verify_status IN ('PENDING','VERIFIED','NOT_VERIFIED')),
    is_latest        BOOLEAN      NOT NULL DEFAULT TRUE,
    em_submitted_at  TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    em_verified_at   TIMESTAMP    NULL DEFAULT NULL,
    reviewed_by      INT UNSIGNED,
    FOREIGN KEY (em_id)       REFERENCES employers(em_id),
    FOREIGN KEY (reviewed_by) REFERENCES admins(admin_id),
    INDEX idx_em_verification_em_id  (em_id),
    INDEX idx_em_verification_status (em_verify_status),
    INDEX idx_em_verification_latest (em_id, is_latest)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- -----------------------------------------------------------------------------
-- jobs
-- -----------------------------------------------------------------------------
CREATE TABLE jobs (
    job_id                    INT UNSIGNED   NOT NULL AUTO_INCREMENT PRIMARY KEY,
    em_id                     INT UNSIGNED   NOT NULL,
    job_title                 VARCHAR(200)   NOT NULL,
    job_description           TEXT,
    job_start_date            DATE           NOT NULL,
    job_end_date              DATE           NOT NULL,
    job_required_vehicle_type VARCHAR(20)    NOT NULL DEFAULT 'VAN',
    job_required_seat         SMALLINT       NOT NULL,
    job_price                 DECIMAL(12,2)  NOT NULL,
    job_status                VARCHAR(20)    NOT NULL DEFAULT 'OPEN'
                                  CHECK (job_status IN ('OPEN','PENDING','MATCHED','IN_PROGRESS','COMPLETED','CANCELLED')),
    selected_fl_id            INT UNSIGNED,
    job_created_at            TIMESTAMP      NOT NULL DEFAULT CURRENT_TIMESTAMP,
    job_updated_at            TIMESTAMP      NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (em_id)          REFERENCES employers(em_id),
    FOREIGN KEY (selected_fl_id) REFERENCES freelancers(fl_id),
    INDEX idx_jobs_em_id          (em_id),
    INDEX idx_jobs_status         (job_status),
    INDEX idx_jobs_selected_fl_id (selected_fl_id),
    INDEX idx_jobs_start_date     (job_start_date),
    INDEX idx_jobs_created_at     (job_created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- -----------------------------------------------------------------------------
-- job_required_languages  ← uses language_id instead of language_name
-- junction table linking job to language
-- -----------------------------------------------------------------------------
CREATE TABLE job_required_languages (
    job_id      INT UNSIGNED NOT NULL,
    language_id INT UNSIGNED NOT NULL,
    PRIMARY KEY (job_id, language_id),
    FOREIGN KEY (job_id)      REFERENCES jobs(job_id),
    FOREIGN KEY (language_id) REFERENCES languages(language_id),
    INDEX idx_job_req_lang_language_id (language_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- -----------------------------------------------------------------------------
-- job_itineraries
-- -----------------------------------------------------------------------------
CREATE TABLE job_itineraries (
    job_itinerary_id INT UNSIGNED  NOT NULL AUTO_INCREMENT PRIMARY KEY,
    job_id           INT UNSIGNED  NOT NULL,
    itinerary_date   DATE          NOT NULL,
    place_name       VARCHAR(200)  NOT NULL,
    start_time       VARCHAR(10)   NOT NULL,
    end_time         VARCHAR(10)   NOT NULL,
    note             TEXT,
    sequence         SMALLINT      NOT NULL DEFAULT 1,
    created_at       TIMESTAMP     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (job_id) REFERENCES jobs(job_id),
    INDEX idx_job_itineraries_job_id (job_id, sequence)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- -----------------------------------------------------------------------------
-- job_passengers
-- -----------------------------------------------------------------------------
CREATE TABLE job_passengers (
    job_passenger_id INT UNSIGNED  NOT NULL AUTO_INCREMENT PRIMARY KEY,
    job_id           INT UNSIGNED  NOT NULL,
    first_name       VARCHAR(100)  NOT NULL,
    last_name        VARCHAR(100),
    hotel_name       VARCHAR(200),
    pickup_time      TIME,
    note             TEXT,
    created_at       TIMESTAMP     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (job_id) REFERENCES jobs(job_id),
    INDEX idx_job_passengers_job_id (job_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- -----------------------------------------------------------------------------
-- job_expenses
-- -----------------------------------------------------------------------------
CREATE TABLE job_expenses (
    job_expense_id INT UNSIGNED   NOT NULL AUTO_INCREMENT PRIMARY KEY,
    job_id         INT UNSIGNED   NOT NULL,
    item_name      VARCHAR(100)   NOT NULL,
    amount         DECIMAL(10,2)  NOT NULL,
    sequence       SMALLINT       NOT NULL DEFAULT 1,
    created_at     TIMESTAMP      NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (job_id) REFERENCES jobs(job_id),
    INDEX idx_job_expenses_job_id (job_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- -----------------------------------------------------------------------------
-- job_applications
-- -----------------------------------------------------------------------------
CREATE TABLE job_applications (
    job_application_id INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    job_id             INT UNSIGNED NOT NULL,
    fl_id              INT UNSIGNED NOT NULL,
    application_status VARCHAR(20)  NOT NULL DEFAULT 'APPLIED'
                           CHECK (application_status IN ('APPLIED','PENDING','ACCEPTED','REJECTED')),
    applied_at         TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at         TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (job_id) REFERENCES jobs(job_id),
    FOREIGN KEY (fl_id)  REFERENCES freelancers(fl_id),
    INDEX idx_job_applications_job_id    (job_id),
    INDEX idx_job_applications_fl_id     (fl_id),
    INDEX idx_job_applications_status    (application_status),
    INDEX idx_job_applications_applied_at (applied_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- -----------------------------------------------------------------------------
-- job_payments
-- -----------------------------------------------------------------------------
CREATE TABLE job_payments (
    payment_id     INT UNSIGNED  NOT NULL AUTO_INCREMENT PRIMARY KEY,
    job_id         INT UNSIGNED  NOT NULL,
    em_id          INT UNSIGNED  NOT NULL,
    fl_id          INT UNSIGNED  NOT NULL,
    payment_status VARCHAR(20)   NOT NULL DEFAULT 'PENDING'
                       CHECK (payment_status IN ('PENDING','CONFIRMED','REJECTED')),
    slip_url       VARCHAR(500),
    reject_reason  TEXT,
    paid_at        TIMESTAMP     NULL DEFAULT NULL,
    confirmed_at   TIMESTAMP     NULL DEFAULT NULL,
    updated_at     TIMESTAMP     NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (job_id) REFERENCES jobs(job_id),
    FOREIGN KEY (em_id)  REFERENCES employers(em_id),
    FOREIGN KEY (fl_id)  REFERENCES freelancers(fl_id),
    INDEX idx_job_payments_job_id (job_id),
    INDEX idx_job_payments_em_id  (em_id),
    INDEX idx_job_payments_fl_id  (fl_id),
    INDEX idx_job_payments_status (payment_status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- -----------------------------------------------------------------------------
-- fl_reviews
-- -----------------------------------------------------------------------------
CREATE TABLE fl_reviews (
    fl_review_id INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    job_id       INT UNSIGNED NOT NULL,
    em_id        INT UNSIGNED NOT NULL,
    fl_id        INT UNSIGNED NOT NULL,
    rating       SMALLINT     NOT NULL CHECK (rating BETWEEN 1 AND 5),
    comment      TEXT,
    reviewed_at  TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (job_id) REFERENCES jobs(job_id),
    FOREIGN KEY (em_id)  REFERENCES employers(em_id),
    FOREIGN KEY (fl_id)  REFERENCES freelancers(fl_id),
    INDEX idx_fl_reviews_fl_id  (fl_id),
    INDEX idx_fl_reviews_job_id (job_id),
    INDEX idx_fl_reviews_em_id  (em_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- -----------------------------------------------------------------------------
-- em_reviews
-- -----------------------------------------------------------------------------
CREATE TABLE em_reviews (
    em_review_id INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    job_id       INT UNSIGNED NOT NULL,
    fl_id        INT UNSIGNED NOT NULL,
    em_id        INT UNSIGNED NOT NULL,
    rating       SMALLINT     NOT NULL CHECK (rating BETWEEN 1 AND 5),
    comment      TEXT,
    reviewed_at  TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (job_id) REFERENCES jobs(job_id),
    FOREIGN KEY (fl_id)  REFERENCES freelancers(fl_id),
    FOREIGN KEY (em_id)  REFERENCES employers(em_id),
    INDEX idx_em_reviews_em_id  (em_id),
    INDEX idx_em_reviews_job_id (job_id),
    INDEX idx_em_reviews_fl_id  (fl_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;