import pytest

from app.news.providers import is_housing_headline


@pytest.mark.parametrize(
    "headline,relevant",
    [
        ("Mortgage rates change", True),
        ("UK house prices rise", True),
        ("Housing supply improves", True),
        ("Commercial property investment", True),
        ("Sports team wins final", False),
        ("Having problems with a partner", False),
        ("Your Daily Mortgage Import Can Leak History Into Evaluation", False),
    ],
)
def test_housing_relevance(headline, relevant):
    assert is_housing_headline(headline) is relevant
