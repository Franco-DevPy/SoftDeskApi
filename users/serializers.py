from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "birth_date",
            "contact_permission",
            "is_active",
        ]


class RegisterSerializer(serializers.ModelSerializer):
    # Campo password: write_only → no se muestra nunca en GET
    password = serializers.CharField(
        write_only=True, required=True, style={"input_type": "password"}
    )

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "password",
            "birth_date",
            "contact_permission",
        ]

    def create(self, validated_data):
        """
        Crea un usuario correctamente:
        - retira password de validated_data
        - crea instancia User sin contraseña
        - aplica hash con set_password()
        - guarda el usuario
        """

        password = validated_data.pop("password")

        # Creamos el usuario SIN contraseña todavía
        user = User(**validated_data)

        # Encriptamos la contraseña
        user.set_password(password)

        # Guardamos el usuario
        user.save()

        return user

    def validate_username(self, value):
        """
        Validación opcional:
        asegurarse que no exista ya un usuario con ese username
        """
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Ce nom d'utilisateur existe déjà.")
        return value

    def validate_email(self, value):
        """
        Validación opcional:
        email único
        """
        if value and User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Cet email est déjà utilisé.")
        return value
