from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

User = get_user_model()

def validate_email_unique(value):
    if User.objects.filter(email__iexact=value).exists():
        raise serializers.ValidationError("This email is already in use.")
    return value

class RegisterSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration with secure password validation and restricted role selection.
    """
    email = serializers.EmailField(
        required=True,
        validators=[validate_email_unique]
    )
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    # Limit role choices to non-admin roles (for example, allow only service providers and clients to register)
    role = serializers.ChoiceField(
        choices=[(role.value, role.label) for role in User.Role 
                 if role.value in [User.Role.SERVICE_PROVIDER, User.Role.CLIENT]]
    )

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'password2', 'role', 'first_name', 'last_name')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Passwords do not match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for retrieving user details with human-friendly role display.
    """
    role_display = serializers.CharField(source="get_role_display", read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'role', 'role_display', 'first_name', 'last_name')

class UpdateProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for updating user profile data.
    """
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')
        extra_kwargs = {'email': {'required': False}}

class ChangePasswordSerializer(serializers.Serializer):
    """
    Serializer for changing user password.
    """
    old_password = serializers.CharField(write_only=True, required=True)
    new_password = serializers.CharField(write_only=True, required=True, validators=[validate_password])

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Incorrect old password.")
        return value

    def validate_new_password(self, value):
        user = self.context['request'].user
        if user.check_password(value):
            raise serializers.ValidationError("New password cannot be the same as the old password.")
        return value

class PasswordResetSerializer(serializers.Serializer):
    """
    Serializer for password reset request.
    """
    email = serializers.EmailField()

    def validate_email(self, value):
        if not User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("No user found with this email.")
        return value
