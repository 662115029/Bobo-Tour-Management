"""
test_utils.py — Unit tests for utils.py functions.

UTC numbering follows the Test Plan (Bobo_Tour_Management_Test_Plan_v0.0.0):
  UTC-01: validate_password
  UTC-02: validate_register_fields
  UTC-03: validate_profile_update_fields
  UTC-04: is_tour_cancellable
  UTC-05: validate_pin
  UTC-06: validate_freelancer_register_fields
  UTC-07: sanitize_sort_params
  UTC-08: format_time
  UTC-09: validate_doc_review_status

Run with:  pytest test_utils.py -v
"""

import pytest
from utils import (
    validate_password,
    validate_register_fields,
    validate_profile_update_fields,
    is_tour_cancellable,
    validate_pin,
    validate_freelancer_register_fields,
    sanitize_sort_params,
    format_time,
    validate_doc_review_status,
)


# ---------------------------------------------------------------------------
# UTC-01  validate_password
# ---------------------------------------------------------------------------

class TestValidatePassword:
    def test_valid_password_default_min_length(self):
        # UTC-01-TC-01 / UTC-01-TD-01
        assert validate_password("abcdef") is None

    def test_empty_password_returns_error(self):
        # UTC-01-TC-02 / UTC-01-TD-02
        assert validate_password("") == "Password is required."

    def test_too_short_password_returns_error(self):
        # UTC-01-TC-03 / UTC-01-TD-03
        assert validate_password("abc") == "Password must be at least 6 characters."

    def test_custom_min_length_valid(self):
        # UTC-01-TC-04 / UTC-01-TD-04
        assert validate_password("abcdefgh", min_length=8) is None


# ---------------------------------------------------------------------------
# UTC-02  validate_register_fields
# ---------------------------------------------------------------------------

class TestValidateRegisterFields:
    def test_all_valid_returns_none(self):
        # UTC-02-TC-01 / UTC-02-TD-01
        result = validate_register_fields("bob123", "Bob Smith", "password123", "bob@gmail.com")
        assert result is None

    def test_empty_username_returns_error(self):
        # UTC-02-TC-02 / UTC-02-TD-02
        result = validate_register_fields("", "Bob Smith", "password123", "bob@gmail.com")
        assert result == "Username is required."

    def test_empty_name_returns_error(self):
        # UTC-02-TC-03 / UTC-02-TD-03
        result = validate_register_fields("bob123", "", "password123", "bob@gmail.com")
        assert result == "Name is required."

    def test_invalid_email_returns_error(self):
        # UTC-02-TC-04 / UTC-02-TD-04
        result = validate_register_fields("bob123", "Bob Smith", "password123", "notanemail")
        assert result is not None
        assert "@" in result or "Email" in result

    def test_short_password_returns_8_char_error(self):
        # UTC-02-TC-05 / UTC-02-TD-05
        result = validate_register_fields("bob123", "Bob Smith", "short12", "bob@gmail.com")
        assert result == "Password must be at least 8 characters."

    def test_exactly_8_char_password_is_valid(self):
        # UTC-02-TC-06 / UTC-02-TD-06
        result = validate_register_fields("bob123", "Bob Smith", "12345678", "bob@gmail.com")
        assert result is None


# ---------------------------------------------------------------------------
# UTC-03  validate_profile_update_fields
# ---------------------------------------------------------------------------

class TestValidateProfileUpdateFields:
    def test_non_empty_fields_returns_none(self):
        # UTC-03-TC-01 / UTC-03-TD-01
        assert validate_profile_update_fields({"em_name": "New Name"}) is None

    def test_empty_dict_returns_error(self):
        # UTC-03-TC-02 / UTC-03-TD-02
        assert validate_profile_update_fields({}) == "No fields to update."


# ---------------------------------------------------------------------------
# UTC-04  is_tour_cancellable
# ---------------------------------------------------------------------------

class TestIsTourCancellable:
    def test_open_is_cancellable(self):
        # UTC-04-TC-01 / UTC-04-TD-01
        assert is_tour_cancellable("OPEN") is True

    def test_matching_is_cancellable(self):
        # UTC-04-TC-02 / UTC-04-TD-02
        assert is_tour_cancellable("MATCHING") is True

    def test_matched_is_cancellable(self):
        # UTC-04-TC-03 / UTC-04-TD-03
        assert is_tour_cancellable("MATCHED") is True

    def test_completed_is_not_cancellable(self):
        # UTC-04-TC-04 / UTC-04-TD-04
        assert is_tour_cancellable("COMPLETED") is False

    def test_cancelled_is_not_cancellable(self):
        # UTC-04-TC-05 / UTC-04-TD-05
        assert is_tour_cancellable("CANCELLED") is False


# ---------------------------------------------------------------------------
# UTC-05  validate_pin
# ---------------------------------------------------------------------------

class TestValidatePin:
    def test_valid_6_digit_pin(self):
        # UTC-05-TC-01 / UTC-05-TD-01
        assert validate_pin("123456") is None

    def test_empty_pin_returns_error(self):
        # UTC-05-TC-02 / UTC-05-TD-02
        assert validate_pin("") == "PIN is required."

    def test_none_pin_returns_error(self):
        # UTC-05-TC-03 / UTC-05-TD-03
        assert validate_pin(None) == "PIN is required."

    def test_too_short_pin_returns_error(self):
        # UTC-05-TC-04 / UTC-05-TD-04
        assert validate_pin("1234") == "PIN must be exactly 6 digits."

    def test_too_long_pin_returns_error(self):
        # UTC-05-TC-05 / UTC-05-TD-05
        assert validate_pin("1234567") == "PIN must be exactly 6 digits."

    def test_non_numeric_pin_returns_error(self):
        # UTC-05-TC-06 / UTC-05-TD-06
        assert validate_pin("12a456") == "PIN must contain only numbers."


# ---------------------------------------------------------------------------
# UTC-06  validate_freelancer_register_fields
# ---------------------------------------------------------------------------

class TestValidateFreelancerRegisterFields:
    def test_all_valid_returns_none(self):
        # UTC-06-TC-01 / UTC-06-TD-01
        result = validate_freelancer_register_fields("driver01", "Somchai", "somchai@gmail.com", "123456")
        assert result is None

    def test_empty_username_returns_error(self):
        # UTC-06-TC-02 / UTC-06-TD-02
        result = validate_freelancer_register_fields("", "Somchai", "somchai@gmail.com", "123456")
        assert result == "Username is required."

    def test_empty_name_returns_error(self):
        # UTC-06-TC-03 / UTC-06-TD-03
        result = validate_freelancer_register_fields("driver01", "", "somchai@gmail.com", "123456")
        assert result == "Name is required."

    def test_invalid_email_returns_error(self):
        # UTC-06-TC-04 / UTC-06-TD-04
        result = validate_freelancer_register_fields("driver01", "Somchai", "notanemail", "123456")
        assert result is not None

    def test_invalid_pin_returns_error(self):
        # UTC-06-TC-05 / UTC-06-TD-05
        result = validate_freelancer_register_fields("driver01", "Somchai", "somchai@gmail.com", "12")
        assert result == "PIN must be exactly 6 digits."

    def test_non_numeric_pin_returns_error(self):
        # UTC-06-TC-06 / UTC-06-TD-06
        result = validate_freelancer_register_fields("driver01", "Somchai", "somchai@gmail.com", "abcdef")
        assert result == "PIN must contain only numbers."


# ---------------------------------------------------------------------------
# UTC-07  sanitize_sort_params
# ---------------------------------------------------------------------------

class TestSanitizeSortParams:
    ALLOWED = {"fl_name", "fl_rating_avg", "fl_updated_at", "fl_created_at"}

    def test_allowed_field_kept_as_is(self):
        # UTC-07-TC-01 / UTC-07-TD-01
        sort_by, order = sanitize_sort_params("fl_name", "asc", self.ALLOWED, "fl_updated_at")
        assert sort_by == "fl_name"
        assert order == "ASC"

    def test_disallowed_field_falls_back_to_default(self):
        # UTC-07-TC-02 / UTC-07-TD-02
        sort_by, order = sanitize_sort_params("DROP TABLE users", "desc", self.ALLOWED, "fl_updated_at")
        assert sort_by == "fl_updated_at"
        assert order == "DESC"

    def test_order_desc_uppercased(self):
        # UTC-07-TC-03 / UTC-07-TD-03
        _, order = sanitize_sort_params("fl_name", "DESC", self.ALLOWED, "fl_updated_at")
        assert order == "DESC"

    def test_order_invalid_value_defaults_to_desc(self):
        # UTC-07-TC-04 / UTC-07-TD-04
        _, order = sanitize_sort_params("fl_name", "banana", self.ALLOWED, "fl_updated_at")
        assert order == "DESC"


# ---------------------------------------------------------------------------
# UTC-08  format_time
# ---------------------------------------------------------------------------

class TestFormatTime:
    def test_none_returns_none(self):
        # UTC-08-TC-01 / UTC-08-TD-01
        assert format_time(None) is None

    def test_empty_string_returns_none(self):
        # UTC-08-TC-02 / UTC-08-TD-02
        assert format_time("") is None

    def test_seconds_converted_to_hhmm(self):
        # UTC-08-TC-03 / UTC-08-TD-03
        assert format_time(9000) == "02:30"

    def test_zero_seconds(self):
        # UTC-08-TC-04 / UTC-08-TD-04
        assert format_time(0) == "00:00"

    def test_string_seconds_converted(self):
        # UTC-08-TC-05 / UTC-08-TD-05
        assert format_time("3600") == "01:00"

    def test_non_numeric_string_falls_back_to_truncated(self):
        # UTC-08-TC-06 / UTC-08-TD-06
        assert format_time("09:30") == "09:30"


# ---------------------------------------------------------------------------
# UTC-09  validate_doc_review_status
# ---------------------------------------------------------------------------

class TestValidateDocReviewStatus:
    def test_approved_is_valid(self):
        # UTC-09-TC-01 / UTC-09-TD-01
        assert validate_doc_review_status("APPROVED") is None

    def test_rejected_is_valid(self):
        # UTC-09-TC-02 / UTC-09-TD-02
        assert validate_doc_review_status("REJECTED") is None

    def test_pending_is_valid(self):
        # UTC-09-TC-03 / UTC-09-TD-03
        assert validate_doc_review_status("PENDING") is None

    def test_invalid_status_returns_error(self):
        # UTC-09-TC-04 / UTC-09-TD-04
        result = validate_doc_review_status("DELETED")
        assert result is not None
        assert "status must be one of" in result

    def test_lowercase_status_is_invalid(self):
        # UTC-09-TC-05 / UTC-09-TD-05
        result = validate_doc_review_status("approved")
        assert result is not None
