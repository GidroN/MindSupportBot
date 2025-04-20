from tortoise import models, fields


class User(models.Model):
    tg_id = fields.CharField(max_length=10, unique=True)
    username = fields.CharField(max_length=32, null=True)
    name = fields.CharField(max_length=129)  # 128 max chars + spacebar
    is_active = fields.BooleanField(default=True)
    points = fields.IntField(default=3)
    favourite_posts = fields.ManyToManyField("models.Post", related_name="favourite_by", through="userfavouritepost")

    def __str__(self):
        return f"{self.name} - {self.username} - {self.tg_id}"

    def save(self, *args, **kwargs):
        if self.points < 0:
            self.points = 0

        super().save(*args, **kwargs)


class Category(models.Model):
    name = fields.CharField(max_length=255)

    def __str__(self):
        return self.name


class Post(models.Model):
    title = fields.CharField(max_length=255)
    url = fields.CharField(max_length=300)
    category = fields.ForeignKeyField("models.Category", on_delete=fields.SET_NULL, related_name="posts", null=True)
    user = fields.ForeignKeyField("models.User", on_delete=fields.CASCADE, related_name="posts")

    def __str__(self):
        return self.title


class UserFavouritePost(models.Model):
    user = fields.ForeignKeyField('models.User', on_delete=fields.CASCADE, related_name='user_favourites')
    post = fields.ForeignKeyField('models.Post', on_delete=fields.CASCADE, related_name='recipe_favourites')

    def __str__(self):
        return f"{self.user.name} - {self.post.name}"
