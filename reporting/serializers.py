from rest_framework.serializers import ModelSerializer
from reporting.models import MachineVM, ConfigVersionHS


class MachineVMSerializer(ModelSerializer):
    class Meta:
        model = MachineVM
        fields = ['id', 'nom_machine', 'ip', 'group', 'os', 'critical', 'important', 'moderate', 'low', 'slug']


class ConfigVersionHSSerializer(ModelSerializer):
    class Meta:
        model = ConfigVersionHS
        fields = ["id", "unsupported_versions"]
