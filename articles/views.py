from rest_framework.views import APIView
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from articles.models import Article
from .serializers import ArticleSerializer,ArticleListSerializer, ArticleCreateSerializer

# Create your views here.
class ArticleView(APIView):
    # 게시글 전체 보기 API
    def get(self, request):
        article = Article.objects.all()
        serializer = ArticleListSerializer(article, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    # 게시글 작성 API
    def post(self, request):
        serializer = ArticleCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ArticleDetailView(APIView):
    # 게시글 상세 페이지 API
    def get(self, request, article_id):
        article = get_object_or_404(Article, id=article_id)
        serializer = ArticleSerializer(article)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    # 게시글 수정 API
    def put(self, request, article_id):
        article = get_object_or_404(Article, id=article_id)
        if article.user == request.user:
            serializer = ArticleCreateSerializer(article, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"msg":"권한이 없습니다!"}, status=status.HTTP_403_FORBIDDEN)
    # 게시글 삭제 API
    def delete(self, request, article_id):
        article = get_object_or_404(Article, id=article_id)
        if article.user == request.user:
            article.delete()
            return Response({"msg":"삭제되었습니다!"}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"msg":"권한이 없습니다!"}, status=status.HTTP_403_FORBIDDEN)

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