from typing import List
from faker import Faker
from datetime import datetime
from .types import CreditCard, CreditLine, CreditScore, Loan
import random

fake = Faker()
# fake.add_provider(CreditScore)


def get_dummy_credit_score():
    """Generates and returns the dummy credit report"""
    score = CreditScore(
        score=680,
        provider="Experian",
        latest=datetime(year=2023, month=3, day=5),
    )
    score.credit_cards.extend(
        [
            CreditCard(
                name="FamPay Platinum Credit Card",
                bank_name="FamPay",
                limit=1_50_000,
                used=23_000,
            ),
            CreditCard(
                name="Flopkart Axum Platinum Credit Card",
                bank_name="Axum Bank",
                limit=2_50_000,
                used=45_000,
            ),
        ]
    )

    score.credit_lines.extend(
        [
            CreditLine(
                name="Herou Capital",
                provider="IDFFC Bank",
                limit=20_000,
                left_to_pay=5_000,
            )
        ]
    )

    score.loans.extend(
        [
            Loan(
                type="Personal Loan",
                next_due_date=datetime(year=2023, month=3, day=5),
                provider="Manipal Bank",
                total=15_000,
                left_to_pay=5_000,
                tenure=4,
            )
        ]
    )

    return score


def get_random_elements(fn):
    return [fn() for _ in range(random.randint(1, 5))]


def get_random_credit_card():
    return CreditCard(
        name=random.choice(
            [
                "FamPay Platinum Credit Card",
                "Flopkart Axum Platinum Credit Card",
                "FamPay Gold Credit Card",
                "Flopkart Axum Gold Credit Card",
                "FamPay Silver Credit Card",
                "Flopkart Axum Silver Credit Card",
                "FamPay Bronze Credit Card",
                "Flopkart Axum Bronze Credit Card",
                "FamPay Titanium Credit Card",
                "Flopkart Axum Titanium Credit Card",
            ]
        ),
        bank_name=random.choice(
            [
                "FamPay",
                "Axum Bank",
                "IDFFC Bank",
                "Manipal Bank",
                "SBI Bank",
            ]
        ),
        limit=random.randint(10_000, 2_00_000),
        overdue=random.choice([True, False]),
        next_due_date=datetime(year=2023, month=3, day=random.randint(5, 30)),
        used=random.randint(0, 2_00_000),
    )


def get_random_credit_score():
    """Generates and returns the dummy credit report"""
    score = CreditScore(
        score=random.randint(500, 900),
        provider=random.choice(["Experian", "Equifax", "TransUnion"]),
        latest=datetime(year=2023, month=3, day=5),
    )
    score.credit_cards.extend(get_random_elements(get_random_credit_card))

    score.credit_lines.extend(
        [
            CreditLine(
                name="Herou Capital",
                provider="IDFFC Bank",
                limit=20_000,
                left_to_pay=5_000,
            )
        ]
    )

    score.loans.extend(
        [
            Loan(
                type="Personal Loan",
                next_due_date=datetime(year=2023, month=3, day=5),
                provider="Manipal Bank",
                total=15_000,
                left_to_pay=5_000,
                tenure=4,
            )
        ]
    )

    return score


def get_credit_score():
    """Return Credit Report of a given User"""
    # Currently returning Dummy data
    data = get_dummy_credit_score()
    return data
