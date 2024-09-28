from rest_framework import serializers
import phonenumbers
from .models import GroupModel, StudentModel, SubjectModel, ExamModel


class GroupModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupModel
        fields='__all__'


class ExamModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExamModel
        fields='__all__'   

    def to_representation(self, instance):
        # This method ensures we return string representations of the subject and student in responses
        ret = super().to_representation(instance)
        ret['subject'] = instance.subject.name  # Use the subject's name
        ret['student'] = instance.student.name  # Use the subject's name
        return ret

class ExamModelSerializerPartial(ExamModelSerializer):   
    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret.pop('student')
        return ret
    
class StudentModelSerializer(serializers.ModelSerializer):
    exams = ExamModelSerializerPartial(many=True, read_only=True)  # Nested serializer for exams

    class Meta:
        model = StudentModel
        fields = '__all__'  # Include exams in the serialized output

    def to_representation(self, instance):
        # This method ensures we return string representations of the group in responses
        ret = super().to_representation(instance)
        ret['group'] = instance.group.name  # Use the subject's name
        return ret
    
    def validate_phone(self, value):
        # Perform validation for phone number here if needed
        try:
            phone_number = phonenumbers.parse(value, None)
            if not phonenumbers.is_valid_number(phone_number):
                raise serializers.ValidationError(f'{value} is not a valid phone number.')
        except phonenumbers.phonenumberutil.NumberParseException:
            raise serializers.ValidationError(f'{value} is not a valid phone number.')
        return value

class SubjectModelSerializer(serializers.ModelSerializer):
   class Meta:
        model = SubjectModel
        fields='__all__'

