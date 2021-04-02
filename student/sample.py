from rest_framework import serializers
from uneplan.model.Initiative import Initiative
from uneplan.serializers.simpleSerializers.DepartmentSimpleSerializer import DepartmentSimpleSerializer
from uneplan.serializers.simpleSerializers.ObjectiveSimpleSerializer import ObjectiveSimpleSerializer
from uneplan.serializers.simpleSerializers.UserSimpleSerializer import UserSimpleSerializer
from uneplan.serializers.simpleSerializers.SubtagSimpleSerializer import SubtagSimpleSerializer
from uneplan.serializers.simpleSerializers.ProgressSimpleSerializer import ProgressSimpleSerializer
from uneplan.serializers.simpleSerializers.LevelSimpleSerializer import LevelSimpleSerializer
from uneplan.serializers.simpleSerializers.ActionSimpleSerializer import ActionSimpleSerializer
from uneplan.model.Strategy import Strategy
from uneplan.model.Objective import Objective
from uneplan.model.Action import Action
from uneplan.model.Supertag import Supertag
from uneplan.model.Subtag import Subtag
from uneplan.model.Progress import Progress
import math


class InitiativeComplexSerializer(serializers.ModelSerializer):
    departments = DepartmentSimpleSerializer(many=True)
    objectives = ObjectiveSimpleSerializer(many=True)
    created_by = UserSimpleSerializer(many=False)
    modified_by = UserSimpleSerializer(many=False)
    deleted_by = UserSimpleSerializer(many=False)
    subtags = SubtagSimpleSerializer(many=True)
    progress = ProgressSimpleSerializer(many=True)
    levels = LevelSimpleSerializer(many=True)
    actions = ActionSimpleSerializer(many=True)
    users = UserSimpleSerializer(many=True)
    strategies = serializers.SerializerMethodField('get_strategies')
    supertags = serializers.SerializerMethodField('get_supertags')
    latest_progress = serializers.SerializerMethodField('get_latest_progress')
    progress_percentage = serializers.SerializerMethodField('get_progress_percentage')
    actions = serializers.SerializerMethodField('get_actions')


    def get_actions(self, initiative):
        actions = Action.objects.filter(initiative=initiative).values('name')
        return actions

    def get_strategies(self, initiative):
        objective = Initiative.objects.filter(id=initiative.id).values('objectives')
        strategy = Objective.objects.filter(id__in=objective).values('strategy')
        if (strategy):
            strategyName = Strategy.objects.filter(id__in=strategy).values('name', 'id')
            return strategyName
        else:
            return ''

    def get_supertags(self, initiative):
        subtag = Initiative.objects.filter(id=initiative.id).values('subtags')
        supertag = Subtag.objects.filter(id__in=subtag).values('supertag')
        if (supertag):
            supertagDescription = Supertag.objects.filter(id__in=supertag).values('description', 'id')
            return supertagDescription
        else:
            return ''

    def get_latest_progress(self, initiative):
        if (Progress.objects.filter(initiative=initiative).order_by('created_at').last()):
            return Progress.objects.filter(initiative=initiative).order_by('created_at').last().progress
        else:
            return ''

    def get_progress_percentage(self, initiative):
        if (Progress.objects.filter(initiative=initiative).order_by('created_at').last()):
            return math.floor(
                ((Progress.objects.filter(initiative=initiative).order_by('created_at').last().progress) / initiative.target) * 100)
        else:
            return ''

    def create(self, validated_data):
        raise serializers.ValidationError('Could not create!')

    def update(self, instance, validated_data):
        raise serializers.ValidationError('Could not update!')

    class Meta:
        model = Initiative
        fields = (
            'id', 'name', 'departments', 'objectives', 'description',
            'start_date', 'end_date', 'measurement', 'target', 'is_complete',
            'created_by', 'modified_by', 'deleted_by', 'created_at',
            'modified_at', 'deleted_at', 'subtags', 'progress', 'levels', 'actions', 'users',
            'latest_progress', 'progress_percentage', 'supertags', 'strategies', 'actions'
        )

