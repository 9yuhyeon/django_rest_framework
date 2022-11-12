from rest_framework.views import APIView
from rest_framework import status, permissions
from rest_framework.response import responses


# Create your views here.
class ArticleView(APIView):
    # 게시글 전체 보기 API
    def get(self, request):
        pass
    
    # 게시글 작성 API
    def post(self, request):
        pass

class ArticleDetailView(APIView):
    # 게시글 상세 페이지 API
    def get(self, request, article_id):
        pass
    
    # 게시글 수정 API
    def put(self, request, article_id):
        pass
    
    # 게시글 삭제 API
    def delete(self, request, article_id):
        pass

class CommentView(APIView):
    # 댓글 보기 API
    def get(self, request):
        pass
    
    # 댓글 작성 API
    def post(self, request):
        pass

class CommentDetailView(APIView):
    # 댓글 수정 API
    def put(self, request, comment_id):
        pass
    
    # 댓글 삭제 API
    def delete(self, request, comment_id):
        pass

class LikeView(APIView):
    # 좋아요 API
    def post(self, request):
        pass