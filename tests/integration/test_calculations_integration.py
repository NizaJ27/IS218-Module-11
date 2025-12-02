import os
import pytest
from app.db import init_db, SessionLocal
from app import schemas, models
from app.operations import calculations as calc_ops


@pytest.fixture(autouse=True)
def setup_db():
    try:
        from app.db import DATABASE_URL
        if DATABASE_URL.startswith("sqlite") and "test_db.sqlite" in DATABASE_URL:
            if os.path.exists("./test_db.sqlite"):
                os.remove("./test_db.sqlite")
    except Exception:
        pass
    init_db()
    yield


def test_create_calculation_stores_result():
    db = SessionLocal()
    try:
        calc_in = schemas.CalculationCreate(a=10, b=5, type=models.CalculationType.DIVIDE)
        calc = calc_ops.create_calculation(db, calc_in, store_result=True)
        assert calc.id is not None
        assert calc.result == 2.0

        # Fetch from DB
        fetched = db.get(models.Calculation, calc.id)
        assert fetched is not None
        assert fetched.result == 2.0
    finally:
        db.close()


def test_create_calculation_invalid_type_raises():
    db = SessionLocal()
    try:
        with pytest.raises(ValueError):
            # using a wrong type value should raise when mapping in compute_result
            bad = schemas.CalculationCreate(a=1, b=1, type="NotAType")
            calc_ops.create_calculation(db, bad)
    finally:
        db.close()
