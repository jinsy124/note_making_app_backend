from sqlalchemy import Column,Integer,String,DateTime,ForeignKey
from app.core.database import Base
from datetime import datetime,timezone
from sqlalchemy import func
import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Relationship
class Note(Base):
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True, index=True)
    uuid = Column(UUID(as_uuid=True), default=uuid.uuid4, unique=True, index=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    user_id = Column(Integer,ForeignKey("users.id",ondelete='CASCADE'),nullable=False)
    owner = Relationship("User",back_populates="notes")
    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),  # Python default, timezone aware
        server_default=func.now(),
        nullable=False
    )

    updated_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    
    )

    
