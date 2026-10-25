"""
Module: eligibility_steps.py
Step definitions that connect the Gherkin scenarios to the eligibility service.
"""
from behave import given, when, then

from src.eligibility_service import HousingEligibilityChecker, ValidationError


@given("the resident is {age:d} years old")
def step_set_age(context, age):
    context.age = age


@given("the resident has lived in the borough for {years:d} years")
def step_set_years(context, years):
    context.years_resident = years


# ":g" (general number) accepts whole numbers such as 22000 as well as decimals.
# ":f" would only match numbers written with a decimal point, e.g. 22000.0.
@given("the annual household income is {income:g} pounds")
def step_set_income(context, income):
    context.income = income


@when("the details are submitted for checking")
def step_submit(context):
    context.result = None
    context.validation_error = None
    try:
        context.result = HousingEligibilityChecker.evaluate_eligibility(
            age=context.age,
            years_resident=context.years_resident,
            income=context.income,
        )
    except ValidationError as err:
        context.validation_error = str(err)


@then("the resident should be shown as eligible")
def step_assert_eligible(context):
    assert context.validation_error is None, f"Unexpected validation error: {context.validation_error}"
    assert context.result.is_eligible is True, f"Expected eligible, got: {context.result.message}"


@then("the resident should be shown as not eligible")
def step_assert_not_eligible(context):
    assert context.validation_error is None, f"Unexpected validation error: {context.validation_error}"
    assert context.result.is_eligible is False, "Expected not eligible, but the resident was accepted"


@then("a validation error should be raised")
def step_assert_validation_error(context):
    assert context.validation_error is not None, "Expected a ValidationError, but none was raised"


@then('the message should contain "{expected}"')
def step_assert_message(context, expected):
    assert context.result is not None, "No result was returned"
    assert expected in context.result.message, f"'{expected}' not found in '{context.result.message}'"


@then('the error message should be "{expected}"')
def step_assert_error_message(context, expected):
    assert context.validation_error == expected, (
        f"Expected error '{expected}', got '{context.validation_error}'"
    )
