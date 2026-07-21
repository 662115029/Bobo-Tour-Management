"""
utils.py — Pure helper functions extracted from routers.
These contain no database or HTTP dependencies and are fully unit-testable.
"""

from typing import Optional, Tuple


# ---------------------------------------------------------------------------
# UTC-01  validate_password
# ---------------------------------------------------------------------------

def validate_password(password: Optional[str], min_length: int = 6) -> Optional[str]:
    """
    Return an error message string if the password is invalid, or None if valid.
    Rules: must be non-empty and at least `min_length` characters (default 6,
    but every current caller explicitly passes min_length=8 — see below).
    Used by: employers.py (change_employer_password, min_length=8),
             admin.py (change_admin_password, min_length=8),
             validate_register_fields (registration, min_length=8)

    # CHANGE: all call sites now explicitly pass min_length=8, so the
    # 8-character minimum is enforced uniformly at registration AND at
    # password change (employer and admin). The function's own default of
    # 6 is kept only as a fallback for any future caller that omits
    # min_length; it is not relied upon anywhere in this codebase today.
    """
    if not password:
        return "Password is required."
    if len(password) < min_length:
        return f"Password must be at least {min_length} characters."
    return None


# ---------------------------------------------------------------------------
# UTC-02  validate_doc_review_status
# ---------------------------------------------------------------------------

VALID_DOC_STATUSES = {"APPROVED", "REJECTED", "PENDING"}


def validate_doc_review_status(status: str) -> Optional[str]:
    """
    Return an error message string if the status is not a valid document review
    status, or None if valid.
    Used by: freelancers.py (review_fl_document),
             employers.py  (review_em_document)
    """
    if status not in VALID_DOC_STATUSES:
        return f"status must be one of: {', '.join(sorted(VALID_DOC_STATUSES))}."
    return None


# ---------------------------------------------------------------------------
# UTC-03  determine_verify_status
# ---------------------------------------------------------------------------

def determine_verify_status(total: int, approved: int, pending: int) -> str:
    """
    Decide the overall verification status for a freelancer or employer based
    on their document counts.

    Rules (matching the logic in review_fl_document / review_em_document):
      - If all uploaded docs are approved (approved == total > 0)  → 'VERIFIED'
      - If no docs are pending and none are approved (all rejected) → 'NOT_VERIFIED'
      - Otherwise                                                   → 'PENDING'

    Used by: freelancers.py (review_fl_document),
             employers.py  (review_em_document)
    """
    if total == 0:
        return "PENDING"
    if approved == total:
        return "VERIFIED"
    if pending == 0 and approved == 0:
        return "NOT_VERIFIED"
    return "PENDING"


# ---------------------------------------------------------------------------
# UTC-04  sanitize_sort_params
# ---------------------------------------------------------------------------

def sanitize_sort_params(
    sort_by: str,
    sort_order: str,
    allowed_fields: set,
    default_field: str,
) -> Tuple[str, str]:
    """
    Sanitize sorting parameters to prevent SQL injection.
    Returns a (safe_sort_by, safe_order) tuple.
    - sort_by is replaced with default_field if not in allowed_fields.
    - sort_order is normalised to 'ASC' or 'DESC' (default 'DESC').

    Used by: freelancers.py (get_freelancers),
             employers.py  (get_employers)
    """
    safe_sort_by = sort_by if sort_by in allowed_fields else default_field
    safe_order = "ASC" if sort_order.lower() == "asc" else "DESC"
    return safe_sort_by, safe_order


# ---------------------------------------------------------------------------
# UTC-05  validate_language_name
# ---------------------------------------------------------------------------

def validate_language_name(raw: Optional[str]) -> Tuple[Optional[str], Optional[str]]:
    """
    Strip and validate a language name input.
    Returns (cleaned_name, error_message).
    - If valid: (stripped name, None)
    - If empty: (None, error message)

    Used by: freelancers.py (create_or_get_language)
    """
    name = (raw or "").strip()
    if not name:
        return None, "language_name is required."
    return name, None


# ---------------------------------------------------------------------------
# UTC-06  normalize_admin_login_identifier
# ---------------------------------------------------------------------------

_RETRY = " Please verify your details and try again."


def normalize_admin_login_identifier(raw: str) -> Tuple[Optional[str], Optional[str]]:
    """
    Normalise an admin login identifier (username or email).
    Returns (normalised_value, error_message).
    - Plain usernames are returned as-is (stripped).
    - Emails must use the @admin.com domain.
    - Empty input returns an error.

    Used by: admin.py (admin_login)
    """
    s = (raw or "").strip()
    if not s:
        return None, "Username or email is missing." + _RETRY
    if "@" in s:
        local, _, domain = s.rpartition("@")
        domain_clean = domain.strip()
        if not local or not domain_clean or "@" in local:
            return None, "That email address is not valid (check the part before and after @)." + _RETRY
        if domain_clean.lower() != "admin.com":
            return None, f"Admin email must use the domain @admin.com only (you entered: {domain_clean})." + _RETRY
        return s.lower(), None
    return s, None

# ---------------------------------------------------------------------------
# UTC-08  format_time
# ---------------------------------------------------------------------------

def format_time(val) -> Optional[str]:
    """
    Convert a seconds integer or HH:MM string to HH:MM format.
    Returns None for empty/None input.

    Used by: tours.py (create_tour, update_tour) via _format_time
    """
    if val is None or val == "":
        return None
    try:
        secs = int(val)
        h, m = divmod(secs // 60, 60)
        return f"{h:02d}:{m:02d}"
    except (ValueError, TypeError):
        return str(val)[:5] or None

# ---------------------------------------------------------------------------
# UTC-10  validate_register_fields   [Feature 1 — Authentication]
# ---------------------------------------------------------------------------

def validate_register_fields(
    username: Optional[str],
    name: Optional[str],
    password: Optional[str],
    email: Optional[str] = None,
) -> Optional[str]:
    """
    Validate required fields for employer registration.
    Returns an error message string if any required field is invalid, else None.

    Rules (mapped to the Register (Employer) use case, Normal Flow step 4):
      - username must be non-empty                  [A1]
      - name must be non-empty                       [A2]
      - email must be non-empty and a valid format   [A3]
      - password must be non-empty                   [A4]
      - password must be at least 8 characters       [A5]

    Username/email uniqueness ([A8] / [A9]) are checked separately in
    auth.py against the database, not here.

    Used by: auth.py (employer_register)

    # CHANGE: added the `email` param + [A3] email format check (was a bare
    # empty-string check, now uses validate_email_format), and raised the
    # password length requirement to 8 characters via
    # validate_password(password, min_length=8) to implement [A5].
    """
    if not (username or "").strip():
        return "Username is required."  # [A1]
    if not (name or "").strip():
        return "Name is required."  # [A2]
    email_err = validate_email_format(email)  # [A3]
    if email_err:
        return email_err
    pwd_err = validate_password(password, min_length=8)  # [A4] empty / [A5] too short
    if pwd_err:
        return pwd_err
    return None


# ---------------------------------------------------------------------------
# UTC-11  validate_profile_update_fields   [Feature 2 — Profile Management]
# ---------------------------------------------------------------------------

def validate_profile_update_fields(fields: dict) -> Optional[str]:
    """
    Return an error message if the fields dict is empty (nothing to update),
    else None.

    Used by: admin.py (update_admin), employers.py (update_employer)
    """
    if not fields:
        return "No fields to update."
    return None


# ---------------------------------------------------------------------------
# UTC-12  validate_job_payment_review   [Feature 3 — Job Management]
# ---------------------------------------------------------------------------

def validate_job_payment_review(status: str, reject_reason: Optional[str]) -> Optional[str]:
    """
    Validate inputs for reviewing a job payment.
    Returns an error message string if invalid, else None.

    Rules:
      - status must be 'CONFIRMED' or 'REJECTED'
      - reject_reason is required when status is 'REJECTED'

    Used by: jobs.py (review_job_payment)
    """
    if status not in ("CONFIRMED", "REJECTED"):
        return "status must be CONFIRMED or REJECTED."
    if status == "REJECTED" and not reject_reason:
        return "reject_reason is required when rejecting."
    return None


# ---------------------------------------------------------------------------
# UTC-13  is_tour_cancellable   [Feature 3 — Job Management]
# ---------------------------------------------------------------------------

CANCELLABLE_STATUSES = {"OPEN", "MATCHING", "MATCHED"}


def is_tour_cancellable(job_status: str) -> bool:
    """
    Return True if a tour with the given status is allowed to be cancelled.
    Cancellable statuses: OPEN, MATCHING, MATCHED.

    Used by: tours.py (cancel_tour)
    """
    return job_status in CANCELLABLE_STATUSES


# ---------------------------------------------------------------------------
# UTC-14  validate_pin   [Feature 1 — Authentication]
# ---------------------------------------------------------------------------

def validate_pin(pin: Optional[str]) -> Optional[str]:
    """
    Return an error message string if the PIN is invalid, or None if valid.
    Rules: must be non-empty, exactly 6 characters, and all digits.

    Used by: freelancers.py (register_freelancer, freelancer_login)
    """
    if not pin:
        return "PIN is required."
    if not pin.isdigit():
        return "PIN must contain only numbers."
    if len(pin) != 6:
        return "PIN must be exactly 6 digits."
    return None


# ---------------------------------------------------------------------------
# UTC-15  validate_email_format   [Feature 1 — Authentication]
# ---------------------------------------------------------------------------

def validate_email_format(email: Optional[str]) -> Optional[str]:
    """
    Return an error message string if the email does not look like a valid
    email address, or None if valid.

    Rule: must contain exactly one '@', with non-empty text before it and
    a '.' somewhere after it (e.g. name@domain.com).
    This is a lightweight structural check, not full RFC 5322 validation.

    Used by: auth.py (employer_register), freelancers.py (register_freelancer)
    """
    s = (email or "").strip()
    if not s:
        return "Email is required."
    if s.count("@") != 1:
        return "Email must contain exactly one '@'."
    local, domain = s.split("@")
    if not local:
        return "Email is missing the part before '@'."
    if "." not in domain or domain.startswith(".") or domain.endswith("."):
        return "Email domain must contain a valid '.' (e.g. gmail.com)."
    if not domain.split(".")[-1]:
        return "Email must end with a valid domain (e.g. .com)."
    return None


# ---------------------------------------------------------------------------
# UTC-16  validate_freelancer_register_fields   [Feature 1 — Authentication]
# ---------------------------------------------------------------------------

def validate_freelancer_register_fields(
    username: Optional[str],
    name: Optional[str],
    email: Optional[str],
    pin: Optional[str],
) -> Optional[str]:
    """
    Validate required fields for freelancer registration.
    Returns an error message string if any required field is invalid, else None.

    Rules:
      - username must be non-empty
      - name must be non-empty
      - email must be non-empty and a valid email format
      - pin must be non-empty, 6 digits, numeric only

    Used by: freelancers.py (register_freelancer)
    """
    if not (username or "").strip():
        return "Username is required."
    if not (name or "").strip():
        return "Name is required."
    email_err = validate_email_format(email)
    if email_err:
        return email_err
    pin_err = validate_pin(pin)
    if pin_err:
        return pin_err
    return None
