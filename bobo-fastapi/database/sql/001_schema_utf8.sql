CREATE TABLE admins (
    admin_id      CHAR(36)     PRIMARY KEY DEFAULT (UUID()),
    username      VARCHAR(100) NOT NULL UNIQUE,
    email         VARCHAR(255) NOT NULL UNIQUE,
    name          VARCHAR(100) NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    status        VARCHAR(20)  NOT NULL DEFAULT 'active'
                      CHECK (status IN ('active','inactive')),
    created_at    TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at    TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE admin_logs (
    log_id      CHAR(36)     PRIMARY KEY DEFAULT (UUID()),
    admin_id    CHAR(36)     NOT NULL,
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
    target_id   CHAR(36)     NOT NULL,
    target_name VARCHAR(200),
    note        TEXT,
    created_at  TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (admin_id) REFERENCES admins(admin_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE employers (
    em_id                CHAR(36)     PRIMARY KEY DEFAULT (UUID()),
    em_username          VARCHAR(100) NOT NULL UNIQUE,
    em_email             VARCHAR(255) NOT NULL UNIQUE,
    em_password_hash     VARCHAR(255) NOT NULL,
    em_name              VARCHAR(150) NOT NULL,
    em_phone             VARCHAR(20),
    em_address           TEXT,
    em_bio               TEXT,
    em_profile_image_url VARCHAR(500),
    em_verify_status     VARCHAR(20)  NOT NULL DEFAULT 'PENDING'
                             CHECK (em_verify_status IN ('PENDING','VERIFIED','NOT_VERIFIED')),
    em_is_active         BOOLEAN      NOT NULL DEFAULT TRUE,
    em_rating_avg        DECIMAL(3,1) DEFAULT 0.0,
    em_created_at        TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    em_updated_at        TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE freelancers (
    fl_id                CHAR(36)     PRIMARY KEY DEFAULT (UUID()),
    line_user_id         VARCHAR(100) UNIQUE,
    fl_username          VARCHAR(100) NOT NULL UNIQUE,
    fl_email             VARCHAR(255) NOT NULL UNIQUE,
    fl_name              VARCHAR(150) NOT NULL,
    fl_pin_hash          VARCHAR(255) NOT NULL,
    fl_date_of_birth     DATE,
    fl_phone             VARCHAR(20),
    fl_address           TEXT,
    fl_bio               TEXT,
    fl_profile_image_url VARCHAR(500),
    fl_verify_status     VARCHAR(20)  NOT NULL DEFAULT 'PENDING'
                             CHECK (fl_verify_status IN ('PENDING','VERIFIED','NOT_VERIFIED')),
    fl_is_active         BOOLEAN      NOT NULL DEFAULT TRUE,
    fl_rating_avg        DECIMAL(3,1) DEFAULT 0.0,
    fl_created_at        TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    fl_updated_at        TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE fl_bank_accounts (
    fl_bank_account_id CHAR(36)     PRIMARY KEY DEFAULT (UUID()),
    fl_id              CHAR(36)     NOT NULL,
    account_name       VARCHAR(150) NOT NULL,
    account_number     VARCHAR(20)  NOT NULL,
    bank_name          VARCHAR(100) NOT NULL,
    is_primary         BOOLEAN      NOT NULL DEFAULT TRUE,
    created_at         TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at         TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (fl_id) REFERENCES freelancers(fl_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE em_bank_accounts (
    em_bank_account_id CHAR(36)     PRIMARY KEY DEFAULT (UUID()),
    em_id              CHAR(36)     NOT NULL,
    account_name       VARCHAR(150) NOT NULL,
    account_number     VARCHAR(20)  NOT NULL,
    bank_name          VARCHAR(100) NOT NULL,
    is_primary         BOOLEAN      NOT NULL DEFAULT TRUE,
    created_at         TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at         TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (em_id) REFERENCES employers(em_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE fl_vehicle (
    fl_vehicle_id            CHAR(36)    PRIMARY KEY DEFAULT (UUID()),
    fl_id                    CHAR(36)    NOT NULL,
    fl_vehicle_type          VARCHAR(20) NOT NULL DEFAULT 'VAN'
                                 CHECK (fl_vehicle_type = 'VAN'),
    fl_vehicle_brand         VARCHAR(50) NOT NULL,
    fl_vehicle_model         VARCHAR(50) NOT NULL,
    fl_vehicle_year          SMALLINT    NOT NULL,
    fl_vehicle_seat_capa     SMALLINT    NOT NULL
                                 CHECK (fl_vehicle_seat_capa BETWEEN 9 AND 13),
    fl_vehicle_license_plate VARCHAR(50) NOT NULL,
    fl_vehicle_created_at    TIMESTAMP   NOT NULL DEFAULT CURRENT_TIMESTAMP,
    fl_vehicle_updated_at    TIMESTAMP   NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (fl_id) REFERENCES freelancers(fl_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE fl_vehicle_images (
    fl_vehicle_image_id  CHAR(36)     PRIMARY KEY DEFAULT (UUID()),
    fl_vehicle_id        CHAR(36)     NOT NULL,
    fl_vehicle_image_url VARCHAR(500) NOT NULL,
    uploaded_at          TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (fl_vehicle_id) REFERENCES fl_vehicle(fl_vehicle_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE fl_languages (
    fl_language_id   CHAR(36)    PRIMARY KEY DEFAULT (UUID()),
    fl_id            CHAR(36)    NOT NULL,
    fl_language_name VARCHAR(50) NOT NULL,
    created_at       TIMESTAMP   NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (fl_id) REFERENCES freelancers(fl_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE fl_pickup_areas (
    fl_area_id   CHAR(36)     PRIMARY KEY DEFAULT (UUID()),
    fl_id        CHAR(36)     NOT NULL,
    fl_area_name VARCHAR(100) NOT NULL,
    created_at   TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (fl_id) REFERENCES freelancers(fl_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE fl_availability (
    fl_available_id         CHAR(36)  PRIMARY KEY DEFAULT (UUID()),
    fl_id                   CHAR(36)  NOT NULL UNIQUE,
    fl_available_start_date DATE      NOT NULL,
    fl_available_end_date   DATE      NOT NULL,
    is_active               BOOLEAN   NOT NULL DEFAULT TRUE,
    created_at              TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at              TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (fl_id) REFERENCES freelancers(fl_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE fl_documents (
    fl_doc_id      CHAR(36)     PRIMARY KEY DEFAULT (UUID()),
    fl_id          CHAR(36)     NOT NULL,
    fl_vehicle_id  CHAR(36),
    fl_doc_type    VARCHAR(50)  NOT NULL
                       CHECK (fl_doc_type IN (
                           'PERSONAL_ID',
                           'DRIVER_LICENSE',
                           'PUBLIC_DRIVER_LICENSE',
                           'VEHICLE_REGISTRATION',
                           'VEHICLE_INSPECTION'
                       )),
    file_url       VARCHAR(500) NOT NULL,
    fl_doc_status  VARCHAR(20)  NOT NULL DEFAULT 'PENDING'
                       CHECK (fl_doc_status IN ('PENDING','APPROVED','REJECTED')),
    is_latest      BOOLEAN      NOT NULL DEFAULT TRUE,
    fl_uploaded_at TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    reviewed_by    CHAR(36),
    reviewed_at    TIMESTAMP    NULL DEFAULT NULL,
    FOREIGN KEY (fl_id)         REFERENCES freelancers(fl_id),
    FOREIGN KEY (fl_vehicle_id) REFERENCES fl_vehicle(fl_vehicle_id),
    FOREIGN KEY (reviewed_by)   REFERENCES admins(admin_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE fl_verification (
    fl_verify_id     CHAR(36)    PRIMARY KEY DEFAULT (UUID()),
    fl_id            CHAR(36)    NOT NULL,
    fl_verify_status VARCHAR(20) NOT NULL DEFAULT 'PENDING'
                         CHECK (fl_verify_status IN ('PENDING','VERIFIED','NOT_VERIFIED')),
    is_latest        BOOLEAN     NOT NULL DEFAULT TRUE,
    fl_submitted_at  TIMESTAMP   NOT NULL DEFAULT CURRENT_TIMESTAMP,
    fl_verified_at   TIMESTAMP   NULL DEFAULT NULL,
    reviewed_by      CHAR(36),
    FOREIGN KEY (fl_id)       REFERENCES freelancers(fl_id),
    FOREIGN KEY (reviewed_by) REFERENCES admins(admin_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE em_documents (
    em_doc_id      CHAR(36)     PRIMARY KEY DEFAULT (UUID()),
    em_id          CHAR(36)     NOT NULL,
    em_doc_type    VARCHAR(50)  NOT NULL
                       CHECK (em_doc_type IN (
                           'COMPANY_REGISTRATION',
                           'BUSINESS_LICENSE',
                           'TOURISM_LICENSE',
                           'TAX_ID_DOCUMENT',
                           'AUTHORIZED_PERSON_ID'
                       )),
    file_url       VARCHAR(500) NOT NULL,
    em_doc_status  VARCHAR(20)  NOT NULL DEFAULT 'PENDING'
                       CHECK (em_doc_status IN ('PENDING','APPROVED','REJECTED')),
    is_latest      BOOLEAN      NOT NULL DEFAULT TRUE,
    em_uploaded_at TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    reviewed_by    CHAR(36),
    reviewed_at    TIMESTAMP    NULL DEFAULT NULL,
    FOREIGN KEY (em_id)       REFERENCES employers(em_id),
    FOREIGN KEY (reviewed_by) REFERENCES admins(admin_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE em_verification (
    em_verify_id     CHAR(36)    PRIMARY KEY DEFAULT (UUID()),
    em_id            CHAR(36)    NOT NULL,
    em_verify_status VARCHAR(20) NOT NULL DEFAULT 'PENDING'
                         CHECK (em_verify_status IN ('PENDING','VERIFIED','NOT_VERIFIED')),
    is_latest        BOOLEAN     NOT NULL DEFAULT TRUE,
    em_submitted_at  TIMESTAMP   NOT NULL DEFAULT CURRENT_TIMESTAMP,
    em_verified_at   TIMESTAMP   NULL DEFAULT NULL,
    reviewed_by      CHAR(36),
    FOREIGN KEY (em_id)       REFERENCES employers(em_id),
    FOREIGN KEY (reviewed_by) REFERENCES admins(admin_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE jobs (
    job_id                    CHAR(36)      PRIMARY KEY DEFAULT (UUID()),
    em_id                     CHAR(36)      NOT NULL,
    job_title                 VARCHAR(200)  NOT NULL,
    job_description           TEXT,
    job_start_date            DATE          NOT NULL,
    job_end_date              DATE          NOT NULL,
    job_required_vehicle_type VARCHAR(20)   NOT NULL DEFAULT 'VAN',
    job_required_seat         SMALLINT      NOT NULL,
    job_price                 DECIMAL(12,2) NOT NULL,
    job_status                VARCHAR(20)   NOT NULL DEFAULT 'OPEN'
                                  CHECK (job_status IN ('OPEN','PENDING','MATCHED','IN_PROGRESS','COMPLETED','CANCELLED')),
    selected_fl_id            CHAR(36),
    job_created_at            TIMESTAMP     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    job_updated_at            TIMESTAMP     NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (em_id)          REFERENCES employers(em_id),
    FOREIGN KEY (selected_fl_id) REFERENCES freelancers(fl_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE job_required_languages (
    job_req_lg_id CHAR(36)    PRIMARY KEY DEFAULT (UUID()),
    job_id        CHAR(36)    NOT NULL,
    language_name VARCHAR(50) NOT NULL,
    created_at    TIMESTAMP   NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (job_id) REFERENCES jobs(job_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE job_itineraries (
    job_itinerary_id CHAR(36)     PRIMARY KEY DEFAULT (UUID()),
    job_id           CHAR(36)     NOT NULL,
    place_name       VARCHAR(200) NOT NULL,
    start_time       VARCHAR(10)  NOT NULL,
    end_time         VARCHAR(10)  NOT NULL,
    note             TEXT,
    sequence         SMALLINT     NOT NULL DEFAULT 1,
    created_at       TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (job_id) REFERENCES jobs(job_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE job_passengers (
    job_passenger_id CHAR(36)     PRIMARY KEY DEFAULT (UUID()),
    job_id           CHAR(36)     NOT NULL,
    first_name       VARCHAR(100) NOT NULL,
    last_name        VARCHAR(100),
    hotel_name       VARCHAR(200),
    pickup_time      TIME,
    note             TEXT,
    created_at       TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (job_id) REFERENCES jobs(job_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE job_expenses (
    job_expense_id CHAR(36)      PRIMARY KEY DEFAULT (UUID()),
    job_id         CHAR(36)      NOT NULL,
    item_name      VARCHAR(100)  NOT NULL,
    amount         DECIMAL(10,2) NOT NULL,
    sequence       SMALLINT      NOT NULL DEFAULT 1,
    created_at     TIMESTAMP     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (job_id) REFERENCES jobs(job_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE job_applications (
    job_application_id CHAR(36)    PRIMARY KEY DEFAULT (UUID()),
    job_id             CHAR(36)    NOT NULL,
    fl_id              CHAR(36)    NOT NULL,
    application_status VARCHAR(20) NOT NULL DEFAULT 'APPLIED'
                           CHECK (application_status IN ('APPLIED','MATCHING','ACCEPTED','REJECTED')),
    applied_at         TIMESTAMP   NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at         TIMESTAMP   NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (job_id) REFERENCES jobs(job_id),
    FOREIGN KEY (fl_id)  REFERENCES freelancers(fl_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE job_payments (
    payment_id     CHAR(36)     PRIMARY KEY DEFAULT (UUID()),
    job_id         CHAR(36)     NOT NULL,
    em_id          CHAR(36)     NOT NULL,
    fl_id          CHAR(36)     NOT NULL,
    payment_status VARCHAR(20)  NOT NULL DEFAULT 'PENDING'
                       CHECK (payment_status IN ('PENDING','CONFIRMED','REJECTED')),
    slip_url       VARCHAR(500),
    reject_reason  TEXT,
    paid_at        TIMESTAMP    NULL DEFAULT NULL,
    confirmed_at   TIMESTAMP    NULL DEFAULT NULL,
    updated_at     TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (job_id) REFERENCES jobs(job_id),
    FOREIGN KEY (em_id)  REFERENCES employers(em_id),
    FOREIGN KEY (fl_id)  REFERENCES freelancers(fl_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE fl_reviews (
    fl_review_id CHAR(36)  PRIMARY KEY DEFAULT (UUID()),
    job_id       CHAR(36)  NOT NULL,
    em_id        CHAR(36)  NOT NULL,
    fl_id        CHAR(36)  NOT NULL,
    rating       SMALLINT  NOT NULL CHECK (rating BETWEEN 1 AND 5),
    comment      TEXT,
    reviewed_at  TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (job_id) REFERENCES jobs(job_id),
    FOREIGN KEY (em_id)  REFERENCES employers(em_id),
    FOREIGN KEY (fl_id)  REFERENCES freelancers(fl_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE em_reviews (
    em_review_id CHAR(36)  PRIMARY KEY DEFAULT (UUID()),
    job_id       CHAR(36)  NOT NULL,
    fl_id        CHAR(36)  NOT NULL,
    em_id        CHAR(36)  NOT NULL,
    rating       SMALLINT  NOT NULL CHECK (rating BETWEEN 1 AND 5),
    comment      TEXT,
    reviewed_at  TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (job_id) REFERENCES jobs(job_id),
    FOREIGN KEY (fl_id)  REFERENCES freelancers(fl_id),
    FOREIGN KEY (em_id)  REFERENCES employers(em_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;