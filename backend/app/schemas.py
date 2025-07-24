from pydantic import BaseModel
import datetime

class WaferBase(BaseModel):
    batch_id: str

class WaferCreate(WaferBase):
    pass

class Wafer(WaferBase):
    id: int
    created_at: datetime.datetime

    class Config:
        from_attributes = True

class TestResultBase(BaseModel):
    die_x: int
    die_y: int
    test_name: str
    result_value: float

class TestResultCreate(TestResultBase):
    wafer_id: int

class TestResult(TestResultBase):
    id: int
    wafer_id: int
    timestamp: datetime.datetime

    class Config:
        from_attributes = True

class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str
    role: str

class User(UserBase):
    id: int
    role: str

    class Config:
        from_attributes = True

class WaferTestConfig(BaseModel):
    wafer_id: int
    instrument_type: str  # "SCPI" or "REST"
    test_params: dict
