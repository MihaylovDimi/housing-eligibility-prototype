"""
Module: eligibility_service.py
Business logic for the Housing Register eligibility pre-check.
"""


class ValidationError(Exception):
    """Raised when user input is missing, of the wrong type or out of range."""


class EligibilityResult:
    """Holds the outcome of an eligibility check."""

    def __init__(self, is_eligible: bool, message: str):
        self.is_eligible = is_eligible
        self.message = message


class HousingEligibilityChecker:
    """Validates applicant data and checks it against the council's basic criteria."""

    @classmethod
    def evaluate_eligibility(cls, age, years_resident, income) -> EligibilityResult:
        """Not implemented yet: always returns 'not eligible' with an empty message."""
        return EligibilityResult(False, "")
