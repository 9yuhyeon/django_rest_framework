from rest_framework.views import APIView
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from articles.models import Article, Comment
from django.db.models.query_utils import Q
from .serializers import ArticleSerializer,ArticleListSerializer, ArticleCreateSerializer, CommentSerializer, CommentCreateSerializer

# Create your views here.
class ArticleView(APIView):
    # 게시글 전체 보기 API
    def get(self, request):
        article = Article.objects.all()
        serializer = ArticleListSerializer(article, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    # 게시글 작성 API
    def post(self, request):
        if not request.user.is_authenticated:
            return Response({"msg":"로그인을 해주세요!"}, status=status.HTTP_401_UNAUTHORIZED)

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
    def get(self, request, article_id):
        article = get_object_or_404(Article, id=article_id)
        comment = article.comment_set.all()
        serializer = CommentSerializer(comment, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 댓글 작성 API
    def post(self, request, article_id):
        serializer = CommentCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, article_id=article_id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CommentDetailView(APIView):
    # 댓글 수정 API
    def put(self, request, article_id, comment_id):
        comment = get_object_or_404(Comment, id=comment_id)
        if comment.user == request.user:
            serializer = CommentCreateSerializer(comment, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"msg":"권한이 없습니다!"}, status=status.HTTP_403_FORBIDDEN)
    
    # 댓글 삭제 API
    def delete(self, request, article_id, comment_id):
        comment = get_object_or_404(Comment, id=comment_id)
        if comment.user == request.user:
            comment.delete()
            return Response({"msg":"삭제완료!"}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"msg":"권한이 없습니다!"}, status=status.HTTP_400_BAD_REQUEST)


class LikeView(APIView):
    # 좋아요 API
    def post(self, request, article_id):
        article = get_object_or_404(Article, id=article_id)
        if request.user in article.like.all():
            article.like.remove(request.user)
            return Response({"msg":"좋아요 취소!"}, status=status.HTTP_200_OK)
        else:
            article.like.add(request.user)
            return Response({"msg":"좋아요!"}, status=status.HTTP_200_OK)


class FeedView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        q = Q()
        for user in request.user.follow.all():
            q.add(Q(user=user),q.OR)
            feeds = Article.objects.filter(q)
            serializer = ArticleListSerializer(feeds, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)