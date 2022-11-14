from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Article
from .serializers import ArticleSerializer
from users.models import User
from faker import Faker

# Create your tests here.
from django.test.client import MULTIPART_CONTENT, encode_multipart, BOUNDARY
from PIL import Image
import tempfile

# temp_file을 받아서 임시 이미지를 생성하여 넣은 후 temp_file을 리턴 / 즉 file에 image를 넣어주는 메서드
# def get_temporary_image(temp_file):
#     size =  (200,200)
#     color = (255,0,0,0)
#     image = Image.new("RGBA", size, color)
#     image.save(temp_file, 'png')
#     return temp_file

# class ArticleCreateTest(APITestCase):
#     @classmethod
#     def setUpTestData(cls):
#         cls.user_data = {"email":"testuser@test.com", "password":"1234"}
#         cls.create_user = User.objects.create_user("testuser@test.com","1234")
#         cls.article_data = {"title":"testcase","content":"test content"}
    
#     def setUp(self):
#         self.access_token = self.client.post(reverse("token_obtain_pair"), self.user_data).data['access']

    # def test_fail_if_not_login(self):
    #     url = reverse("article_view")
    #     response = self.client.post(url, self.article_data)
    #     self.assertEqual(response.status_code, 401)

    # def test_create_article(self):
    #     response = self.client.post(
    #         path=reverse("article_view"),
    #         data=self.article_data,
    #         HTTP_AUTHORIZATION = f"Bearer {self.access_token}"
    #     )
    #     print(response.data)
    #     self.assertEqual(response.status_code, 201)

    # def test_create_article_with_image(self):
    #     # 임시 이미지 파일 생성
    #     temp_file = tempfile.NamedTemporaryFile() # 이름이 있는 임시 파일 생성
    #     temp_file.name = "image.png" # image.png 라는 이름 할당
    #     image_file = get_temporary_image(temp_file) # image.png 라는 temp_file을 get_temporary_image(temp_file)에 넣어 이미지 생성
    #     image_file.seek(0) # image 파일의 첫 번째 프레임을 저장
    #     self.article_data["image"] = image_file # article에 작성할 image 필드를 위에서 만든 image_file을 사용

    #     # 전송하기
    #     response = self.client.post(
    #         path=reverse("article_view"),
    #         data=encode_multipart(data=self.article_data, boundary=BOUNDARY),
    #         content_type=MULTIPART_CONTENT,
    #         HTTP_AUTHORIZATION = f"Bearer {self.access_token}"
    #     )
    #     print(response.data['image'])
    #     self.assertEqual(response.status_code, 201)


class ArticleReadTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.faker = Faker()
        cls.articles = []
        for i in range(10):
            cls.user = User.objects.create_user(cls.faker.email(), cls.faker.word())
            cls.articles.append(Article.objects.create(title=cls.faker.sentence(), content=cls.faker.text(), user=cls.user))

    def test_get_articles(self):
        for article in self.articles:
            url = article.get_absolute_url()
            response = self.client.get(url)
            serializer = ArticleSerializer(article).data
            for key, value in serializer.items():
                self.assertEqual(response.data[key], value)
                print(key, value)
                # serializer[key]를 해도 OK가 나오지만 response.data의 key를 사용한건 response로 받은 데이터를 시리얼라이징을 하고 난 후 value 값과 일치한지 검사하기 위함
                # serializer[key]로 value와 같은지 검사하는 것은 의미가 없다 이유는 serializer.item을 반복문으로 돌면서 각각의 key value로 넣어주기 때문에 당연히 일치하다.
                # 반대로 response.data[value]와 key가 같은지 검사해도 결과는 같을 것이다.
                # self.assertEqual(serializer[key], value)

