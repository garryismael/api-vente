from src.app import ma
from src.models.user import User


class UserSerializer(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        include_fk = True
        load_instance = True
    

user_serializer = UserSerializer()
users_serializer = UserSerializer(many=True, only=('id', 'name', 'address', 'is_admin'))
