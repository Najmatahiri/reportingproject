from rest_framework.serializers import ModelSerializer

from reporting.models import MachineVM


class MachineVMSerializer(ModelSerializer):
    class Meta:
        model = MachineVM
        fields = ['id', 'nom_machine', 'ip', 'group', 'os', 'critical', 'important', 'moderate', 'low']
