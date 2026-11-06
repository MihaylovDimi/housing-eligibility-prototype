"""Step definitions that connect the Gherkin scenarios to the code."""

from behave import given, when, then

from src.eligibility_service import ValidationError, check_eligibility


@given("the resident is {age:d} years old")
def set_age(context, age):
    context.age = age


@given("the resident has lived in the borough for {years:d} years")
def set_years(context, years):
    context.years_resident = years


# ":g" accepts whole numbers such as 22000 as well as decimals.
@given("the annual household income is {income:g} pounds")
def set_income(context, income):
    context.income = income


@when("the details are submitted for checking")
def submit_details(context):
    context.result = None
    context.error = None
    try:
        context.result = check_eligibility(
            context.age, context.years_resident, context.income
        )
    except ValidationError as err:
        context.error = str(err)


@then("the resident should be shown as eligible")
def check_eligible(context):
    assert context.error is None, f"Unexpected error: {context.error}"
    assert context.result.is_eligible, context.result.message


@then("the resident should be shown as not eligible")
def check_not_eligible(context):
    assert context.error is None, f"Unexpected error: {context.error}"
    assert not context.result.is_eligible, "Resident was accepted"


@then("a validation error should be raised")
def check_error_raised(context):
    assert context.error is not None, "No ValidationError was raised"


@then('the message should contain "{expected}"')
def check_message(context, expected):
    assert expected in context.result.message, context.result.message


@then('the error message should be "{expected}"')
def check_error_message(context, expected):
    assert context.error == expected, f"Got: {context.error}"