"""
test_itc09_invite_accept.py — Integration test for ITC-09
(Test Invite Acceptance to Job Match and Auto-Reject Other Applications)

Requires a real DB connection (same env vars as connection.py:
MYSQL_HOST, MYSQL_PORT, MYSQL_DATABASE, MYSQL_USER, MYSQL_PASSWORD)
pointing at a TEST database — this test INSERTs/DELETEs real rows.

NOTE: em_id, fl_id, job_id, job_application_id are all AUTO_INCREMENT
INT UNSIGNED columns in the real schema — they are never chosen by the
caller. This fixture inserts full rows (matching the required columns
used by the real register/create-tour endpoints) and captures the
generated ids via cursor.lastrowid, then uses those ids everywhere.

Run with:  python -m pytest app/routers/test_itc09_invite_accept.py -v
"""

import pytest
from app.db.connection import get_connection, get_cursor
from app.routers.tours import invite_freelancer
from app.routers.jobs import accept_application, reject_application

# Distinctive test-only values so rows are easy to recognize/clean up
# if a run is ever interrupted before teardown runs.
EM_USERNAME = "itc09_test_employer"
EM_EMAIL = "itc09_test_employer@test.local"
FL_A_USERNAME = "itc09_test_fl_a"
FL_A_EMAIL = "itc09_test_fl_a@test.local"
FL_B_USERNAME = "itc09_test_fl_b"
FL_B_EMAIL = "itc09_test_fl_b@test.local"


@pytest.fixture
def setup_data():
    conn = get_connection()
    cur = get_cursor(conn)
    # invite_freelancer/accept_application/reject_application each use a
    # separate pooled connection and commit their own changes. Under the
    # default REPEATABLE READ isolation, this connection's transaction
    # snapshot would keep showing stale data after those commits, so use
    # READ COMMITTED to always see the latest committed state.
    cur.execute("SET SESSION TRANSACTION ISOLATION LEVEL READ COMMITTED")

    # -- employer (em_id is AUTO_INCREMENT — capture via lastrowid) --
    cur.execute(
        """
        INSERT INTO employers
            (em_username, em_email, em_password_hash, em_name, em_phone, em_address, em_bio)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """,
        (EM_USERNAME, EM_EMAIL, "dummy_hash", "ITC09 Test Employer",
         "0800000000", "Test Address", "Test bio"),
    )
    em_id = cur.lastrowid

    # -- freelancers A and B (fl_id is AUTO_INCREMENT) --
    cur.execute(
        """
        INSERT INTO freelancers
            (line_user_id, fl_username, fl_email, fl_name, fl_phone, fl_pin_hash,
             fl_verify_status, fl_is_active)
        VALUES (%s, %s, %s, %s, %s, %s, 'VERIFIED', 1)
        """,
        ("itc09_line_a", FL_A_USERNAME, FL_A_EMAIL, "ITC09 Test FL A",
         "0800000001", "dummy_pin_hash"),
    )
    fl_a = cur.lastrowid

    cur.execute(
        """
        INSERT INTO freelancers
            (line_user_id, fl_username, fl_email, fl_name, fl_phone, fl_pin_hash,
             fl_verify_status, fl_is_active)
        VALUES (%s, %s, %s, %s, %s, %s, 'VERIFIED', 1)
        """,
        ("itc09_line_b", FL_B_USERNAME, FL_B_EMAIL, "ITC09 Test FL B",
         "0800000002", "dummy_pin_hash"),
    )
    fl_b = cur.lastrowid

    # -- job (job_id is AUTO_INCREMENT); job_status defaults to OPEN --
    cur.execute(
        """
        INSERT INTO jobs
            (em_id, job_title, job_description, job_start_date, job_end_date,
             job_required_vehicle_type, job_required_seat, job_price)
        VALUES (%s, %s, %s, %s, %s, 'Sedan', 4, 0)
        """,
        (em_id, "ITC09 Test Job", "Test job for ITC-09",
         "2026-01-01", "2026-01-02"),
    )
    job_id = cur.lastrowid
    conn.commit()

    ids = {"em_id": em_id, "fl_a": fl_a, "fl_b": fl_b, "job_id": job_id}
    yield conn, cur, ids

    # teardown — same order delete_job() uses in jobs.py, so any review/
    # payment rows created against this job_id/em_id/fl_id don't block
    # the deletes below with a foreign key error.
    cur.execute("DELETE FROM fl_reviews WHERE job_id=%s", (job_id,))
    cur.execute("DELETE FROM em_reviews WHERE job_id=%s", (job_id,))
    cur.execute("DELETE FROM job_payments WHERE job_id=%s", (job_id,))
    cur.execute("DELETE FROM job_applications WHERE job_id=%s", (job_id,))
    cur.execute("DELETE FROM jobs WHERE job_id=%s", (job_id,))
    cur.execute("DELETE FROM freelancers WHERE fl_id IN (%s,%s)", (fl_a, fl_b))
    cur.execute("DELETE FROM employers WHERE em_id=%s", (em_id,))
    conn.commit()
    conn.close()


def test_itc09_tc01_invite_creates_pending_and_blocks_second_invite(setup_data):
    conn, cur, ids = setup_data
    invite_freelancer(ids["job_id"], {"em_id": ids["em_id"], "fl_id": ids["fl_a"]})

    cur.execute(
        "SELECT application_status FROM job_applications WHERE job_id=%s AND fl_id=%s",
        (ids["job_id"], ids["fl_a"]),
    )
    assert cur.fetchone()["application_status"] == "PENDING"

    with pytest.raises(Exception):  # HTTPException 409
        invite_freelancer(ids["job_id"], {"em_id": ids["em_id"], "fl_id": ids["fl_b"]})


def test_itc09_tc02_accept_matches_job_and_sets_selected_freelancer(setup_data):
    conn, cur, ids = setup_data
    invite_freelancer(ids["job_id"], {"em_id": ids["em_id"], "fl_id": ids["fl_a"]})
    cur.execute(
        "SELECT job_application_id FROM job_applications WHERE job_id=%s AND fl_id=%s",
        (ids["job_id"], ids["fl_a"]),
    )
    app_id = cur.fetchone()["job_application_id"]

    accept_application(app_id, {})

    cur.execute("SELECT job_status, selected_fl_id FROM jobs WHERE job_id=%s", (ids["job_id"],))
    job = cur.fetchone()
    assert job["job_status"] == "MATCHED"
    assert job["selected_fl_id"] == ids["fl_a"]


def test_itc09_tc03_accept_auto_rejects_other_pending_application(setup_data):
    conn, cur, ids = setup_data
    # Simulate two separate PENDING applications already existing for this job
    # (e.g. freelancer self-apply, not the employer-invite flow) — inserted
    # directly rather than via invite_freelancer(), since that endpoint's
    # single-pending-invite guard (covered by TC01) would otherwise reject
    # the second one before we can test accept_application's auto-reject.
    cur.execute(
        "INSERT INTO job_applications (job_id, fl_id, application_status) VALUES (%s,%s,'PENDING')",
        (ids["job_id"], ids["fl_b"]),
    )
    cur.execute(
        "INSERT INTO job_applications (job_id, fl_id, application_status) VALUES (%s,%s,'PENDING')",
        (ids["job_id"], ids["fl_a"]),
    )
    conn.commit()

    cur.execute(
        "SELECT job_application_id FROM job_applications WHERE job_id=%s AND fl_id=%s",
        (ids["job_id"], ids["fl_a"]),
    )
    app_id = cur.fetchone()["job_application_id"]

    accept_application(app_id, {})

    cur.execute(
        "SELECT application_status FROM job_applications WHERE job_id=%s AND fl_id=%s",
        (ids["job_id"], ids["fl_b"]),
    )
    assert cur.fetchone()["application_status"] == "REJECTED"


def test_itc09_tc04_reject_leaves_job_open_and_unlocks_invite(setup_data):
    conn, cur, ids = setup_data
    invite_freelancer(ids["job_id"], {"em_id": ids["em_id"], "fl_id": ids["fl_a"]})
    cur.execute(
        "SELECT job_application_id FROM job_applications WHERE job_id=%s AND fl_id=%s",
        (ids["job_id"], ids["fl_a"]),
    )
    app_id = cur.fetchone()["job_application_id"]

    reject_application(app_id, {})

    cur.execute("SELECT job_status FROM jobs WHERE job_id=%s", (ids["job_id"],))
    assert cur.fetchone()["job_status"] in ("OPEN", "PENDING")

    # should now succeed — no more PENDING application blocking it
    invite_freelancer(ids["job_id"], {"em_id": ids["em_id"], "fl_id": ids["fl_b"]})
