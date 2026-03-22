from rest_framework import generics,viewsets, status, mixins
from rest_framework.response import Response
from django.http import Http404
from django.db import IntegrityError

from .models import (
    Company,
    Membership,
    Video
)

from .services import (
    get_video_to_review, 
    create_video_by_user, 
    get_or_create_membership,
    create_company_by_user
)

from .serializers import (
    CompanySerializer,
    MembershipSerializer,
    MembershipUpdateSerializer,
    VideoUpdateSerializer,
    VideoSerializer
)

from .permissions import (
    IsAny,
    IsSuperAdmin,
    IsAdmin,
    IsUser
)


class CompanyViewSet(viewsets.ModelViewSet):
    queryset=Company.objects.all()
    serializer_class=CompanySerializer

    def create(self,request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            company, _ = create_company_by_user(
                self.context['request'].user.id,
                **serializer.validated_data
            )
        except IntegrityError as e:
            return Response({'details': str(e)},status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(
                CompanySerializer(company).data,
                status=status.HTTP_201_CREATED
            )
        

class MembershipViewSet(mixins.CreateModelMixin,
                        mixins.UpdateModelMixin,
                        viewsets.GenericViewSet):
    queryset = Membership.objects.all()

    def get_permissions(self):
        if self.action == 'create':
            return [IsAny]
        else:
            return [IsSuperAdmin]
        
    def get_serializer_class(self):
        if self.request.method in ['update','partial_update']:
            return MembershipUpdateSerializer
        else:
            return MembershipSerializer

    def perform_create(self, serializer):
        company_id = serializer.validated_data.get('company_id')

        member, created = Membership.objects.get_or_create(user=self.request.user,company_id=company_id)

        return Response(
            MembershipSerializer(member).data, 
            status=status.HTTP_201_CREATED if created else status.HTTP_200_OK
        )
    


class VideoAdminView(generics.RetrieveUpdateAPIView):
    queryset = Video.objects.all()
    permission_classes = [IsAdmin]

    def get_object(self):
        company_id = self.kwargs.get('company_id')
        user = self.request.user

        member = Membership.objects.filter(user=user,company_id=company_id).first()
        video = get_video_to_review(member)

        return video
        
    def get_serializer_class(self):
        if self.request.method in ['PATCH','PUT']:
            return VideoUpdateSerializer
        else:
            return VideoSerializer
        
    # def perform_update(self, serializer):
        
    
    # def post(self, request, *args, **kwargs):
    #     user = request.user
    #     company_id = self.request.data.get('company_id')
    #     print(f'user_id - {user.id}, company_id - {company_id}')
    #     video = get_video_to_review(user.pk,company_id)

    #     if video is None:
    #         raise Http404("No video available for review")
        
    #     return Response(
    #         VideoSerializer(video).data,
    #         status=status.HTTP_200_OK
    #     )
    
    # def patch(self, request, *args, **kwargs):
    #     company_id = self.request.data.get('company_id')
    #     video = get_video_to_review(request.user.id, company_id)
    #     if not video:
    #         return Response({'details':' video is None'})
    #     serializer = self.get_serializer(video,data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()

    #     return Response(status=status.HTTP_200_OK)
        

class VideoUserView(generics.CreateAPIView):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    permission_classes = [IsUser]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
    
        company_id = serializer.validated_data.get('company_id')
        link = serializer.validated_data.get('link')

        try:
            video = create_video_by_user(
                link=link,
                user_id=request.user.id,
                company_id=company_id
            )
        except Exception as e:
            return Response({'detail':f'cant save video - {e}'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(VideoSerializer(video).data, status=status.HTTP_201_CREATED)



