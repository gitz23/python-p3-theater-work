from xmlrpc.client import Boolean
from sqlalchemy import ForeignKey, Column, Integer, String, Boolean, MetaData, create_engine
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

convention = {
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
}
metadata = MetaData(naming_convention=convention)

engine = create_engine('sqlite:///migrations_test.db')

Base = declarative_base(metadata=metadata)

class Audition(Base):
    __tablename__ = 'auditions'

    id = Column(Integer(), primary_key = True)
    actor = Column(String())
    location = Column(String())
    phone = Column(Integer())
    hired = Column(Boolean())
    role_id = Column(Integer(), ForeignKey('roles.id'))

    roles = relationship("Role", back_populates='auditions')

    def call_back(self):
        self.hired = True

    def __repr__(self):
        return f"Actor {self.actor}: "\
            +f"{self.location},"\
            +f"{self.phone},"\
            +f"{self.hired}"
    
class Role(Base):
    __tablename__ = 'roles'

    id = Column(Integer, primary_key=True)
    charater_name = Column(String())

    auditions = relationship('Audition', back_populates='roles')
    
    def lead(self):
        for audition in self.auditions:
            if audition.hired:
                return audition      
        return 'no actor has been hired for this role'
    
    def understudy(self):
        hired_auditions = [audition for audition in self.auditions if audition.hired]
        if len(hired_auditions) >= 2:
            return hired_auditions[1]
        return 'no actor has been hired for understudy for this role'

    def __repr__(self):
        return f"Role {self.charater_name}: "
    

role = Role()
role.charater_name = "cheese"
print(role)