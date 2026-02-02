from rest_framework import generics,viewsets, status
from rest_framework.response import Response
from django.http import Http404


from . import models as comp_models

from .services import get_video_to_review, create_video_by_user, get_or_create_membership
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


class CompanyView(viewsets.ModelViewSet):
    queryset=comp_models.Companies.objects.all()
    serializer_class=CompanySerializer
        

class MembershipView(generics.CreateAPIView):
    serializer_class=MembershipSerializer

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        member, created = serializer.save()

        return Response(
            self.get_serializer(member).data, 
            status=status.HTTP_201_CREATED if created else status.HTTP_200_OK
        )
    
    
class MembershipUpdateView(generics.UpdateAPIView):
    queryset = comp_models.Memberships.objects.all()
    permission_classes = [IsSuperAdmin]
    serializer_class = MembershipUpdateSerializer

    def get_object(self):
        return None
    
    def perform_update(self, serializer):
        target_member = serializer.validated_data['target_member']

        target_member.role = serializer.validated_data.get('role', target_member.role)
        target_member.is_active = serializer.validated_data.get('is_active', target_member.is_active)
        
        target_member.save()


class VideoAdminView(generics.GenericAPIView):
    queryset = comp_models.Video.objects.all()
    permission_classes = [IsAdmin]

    def get_serializer_class(self):
        if self.request.method in ['PATCH','PUT']:
            return VideoUpdateSerializer
        else:
            return VideoSerializer
    
    def post(self, request, *args, **kwargs):
        user = request.user
        company_id = self.request.data.get('company_id')
        print(f'user_id - {user.id}, company_id - {company_id}')
        video = get_video_to_review(user.pk,company_id)

        if video is None:
            raise Http404("No video available for review")
        
        return Response(
            VideoSerializer(video).data,
            status=status.HTTP_200_OK
        )
    
    def patch(self, request, *args, **kwargs):
        company_id = self.request.data.get('company_id')
        video = get_video_to_review(request.user.id, company_id)
        if not video:
            return Response({'details':' video is None'})
        serializer = self.get_serializer(video,data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_200_OK)
        


class VideoUserView(generics.CreateAPIView):
    queryset = comp_models.Video.objects.all()
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

# @csrf_exempt
# @login_required
# def home_view(request, company_name):
#     company = get_company_by_name(company_name)
#     member, _ = get_or_create_company_member(company=company,user=request.user)
# # -------------------------------- SUPER USER --------------------------------------
#     if member.role == 'Super Admin':
#         return render(request, 'companies/superAdmin.html', {'member': member})
# # -------------------------------- ADMIN --------------------------------------
#     elif member.role == 'Admin':
#         context = {'member': member,}
#         return render(request, 'companies/admin.html', context)
# # -------------------------------- USER --------------------------------------
#     elif member.role == 'User':
#         history = get_user_video_history(member.pk)
#         return render(request, 'companies/user.html',{'history':history, 'member': member})
    



