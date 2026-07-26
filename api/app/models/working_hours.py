"""Working hours model — recurring weekly schedule.

Uses Python weekday convention: 0=Monday, 6=Sunday.
Multiple intervals per day are supported (e.g. 9-12 and 14-17).

Times are stored as wall-clock times in the clinic timezone.
"""

import datetime

from sqlalchemy import Boolean, Date, Integer, String, Time
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class WorkingHours(Base):
    __tablename__ = "working_hours"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    weekday: Mapped[int] = mapped_column(
        Integer, nullable=False, index=True
    )
    start_time: Mapped[datetime.time] = mapped_column(Time, nullable=False)
    end_time: Mapped[datetime.time] = mapped_column(Time, nullable=False)
    is_active: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=True, server_default="true"
    )
    effective_from: Mapped[datetime.date] = mapped_column(Date, nullable=False)
    effective_until: Mapped[datetime.date | None] = mapped_column(
        Date, nullable=True
    )
